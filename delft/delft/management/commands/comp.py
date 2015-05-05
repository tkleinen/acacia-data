'''
Created on Dec 6, 2014

@author: theo
'''
from django.core.management.base import BaseCommand
from acacia.data.models import Series, DataPoint, Chart, MeetLocatie
from acacia.meetnet.models import Well,Screen
from django.contrib.auth.models import User
from django.db.models import F

import math, pytz, datetime

class Command(BaseCommand):
    args = ''
    help = 'Maak luchtdruk gecompenseerde reeksen'
        
    def handle(self, *args, **options):
        user = User.objects.get(username='theo')
        known_baros = {}
        tz = pytz.FixedOffset(60)#Nederlandse wintertijd
        #for well in Well.objects.all():
        for well in Well.objects.exclude(name=F('nitg')):
            for screen in well.screen_set.all():
                print screen
                name = '%s COMP' % screen
                series, created = Series.objects.get_or_create(name=name,user=user)
                series.unit = 'm tov NAP'
                seriesdata = None
                for logpos in screen.loggerpos_set.all().order_by('start_date'):
                    if seriesdata is  None:
                        meteo = logpos.baro.meetlocatie().name
                        series.description = 'Gecompenseerd voor luchtdruk van %s' % meteo
                        print '  Luchtdruk:', meteo
                    if logpos.baro in known_baros:
                        baro = known_baros[logpos.baro]
                    else:
                        baro = logpos.baro.to_pandas() / 9.80638 # 0.1 hPa naar cm H2O
                        baro = baro.tz_convert(tz)
                        known_baros[logpos.baro] = baro
                    for mon in logpos.monfile_set.all().order_by('start_date'):
                        print ' ', logpos.logger, mon
                        data = mon.get_data()['PRESSURE']
                        data = series.do_postprocess(data).tz_localize(tz)
                        data = data - baro
                        data.dropna(inplace=True)
                        data = data / 100 + (logpos.refpnt - logpos.depth)
                        if seriesdata is None:
                            seriesdata = data
                        else:
                            seriesdata = seriesdata.append(data)
                            
                if seriesdata is not None:
                    seriesdata = seriesdata.groupby(level=0).last()
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
                
                #maak/update grafiek
                chart, created = Chart.objects.get_or_create(name=unicode(screen), defaults={
                            'title': unicode(screen),
                            'user': user, 
                            'percount': 0, 
                            'start':datetime.datetime(2014,1,1), 
                            'stop': datetime.datetime(2015,1,1),
                            })
                chart.series.get_or_create(series=series, defaults={'label' : 'm tov NAP'})
                # handpeilingen toevoegen (als beschikbaar)
                try:
                    mloc = MeetLocatie.objects.get(name=unicode(screen))
                    for hand in mloc.manualseries_set.all():
                        chart.series.get_or_create(series=hand,defaults={'type':'scatter', 'order': 2})
                except:
                    pass