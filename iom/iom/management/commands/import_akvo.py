'''
Created on Aug 6, 2015

@author: theo
'''
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from optparse import make_option
from django.contrib.gis.geos import Point
import pytz,datetime, time
import logging

from acacia.data.models import ProjectLocatie
from iom import util
from iom.akvo import FlowAPI
from iom.models import AkvoFlow, CartoDb, Meetpunt, Waarnemer

logger = logging.getLogger('akvo')

def importAkvoRegistration(api,surveyId,projectlocatie,user):
    meetpunten=set()
    for key,instance in api.get_registration_instances(surveyId).items():
        identifier=instance['surveyedLocaleIdentifier']
        locale = instance['surveyedLocaleDisplayName']
        submitter = instance['submitterName']
        device = instance['deviceIdentifier']
        date=instance['collectionDate']
        date=datetime.datetime.utcfromtimestamp(date/1000.0).replace(tzinfo=pytz.utc)
        answers = api.get_answers(instance['keyId'])
        meetid = api.get_answer(answers,questionID='6040925')
        foto = api.get_answer(answers,questionID='8070919')
        geoloc = api.get_answer(answers,questionID='9070917')
        try:
            lat,lon,elev,code = geoloc.split('|')
            location = Point(float(lon),float(lat),srid=4326)
            location.transform(28992)
        except:
            logger.error('Probleem met coordinaten {loc}'.format(loc=geoloc))
            continue

        waarnemer,created = Waarnemer.objects.get_or_create(akvoname=submitter,defaults={'achternaam':submitter})
        if created:
            logger.info('Waarnemer {name} aangemaakt'.format(name=submitter))
            
        meetpunt, created = waarnemer.meetpunt_set.get_or_create(identifier=identifier, defaults={
            'name': meetid or locale, 
            'projectlocatie': projectlocatie, 
            'location': location, 
            'device': device, 
            'photo_url': foto,
            'description': 'imported from {url}'.format(url=api.instance)})
        if created:
            logger.info('Meetpunt {locatie} aangemaakt'.format(locatie=meetpunt.name))
        
        ec = api.get_answer(answers,questionID='3020916')
        diep = api.get_answer(answers,questionID='6060916')

        waarnemingen = meetpunt.waarneming_set.filter(naam='EC_'+diep,datum=date)
        if waarnemingen.exists():
            logger.warning('EC waarnemingen worden vervangen voor {locatie}, datum={date}'.format(locatie=meetpunt.name,date=date)) 
            waarnemingen.delete()
        meetpunt.waarneming_set.create(naam='EC_'+diep, waarnemer=waarnemer, datum=date, device=device, waarde=ec, opmerking='', foto_url=foto, eenheid='uS/cm' )
        logger.debug('EC_{diep}, {date}, EC={ec}'.format(diep=diep, date=date, ec=ec))
        
        meetpunten.add(meetpunt)
        
    return meetpunten
   
def importAkvoMonitoring(api,surveys):
    meetpunten = set()
    for surveyId in surveys:
        survey = api.get_survey(surveyId)
        instances,meta = api.get_survey_instances(surveyId=surveyId)
        while instances:
            for instance in instances:
                submitter = instance['submitterName']
                waarnemer,created = Waarnemer.objects.get_or_create(akvoname=submitter,defaults={'achternaam':submitter})
                if created:
                    logger.info('Waarnemer {name} aangemaakt'.format(name=submitter))
                
                #find related registration form (meetpunt)
                localeId = instance['surveyedLocaleIdentifier']
                try:
                    meetpunt = Meetpunt.objects.get(identifier=localeId)
                except Meetpunt.DoesNotExist:
                    logger.error('Meetpunt {locatie} niet gevonden'.format(locatie=localeId))
                    continue
                
                device = instance['deviceIdentifier']
                date=instance['collectionDate']
                date=datetime.datetime.utcfromtimestamp(date/1000.0).replace(tzinfo=pytz.utc)

                answers = api.get_answers(instance['keyId'])
                ec=api.get_answer(answers,questionID='2060924')
                diep=api.get_answer(answers,questionID='7080929')
                foto=api.get_answer(answers,questionID='5040929')

                waarnemingen = meetpunt.waarneming_set.filter(naam='EC_'+diep,datum=date)
                if waarnemingen.exists():
                    logger.warning('EC waarnemingen worden vervangen voor {locatie}, datum={date}'.format(locatie=meetpunt.name,date=date)) 
                    waarnemingen.delete()
                meetpunt.waarneming_set.create(naam='EC_'+diep, waarnemer=waarnemer, datum=date, waarde=ec, device=device, foto_url=foto, opmerking='', eenheid='uS/cm' )
                logger.debug('EC_{diep}, {date}, EC={ec}'.format(diep=diep, date=date, ec=ec))
                meetpunten.add(meetpunt)

            instances,meta = api.get_survey_instances(surveyId=surveyId, since=meta['since'])
    return meetpunten

