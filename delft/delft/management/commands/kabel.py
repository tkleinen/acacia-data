'''
Created on Dec 6, 2014

@author: theo
'''
import os, csv, re, datetime, binascii
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from acacia.meetnet.models import Datalogger, LoggerDatasource
from acacia.data.models import Series, DataPoint
from acacia.meetnet.models import Well,Screen
from django.contrib.auth.models import User
import math
import pytz

class Command(BaseCommand):
    args = ''
    help = 'Importeer kabellengtes'
    option_list = BaseCommand.option_list + (
            make_option('--file',
                action='store',
                type = 'string',
                dest = 'fname',
                default = None),
        )
        
    def handle(self, *args, **options):
        fname = options.get('fname')
        CET=pytz.timezone('CET')
        if fname:
            with open(fname,'r') as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    NITG = row['nitg']
                    try:
                        well = Well.objects.get(name=NITG)
                        filt = int(row['filter'])
                        screen = well.screen_set.get(nr=filt)
                        datumtijd = '%s %s' % (row['datum'], row['tijd'])
                        depth = row.get('kabellengte')
                        if len(depth) > 0:
                            depth = float(depth)
                        else:
                            depth = 0
                        date = datetime.datetime.strptime(datumtijd,'%Y-%m-%d %H:%M:%S')
                        date = date.replace(tzinfo=CET)
                        date = date.date()

                        for lp in screen.loggerpos_set.all():
                            start = lp.start_date.date()
                            if (abs(start - date).days < 2) or (date.year == 2013 and start.year == 2013): 
                                lp.depth = depth
                                lp.save()
                                    
                    except Well.DoesNotExist:
                        print 'Well %s not found' % NITG
                    except Screen.DoesNotExist:
                        print 'Screen %s/%03d not found' % (NITG, filt)
                        