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
from acacia.meetnet.models import Screen
from django.contrib.auth.models import User
import math

class Command(BaseCommand):
    args = ''
    help = 'Maak luchtdruk gecompenseerde reeksen'
        
    def handle(self, *args, **options):
        user = User.objects.get(username='theo')
        known_baros = {}
        for screen in Screen.objects.all():
            print screen
            name = '%s COMPENSATED' % screen
            series, created = Series.objects.get_or_create(name=name,user=user)
            seriesdata = None
            for logpos in screen.loggerpos_set.all().order_by('start_date'):
                if seriesdata is  None:
                    print ' ', logpos.baro
                if logpos.baro in known_baros:
                    baro = known_baros[logpos.baro]
                else:
                    baro = logpos.baro.to_pandas() / 9.80638
                    known_baros[logpos.baro] = baro
                for mon in logpos.monfile_set.all().order_by('start_date'):
                    print ' ', mon
                    data = mon.get_data()['PRESSURE']
                    data = series.do_postprocess(data)
                    data = data.tz_localize('CET') # Nederlandse wintertijd
                    start = data.index.min()
                    stop = data.index.max()
                    data = data - baro
                    data = data[start:stop]
                    if seriesdata is None:
                        seriesdata = data
                    else:
                        seriesdata = seriesdata.append(data)
                        
            if seriesdata is not None:
                seriesdata.sort(inplace=True)
                datapoints=[]
                for date,value in seriesdata.iteritems():
                    value = float(value)
                    if math.isnan(value) or date is None:
                        continue
                    datapoints.append(DataPoint(series=series, date=date, value=value))
                series.datapoints.all().delete()
                series.datapoints.bulk_create(datapoints)
                series.make_thumbnail()
                series.save()
                #self.getproperties()#.update()
