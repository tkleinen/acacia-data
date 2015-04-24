'''
Created on Dec 6, 2014

@author: theo
'''
import os, csv, re, datetime, binascii
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from acacia.meetnet.models import Datalogger, LoggerDatasource
from acacia.data.models import Formula, Variable

class Command(BaseCommand):
    args = ''
    help = 'Maak berekende reeksen voor compensatie'
        
    def handle(self, *args, **options):
        for ds in LoggerDatasource.objects.all():
            meetlocatie = ds.meetlocatie
            logger = ds.logger
            screen = logger.screen
            try:
                baro = logger.baro
                barolocatie = baro.meetlocatie()
            except:
                baro = None
            if baro is None:
                print 'Geen barometer gedefinieerd voor logger %s in peilbuis %s' % (logger, logger.screen)
                continue
        
            f, created = Formula.objects.get_or_create(name='LEVEL',locatie=meetlocatie,user=ds.user)
            if created:
                # get 1st series for parameter PRESSURE
                parameter = ds.parameter_set.get(name='PRESSURE')
                pressure = parameter.series_set.first()
                varp, created = Variable.objects.get_or_create(name='PRESSURE',locatie=meetlocatie,series=pressure)
                varb, created = Variable.objects.get_or_create(name='baro',locatie=barolocatie,series=baro)
                f.formula_text = 'PRESSURE - baro'
                f.formula_variables.add(varp)
                f.formula_variables.add(varb)
                f.save()
