'''
Created on Jan 29, 2013

@author: theo
'''
import zipfile,os,fnmatch
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def find_files(pattern, root=os.curdir):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

class Dino():

    def skip_section(self,f):
        while True:
            line=f.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                break
        
    def read_header(self,f):
        line = f.readline()
        while line:
            line = line.strip()
            if line:
                return line.split(',')
            line = f.readline()
        return None

    def read_well(self,f):
        keys = self.read_header(f)
        data = []
        line = f.readline()
        while line:
            line = line.strip()
            if line:
                values =line.split(',')
                data = dict(zip(keys,values))
                line = f.readline()
        return data
        
    def read_standen(self,f):
        header = self.read_header(f)
        data = []
        line = f.readline()
        while line:
            line = line.strip()
            if line:
                tokens=line.split(',')
                locatie = tokens[0]
                filternummer = tokens[1]
                peildatum = tokens[2]
                stand_mp= tokens[3]
                stand_mv= tokens[4]
                stand_nap= tokens[5]
                data.append((locatie,filternummer,peildatum,stand_mp,stand_mv,stand_nap))
            line = f.readline()
        return data
    
    def read_file(self,f):
        self.skip_section(f)
        self.skip_section(f)
        try:
            well=self.read_well(f)
            well['standen']=self.read_standen(f)
            return well
        except Exception as e:
            logger.error('cant load file: ' + e)
            return None
    
    def iter_folder(self,folder):
        for name in find_files('*_1.csv', folder):
            try:
                with open(name,'r') as f:
                    data = self.read_file(f)
                    yield (name, data)
            except Exception as e:
                print 'ERROR in ', name, e
    
    def iter_zip(self, filename):
        with zipfile.ZipFile(filename,'r') as z:
            for info in z.infolist():
                if info.filename.endswith('_1.csv'):
                    try:
                        with z.open(info.filename,'r') as f:
                            data = self.read_file(f)
                            yield (info.filename, data)
                    except Exception as e:
                        print 'ERROR in ', info.filename, e

#from models import Well, Screen
from django.contrib.gis.geos import Point                         
import datetime


if (__name__ == '__main__'):
    'Import DINDOLOKET data'
    dino=Dino()
    for f,d in dino.iter_zip('/media/sf_C_DRIVE/projdirs/Gorinchem/dino/1626d423-0d17-499f-b97b-b0ef48fb542f.zip'):
        name = d['Locatie']
        filter = int(d['Filternummer'])
        datum = datetime.datetime.strptime(d['Datum maaiveld gemeten'],'%d-%M-%Y')
        x = float(d['X-coordinaat'])
        y = float(d['Y-coordinaat'])
        loc = Point(x,y)
        maaiveld = float(d['Maaiveld (cm t.o.v. NAP)']) / 100
        refpnt = float(d['Meetpunt (cm t.o.v. NAP)']) / 100
#         well,created = Well.objects.get_or_create(nitg=name, defaults = {'name': name,
#                                                                  'maaiveld': maaiveld,
#                                                                  'refpnt': refpnt,
#                                                                  'date': datum,
#                                                                  })
#         well.save()
        print f, len(d['standen'])
        
