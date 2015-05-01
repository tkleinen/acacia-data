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
            make_option('--folder',
                action='store',
                type = 'string',
                dest = 'folder',
                default = '.'),
            make_option('--zip',
                action='store',
                type = 'string',
                dest = 'zip'),
        )

    def add_file(self, ds, pathname):
        with open(pathname) as f:
            contents = f.read()
        filename = os.path.basename(pathname)
        crc = abs(binascii.crc32(contents))
        try:
            sourcefile = ds.sourcefiles.get(name=filename)
        except SourceFile.DoesNotExist:
            sourcefile = SourceFile(name=filename,datasource=ds,user=ds.user)
        sourcefile.crc = crc
        contentfile = ContentFile(contents)
        sourcefile.file.save(name=filename, content=contentfile)
        sourcefile.save()
        
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
                                well = Well.objects.get(name=put)
                                screen = well.screen_set.get(nr=int(filter))
                                with z.open(info.filename, 'r') as f:
                                    contents = f.read() 
                                    io = StringIO.StringIO(contents)
                                    mon, channels = monfile.create(io)
                                    serial = mon.serial_number
                                    logger, created = Datalogger.objects.get_or_create(serial=serial,defaults={'model': mon.instrument_type})
                                    pos = logger.loggerpos_set.create(screen=screen,start_date=mon.start_date,end_date=mon.end_date,refpnt=screen.refpnt)
                                    
                                    # get meetlocatie
                                    loc = MeetLocatie.objects.get(name=unicode(screen))
                                    
                                    # get/create datasource for logger
                                    ds, created = LoggerDatasource.objects.get_or_create(name=logger.serial,meetlocatie=loc,
                                                                                         defaults = {'logger': logger, 'generator': generator, 'user': user, 'timezone': 'CET'})
                                    
                                    # add source file
                                    filename = os.path.basename(info.filename)
                                    mon.name = mon.filename = filename
                                    mon.datasource = ds
                                    mon.user = ds.user
                                    mon.crc = abs(binascii.crc32(contents))
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
                                continue
                            except Exception as e:
                                print e
                                
                print count, '.MON bestanden toegevoegd'
        else:
            folder = options.get('folder')
            for path, dirs, filenames in os.walk(folder):
                for fname in filenames:
                    #fname = 'g-pb15_141103114201_S2850.MON'
                    put,date,serial = fname.split('_')
                    serial = serial.split('.')[0]
                    try:
                        logger = Datalogger.objects.get(serial = serial)
                    except Datalogger.DoesNotExist:
                        print 'Datalogger %s is niet geregistreerd' % logger
                        continue
                    try:
                        ds = LoggerDatasource.objects.get(logger = logger)
                        print '%s -> %s' % (ds, logger.screen)
                    except LoggerDatasource.DoesNotExist:
                        print 'Geen datasource voor logger %s gedefinieerd' % logger
                        continue
                    self.add_file(ds, os.path.join(path,fname))
                
                