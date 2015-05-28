'''
Created on Dec 6, 2014

@author: theo
'''
import os, csv, re, datetime, binascii
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from gorinchem.models import Network, Well, Screen, Datalogger, LoggerDatasource
from gorinchem import settings
from django.contrib.gis.geos import Point
from acacia.data.models import Project, ProjectLocatie, MeetLocatie, Datasource, Generator, SourceFile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def find_files(pattern, root=os.curdir):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

class Command(BaseCommand):
    args = ''
    help = 'Importeer mon files'
    option_list = BaseCommand.option_list + (
            make_option('--folder',
                action='store',
                type = 'string',
                dest = 'folder',
                default = '.'),
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
                
                