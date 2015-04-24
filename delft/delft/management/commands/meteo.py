'''
Created on Dec 6, 2014

@author: theo
'''
import os, csv, re, datetime, binascii
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from acacia.meetnet.models import Datalogger, LoggerDatasource
from acacia.data.models import Formula, Variable, MeetLocatie, Project

from acacia.data.knmi.models import NeerslagStation, Station
from acacia.data.models import Datasource, Generator
from django.contrib.auth.models import User

import math
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

def luchtdruk(loc,user):
    ''' Luchtdruk stations toevoegen aan project '''
    
    project = loc.project()
    p = loc.location
    
    stns = sort_objects(Station.objects.all(),p)
    stn = stns[0] # closest
    name='Meteostation %s ' % stn.naam
    ploc, created = project.projectlocatie_set.get_or_create(name=name,defaults={'location':stn.location})
    mloc, created = ploc.meetlocatie_set.get_or_create(name=name,defaults={'location':stn.location})
    try:
        df = mloc.datasources.get(name=name)
    except Datasource.DoesNotExist:
        print name
        df = Datasource(name=name,meetlocatie = mloc,user = user, generator = Generator.objects.get(name='KNMI Uurgegevens'))
        generator = df.get_generator_instance()
        df.url = generator.url + '?stns=%d&start=2014010101' % stn.nummer
        df.save()
        df.download()
        df.update_parameters()
        
class Command(BaseCommand):
    args = ''
    help = 'KNMI luchtdruk stations toevoegen aan project'
        
    def handle(self, *args, **options):
        project = Project.objects.get(name = 'Delft')
        user = User.objects.get(username='theo')
        for pl in project.projectlocatie_set.all():
            for ml in pl.meetlocatie_set.all():
                luchtdruk(ml,user) 