'''
Created on Sep 4, 2015

@author: theo
'''

import os,math,time,logging
from django.utils.text import slugify
from django.conf import settings
from iom.models import Meetpunt
from acacia.data.models import Chart

logger = logging.getLogger(__name__)
def distance(obj, pnt):
    dx = obj.location.x - pnt.x
    dy = obj.location.y - pnt.y
    return math.sqrt(dx*dx+dy*dy)

def closest_object(query,target):
    closest = None
    dist = 1e99
    for obj in query:
        d = distance(obj, target)
        if d < dist:
            closest = obj
            dist = d
    return closest

def sort_objects(query,target):
    objs = []
    for obj in query:
        obj.distance = distance(obj, target)
        objs.append(obj)
    return sorted(objs, key=lambda x: x.distance)

def zoek_meetpunten(target, tolerance=1.0):
    mps = sort_objects(Meetpunt.objects.all(), target)
    return [m for m in mps if m.distance < tolerance]

def zoek_tijdreeksen(target,tolerance=1.0):
    ''' haal alle tijdreeksen op rond een locatie '''
    mps = zoek_meetpunten(target, tolerance)
    series = []
    for mp in mps:
        series.extend(mp.series())
    return series

import matplotlib.pyplot as plt
import pandas as pd

def maak_meetpunt_thumbnail(meetpunt):
    
    imagefile = os.path.join(meetpunt.chart_thumbnail.field.upload_to,slugify(unicode(meetpunt.identifier))+'.png')
    imagepath = os.path.join(settings.MEDIA_ROOT,imagefile)
    imagedir = os.path.dirname(imagepath)
    if not os.path.exists(imagedir):
        os.makedirs(imagedir)
    
    meetpunt.chart_thumbnail.name = imagefile
    
    plt.figure(figsize=(9,3))
    options = {'grid': False, 'legend': True, 'title': 'Meetpunt {num}'.format(num=meetpunt)}

    mps = zoek_meetpunten(meetpunt.location, 1)
    for mp in mps:
        s = mp.get_series('EC')
        if s:
            s =s.to_pandas()
            s.name = 'ondiep' if s.name.endswith('o') else 'diep'
            ax=s.plot(**options)
            ax.set_ylabel('EC')
    plt.savefig(imagepath)
    
    plt.close()
    
    meetpunt.save()

def maak_meetpunt_grafiek(meetpunt,user):
    try:
        chart = meetpunt.chart
    except Exception as e:
        chart = None

    if chart is None:
        name = unicode(meetpunt)
        chart, created = Chart.objects.get_or_create(name = name, defaults = {
                                                             'user': user, 
                                                             'title': name, 
                                                             'description': unicode(meetpunt.description)})
        meetpunt.chart=chart
        meetpunt.save()
                                                             
    series = zoek_tijdreeksen(meetpunt.location,1)
    for s in series:
        pos, ax = ('l', 1) if s.name.startswith('EC') else ('r', 2)
        cs, created = chart.series.get_or_create(series=s, defaults={'name': s.name, 'axis': ax, 'axislr': pos, 'type': s.type})
    chart.save()
    
    maak_meetpunt_thumbnail(meetpunt)
    
    
def updateSeries(mps, user):    
    '''update timeseries using meetpunten from  mps'''
    allseries = set()
    for mp in mps:
        loc = mp.projectlocatie
        for w in mp.waarneming_set.all():
            series, created = mp.manualseries_set.get_or_create(name=w.naam,defaults={'user': user, 'type': 'line', 'unit': 'uS/cm'})
            if created:
                logger.info('Tijdreeks {name} aangemaakt voor meetpunt {locatie}'.format(name=series.name,locatie=mp.displayname))  
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
        maak_meetpunt_grafiek(mp, user)


def maak_naam(parameter,diep):
    if diep and not diep.endswith('iep'):
        diep = None
    return parameter + '_' + diep if diep else parameter
        
def updateCartodb(cartodb, mps):
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
        if ec is None or date is None:
            date = 'NULL'
            ec = 'NULL'
        else:
            date = time.mktime(date.timetuple())

        url = m.chart_thumbnail.name
        url = 'NULL' if url is None else "'{url}'".format(url=url)
        s = "(ST_SetSRID(ST_Point({x},{y}),4326), {diep}, {charturl}, '{meetpunt}', '{waarnemer}', to_timestamp({date}), {ec})".format(x=p.x,y=p.y,diep=diep,charturl=url,meetpunt=m.name,waarnemer=unicode(m.waarnemer),ec=ec,date=date)
        values = 'VALUES ' + s
        
        sql = "DELETE FROM waarnemingen WHERE waarnemer='{waarnemer}' AND meetpunt='{meetpunt}'".format(waarnemer=unicode(m.waarnemer), meetpunt=m.name)
        cartodb.runsql(sql)

        sql = 'INSERT INTO waarnemingen (the_geom,diepondiep,charturl,meetpunt,waarnemer,datum,ec) ' + values
        cartodb.runsql(sql)

def exportCartodb(cartodb, mps, table):

    for m in mps:
        print m
        p = m.location
        p.transform(4326)
        waarnemingen = m.waarneming_set.all().order_by('datum')
        values = ''
        for w in waarnemingen:
            ec = w.waarde
            date = w.datum
            if w.naam.find('_'):
                words = w.naam.split('_')
                diep = "'"+words[-1]+"'"
            else:
                diep = 'NULL'
            
            date = time.mktime(date.timetuple())
            url = m.chart_thumbnail.name
            url = 'NULL' if url is None else "'{url}'".format(url=url)
            s = "(ST_SetSRID(ST_Point({x},{y}),4326), {diep}, {charturl}, '{meetpunt}', '{waarnemer}', to_timestamp({date}), {ec})".format(x=p.x,y=p.y,diep=diep,charturl=url,meetpunt=m.name,waarnemer=unicode(m.waarnemer),ec=ec,date=date)
            if values:
                values += ','
            values += s
            
        if values:
            sql = "DELETE FROM {table} WHERE waarnemer='{waarnemer}' AND meetpunt='{meetpunt}'".format(table=table, waarnemer=unicode(m.waarnemer), meetpunt=m.name)
            cartodb.runsql(sql)
            sql = 'INSERT INTO {table} (the_geom,diepondiep,charturl,meetpunt,waarnemer,datum,ec) VALUES '.format(table=table) + values
            cartodb.runsql(sql)
        

