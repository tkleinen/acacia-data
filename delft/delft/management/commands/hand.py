'''
Created on Dec 6, 2014

@author: theo
'''
import csv, datetime
from optparse import make_option
from django.core.management.base import BaseCommand
from acacia.data.models import ProjectLocatie, MeetLocatie
from acacia.meetnet.models import Well,Screen
from django.contrib.auth.models import User
import pytz

class Command(BaseCommand):
    args = ''
    help = 'Importeer hndpeilingen'
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
        user=User.objects.get(username='theo')
        if fname:
            with open(fname,'r') as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    NITG = row['NITG']
                    try:
                        well = Well.objects.get(name=NITG)
                        filt = int(row['Filter'])
                        screen = well.screen_set.get(nr=filt)
                        ploc = ProjectLocatie.objects.get(name=well.name)
                        mloc = ploc.meetlocatie_set.get(name=unicode(screen))
                        datumtijd = '%s %s' % (row['Datum'], row['Wintertijd'])
                        depth = row.get('Meting')
                        if len(depth) > 0:
                            depth = float(depth)
                        else:
                            depth = 0
                        nap = screen.refpnt - depth
                        date = datetime.datetime.strptime(datumtijd,'%d/%m/%Y %H:%M:%S')
                        date = date.replace(tzinfo=CET)
                        series, created = mloc.manualseries_set.get_or_create(name='%s HAND' % mloc.name, defaults = {'description': 'Handpeiling', 'unit': 'm NAP', 'type': 'scatter', 'user': user})
                        pt, created = series.datapoints.get_or_create(date=date,defaults={'value': nap})
                        if not created:
                            pt.value = nap
                            pt.save()
                        print screen, pt.date, pt.value
                    except Well.DoesNotExist:
                        print 'Well %s not found' % NITG
                    except Screen.DoesNotExist:
                        print 'Screen %s/%03d not found' % (NITG, filt)
                    except MeetLocatie.DoesNotExist:
                        print 'Meetlocatie %s/%03d not found' % (NITG, filt)
                    except Exception as e:
                        print e
                        