'''
Created on Dec 6, 2014

@author: theo
'''
from django.core.management.base import BaseCommand
from acacia.data.models import Series
from delft.models import ManualSeries
import pandas as pd

class Command(BaseCommand):
    args = ''
    help = 'Vergelijk standen en handpeilingen'
                        
    def handle(self, *args, **options):
        print 'filter,tijdstip,stand,handpeiling'
        for h in ManualSeries.objects.all():
            hand = pd.DataFrame(h.to_pandas())
            mloc = h.meetlocatie()
            try:
                name = '%s COMP' % mloc.name
                ser = Series.objects.get(name = name)
            except Series.DoesNotExist:
                print 'Series', name, 'not found' 
            data = pd.DataFrame(ser.to_pandas())
            inter = pd.concat([data, hand]).sort_index().interpolate(method='time').groupby(level=0).mean()
            for p in h.datapoints.all().order_by('date'):
                row = inter.loc[p.date]
                print mloc.name,',',p.date,',',row.values[0],',',row.values[1]
                
