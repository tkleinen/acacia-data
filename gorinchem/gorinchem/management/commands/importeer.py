'''
Created on Feb 13, 2014

@author: theo
'''
import os, csv, datetime
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from gorinchem.models import Network, Well, Screen, DataPoint
from gorinchem import settings
from gorinchem.dino import Dino
from django.contrib.gis.geos import Point

class Command(BaseCommand):
    args = ''
    help = 'Importeer csv bestanden'
    option_list = BaseCommand.option_list + (
            make_option('--put',
                action='store',
                type = 'string',
                dest = 'put',
                default = None),
            make_option('--filter',
                action='store',
                type = 'string',
                dest = 'filter',
                default = None),
            make_option('--overzicht',
                action='store',
                type = 'string',
                dest = 'overzicht',
                default = None),
            make_option('--dino',
                action='store',
                type = 'string',
                dest = 'dino',
                default = None),
        )

    def handle(self, *args, **options):
        
        fname = options.get('put')
        if fname:
            with open(fname,'r') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    well = Well(name=row['Code'], location = Point(y=float(row['X']),x=float(row['Y'])), 
                                maaiveld=0, 
                                date=datetime.datetime.strptime(row['Gewijzigd'], '%d-%m-%y %H:%M:%S'))
                    well.save()
                    print well

        fname = options.get('filter')
        if fname:
            with open(fname,'r') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    well = Well.objects.get(name=row['Meetpunt'])
                    screen = well.screen_set.create(nr=int(row['Naam']), 
                                           top=float(row['Van']),
                                           bottom=float(row['Tot']),
                                           diameter=float(row['Diameter']),
                                           material=row['Materiaal'].lower())
                    print screen

        fname = options.get('overzicht')
        if fname:
            with open(fname,'r') as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    well = Well.objects.get(name=row['Code'])
                    well.date=datetime.datetime.strptime(row['Datum'], '%m/%d/%Y')
                    well.location = Point(y=float(row['X']),x=float(row['Y']))
                    well.maaiveld = float(row['Z (MV)'])
                    well.refpnt = float(row['Z (PB)'])
                    well.save()
                    
                    screen,created = well.screen_set.get_or_create(nr=1)
                    screen.top=float(row['Van'])
                    screen.bottom=float(row['Tot'])
                    screen.diameter=float(row['Diameter'])
                    screen.material=row['Materiaal'].lower()
                    screen.save()
                    
                    diver,created = screen.datalogger_set.get_or_create(serial=row['Diver'], defaults = {
                        'model' : row['Type'].lower(),
                        'refpnt' : well.refpnt,
                        'depth' : float(row['Diver (cm-pb)']) / 100.0,
                        'date' : datetime.datetime(2014,5,1,13,0),
                    })
                    diver.save()
        fname = options.get('dino')
        if fname:
            dino=Dino()
            Network.objects.filter(name='Dino').delete()
            network,created = Network.objects.get_or_create(name='Dino')
            count = 0
            for f,d in dino.iter_zip(fname): #'/media/sf_C_DRIVE/projdirs/Gorinchem/dino/1626d423-0d17-499f-b97b-b0ef48fb542f.zip'):
                count += 1
                if count > 20:
                    break
                try:
                    name = d['Locatie']
                    nr = int(d['Filternummer'])
                    datum = datetime.datetime.strptime(d['Datum maaiveld gemeten'],'%d-%m-%Y')
                    x = float(d['X-coordinaat'])
                    y = float(d['Y-coordinaat'])
                    loc = Point(x,y)
                    maaiveld = float(d['Maaiveld (cm t.o.v. NAP)']) / 100
                    refpnt = float(d['Meetpunt (cm t.o.v. NAP)']) / 100
                    well,created = Well.objects.get_or_create(nitg=name, defaults = {'network': network,
                                                                                     'name': name,
                                                                                     'location': loc,
                                                                                     'maaiveld': maaiveld,
                                                                                     'refpnt': refpnt,
                                                                                     'date': datum,
                                                                                     })
                    top = float(d['Bovenkant filter (cm t.o.v. NAP)']) / 100
                    bottom = float(d['Onderkant filter (cm t.o.v. NAP)']) / 100
                    filter,newfilter = well.screen_set.get_or_create(nr=nr, defaults = {'top': top, 'bottom': bottom})
                    print filter
                    if filter.num_standen() == 0:
                        for s in d['standen']:
                            try:
                                date = s[2]
                                value = s[5]
                                if len(date)>0 and len(value)>0:
                                    peildatum = datetime.datetime.strptime(date+' 12:00:00','%d-%m-%Y %H:%M:%S')
                                    standnap = float(value) / 100
                                    if newfilter:
                                        filter.datapoint_set.create(date=peildatum,level=standnap)
                                    else:
                                        filter.datapoint_set.get_or_create(date=peildatum,defaults={'level': standnap})
                            except Exception as e:
                                print name, nr, e
                except Exception as e:
                    print name, nr, e