def updateSeries(mps, user):    
    '''update timeseries using meetpunten from  mps'''
    allseries = set()
    for mp in mps:
        loc = mp.projectlocatie
        for w in mp.waarneming_set.all():
            series, created = mp.manualseries_set.get_or_create(name=w.naam,defaults={'user': user, 'type': 'line', 'unit': 'uS/cm'})
            if created:
                logger.info('Tijdreeks {name} aangemaakt voor meetpunt {locatie}'.format(name=series.name,locatie=mp.name))  
            dp, created = series.datapoints.get_or_create(date=w.datum, defaults={'value': w.waarde})
            if not created:
                if dp.value != w.waarde:
                    dp.value=w.waarde
                    dp.save(update_fields=['value'])
            logger.debug('{name}, {date}, EC={ec}'.format(name=series, date=dp.date, ec=dp.value))
            allseries.add(series)

    logger.info('Thumbnails tijdreeksen aanpassen')
    for series in allseries:
        series.getproperties().update()
        series.make_thumbnail()

    logger.info('Grafieken aanpassen')
    for mp in mps:
        util.maak_meetpunt_grafiek(mp, user)
        
def updateCartodb(cartodb, mps):
    #cartodb.runsql('DELETE FROM waarnemingen')
    for m in mps:
        p = m.location
        p.transform(4326)
        
        waarnemingen = m.waarneming_set.all().order_by('-datum')
        if waarnemingen.exists():
            last = waarnemingen[0]
            ec = last.waarde
            date = last.datum
            diep = "'ondiep'" if last.naam.endswith('ndiep') else "'diep'"
        else:
            ec = None
            date = None
            diep = ''
#         series = m.get_series('EC')
#         ec = None if series is None else series.laatste()
        if ec is None or date is None:
            date = 'NULL'
            ec = 'NULL'
        else:
            date = time.mktime(date.timetuple())

        url = m.chart_thumbnail.name
        url = 'NULL' if url is None else "'{url}'".format(url=url)
        s = "(ST_SetSRID(ST_Point({x},{y}),4326), {diep}, {charturl}, '{sampleid}', '{waarnemer}', to_timestamp({date}), {ec})".format(x=p.x,y=p.y,diep=diep,charturl=url,sampleid=m.name,waarnemer=unicode(m.waarnemer),ec=ec,date=date)
        values = 'VALUES ' + s
        
        sql = "DELETE FROM waarnemingen WHERE waarnemer='{waarnemer}' AND sampleid='{sampleid}'".format(waarnemer=m.waarnemer.id, sampleid=m.name)
        cartodb.runsql(sql)

        sql = 'INSERT INTO waarnemingen (the_geom,diepondiep,charturl,sampleid,waarnemer,datum,ec) ' + values
        cartodb.runsql(sql)
    
class Command(BaseCommand):
    args = ''
    help = 'Importeer metingen vanuit akvo flow'
    option_list = BaseCommand.option_list + (
            make_option('--akvo',
                action='store',
                dest = 'akvo',
                default = 1,
                help = 'id van Akvoflow configuratie'),
            make_option('--cartodb',
                action='store',
                dest = 'cartodb',
                default = 1,
                help = 'id van Cartodb configuratie'),
            make_option('--project',
                action='store',
                dest = 'proj',
                default = 1,
                help = 'id van project locatie'),
            make_option('--user',
                action='store',
                dest = 'user',
                default = 'akvo',
                help = 'user name'),
        )

    def handle(self, *args, **options):
        
        akvo = AkvoFlow.objects.get(pk=options.get('akvo'))
        api = FlowAPI(instance=akvo.instance, key=akvo.key, secret=akvo.secret)
        cartodb = CartoDb.objects.get(pk=options.get('cartodb'))
    
        project = ProjectLocatie.objects.get(pk=options.get('proj'))
        user = User.objects.get(username=options.get('user'))

        try:
            logger.info('Meetpuntgegevens ophalen')
            mp = importAkvoRegistration(api, akvo.regform, projectlocatie=project,user=user)
        
            logger.info('Waarnemingen ophalen')
            surveys = [f.strip() for f in akvo.monforms.split(',')]
            mp.update(importAkvoMonitoring(api, surveys))
            
            logger.info('Grafieken aanpassen')
            updateSeries(mp, user)

            logger.info('Cartodb actialiseren')
            updateCartodb(cartodb, mp)        
        except Exception as e:
            logger.exception('Probleem met verwerken nieuwe EC metingen: %s',e)

