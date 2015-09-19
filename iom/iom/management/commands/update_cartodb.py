'''
Created on Feb 13, 2014

@author: theo
'''
from django.core.management.base import BaseCommand
from optparse import make_option
from iom.models import Meetpunt 
import urllib,urllib2
import time

class Command(BaseCommand):
    args = ''
    help = 'Updates data in cartodb'
    option_list = BaseCommand.option_list + (
            make_option('--pk',
                action='store',
                type = 'int',
                dest = 'pk',
                default = None,
                help = 'update single meetpunt'),
        )
    url = 'https://tkleinen.cartodb.com/api/v2/sql'
    key = '6c962290788f1addce759c808ad7593f61524d90'
        
    def handle(self, *args, **options):
        values = None
        for m in Meetpunt.objects.all():
            p = m.location
            p.transform(4326)
            series = m.get_series('EC')
            ec = None if series is None else series.laatste()
            series = m.get_series('Temp')
            temp = None if series is None else series.laatste()
            if ec is None:
                date = 'NULL'
                ec = 'NULL'
            else:
                date = time.mktime(ec.date.timetuple())
                ec = ec.value
            temp = 'NULL' if temp is None else temp.value
            s = '(ST_SetSRID(ST_Point({x},{y}),4326), {sampleid}, {waarnemer}, to_timestamp({date}), {ec}, {temp})'.format(x=p.x,y=p.y,sampleid=m.nummer,waarnemer=m.waarnemer.id,ec=ec,temp=temp,date=date)
            if values is None:
                values = 'VALUES ' + s
            else:
                values += ',' + s
        values += ';'
        sql = 'INSERT INTO waarnemers_1 (the_geom,sampleid,waarnemer,datum,ec,temperatuur) ' + values
        data = urllib.urlencode({'q': sql, 'api_key': self.key})
        request = urllib2.Request(url=self.url, data=data)
        response = urllib2.urlopen(request)
        print response.read()
        