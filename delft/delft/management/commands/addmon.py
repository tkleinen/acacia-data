'''
Created on Dec 6, 2014

@author: theo
'''
import os, re, binascii, zipfile
from optparse import make_option
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from acacia.meetnet.models import Well, Screen, Datalogger, LoggerDatasource, LoggerPos
from acacia.data.models import SourceFile, Generator, MeetLocatie
from django.contrib.auth.models import User

import monfile, StringIO

class Command(BaseCommand):
    args = ''
    help = 'Importeer mon files'
    option_list = BaseCommand.option_list + (
            make_option('--zip',
                action='store',
                type = 'string',
                dest = 'zip'),
        )

    def handle(self, *args, **options):
        
        user = User.objects.get(username='theo')
        generator = Generator.objects.get(name='Schlumberger')
        
        zip = options.get('zip')
        if zip:
            with zipfile.ZipFile(zip,'r') as z:
                count = 0
                for info in z.infolist():
                    if info.filename.endswith('.MON'):
                        name = re.split(r'[_\.\/]',info.filename)
                        if name[0].startswith('MON'):
                            try:
                                put, filter = name[1].split('-')
                            except:
                                continue
                            try:
                                try:
                                    well = Well.objects.get(nitg=put)
                                except Well.DoesNotExist:
                                    well = Well.objects.get(name=put)
                                screen = well.screen_set.get(nr=int(filter))
                                with z.open(info.filename, 'r') as f:
                                    contents = f.read() 
                                    io = StringIO.StringIO(contents)
                                    mon, channels = monfile.create(io)
                                    serial = mon.serial_number
                                    logger, created = Datalogger.objects.get_or_create(serial=serial,defaults={'model': mon.instrument_type})
                                    pos, created = logger.loggerpos_set.get_or_create(screen=screen,start_date=mon.start_date,end_date=mon.end_date,refpnt=screen.refpnt)
                                    
                                    # get meetlocatie
                                    loc = MeetLocatie.objects.get(name=unicode(screen))
                                    
                                    # get/create datasource for logger
                                    ds, created = LoggerDatasource.objects.get_or_create(name=logger.serial,meetlocatie=loc,
                                                                                         defaults = {'logger': logger, 'generator': generator, 'user': user, 'timezone': 'CET'})
                                    
                                    mon.crc = abs(binascii.crc32(contents))
                                    try:
                                        ds.sourcefiles.get(crc=mon.crc)
                                    except SourceFile.DoesNotExist:
                                        # add source file
                                        filename = os.path.basename(info.filename)
                                        mon.name = mon.filename = filename
                                        mon.datasource = ds
                                        mon.user = ds.user
                                        contentfile = ContentFile(contents)
                                        mon.file.save(name=filename, content=contentfile)
                                        mon.get_dimensions()
                                        mon.save()
                                        mon.channel_set.add(*channels)
                                        pos.monfile_set.add(mon)

                                        print screen, serial, mon.num_points, mon.start_date, mon.end_date
                                        count += 1
                            except Well.DoesNotExist:
                                continue
                            except Screen.DoesNotExist:
                                #print 'screen not found:', well.name, filter
                                continue
                            except Exception as e:
                                print e
                                
                print count, '.MON bestanden toegevoegd'
