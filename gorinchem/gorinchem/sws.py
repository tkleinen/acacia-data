'''
Created on Jan 26, 2014

@author: theo
'''
import pandas as pd
import logging
logger = logging.getLogger(__name__)

class MonFileException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Diver():
    header = None
    def get_header(self,f):
        line = f.readline()
        if not line.startswith('Data file for DataLogger.'):
            raise MonFileException('%s is not recognized as mon file' % f.name )
        line = f.readline()
        if not line.startswith('====='):
            raise MonFileException('%s is not recognized as mon file' % f.name )
        header = {}
        while True:
            line = f.readline()
            if 'BEGINNING OF DATA' in line:
                break
            colon = line.find(':')
            if colon < 0:
                raise MonFileException('colon expected parsing line \'%s\'' % line )
            key = line[0:colon].strip()
            if key == '':
                continue
            value = line[colon+1:].strip()
            header[key] = value
        sections = {}
        sections['HEADER'] = header
        section = {}
        sections['DEFAULT'] = section
        while True:
            line = f.readline().strip()
            if line == '':
                continue
            if line == '[Data]':
                break
            if line.startswith('['):
                name = line.strip('[]').strip()
                section = {}
                sections[name] = section
            else:
                delim = line.find('=')
                if delim < 0:
                    continue
                key = line[0:delim].strip()
                value = line[delim+1:].strip()
                section[key] = value
        self.header = sections
        return self.header

    def get_data(self,f,**kwargs):
        self.header = self.get_header(f)
        names = ['DATE','TIME']
        num = int(self.header['Logger settings'].get('Number of channels'))
        for i in range(1,num+1):
            name = self.header['Channel %d' % i].get('Identification')
            names.append(name)
        num=int(f.readline())
        data = pd.read_csv(f, header=0, index_col=0, names = names, delim_whitespace=True, parse_dates = {'date': [0,1]}, nrows=num-1)
        return data

if __name__ == '__main__':
    d = Diver()
    with open(r'/home/theo/acaciadata.com/gorinchem/data/Delft MON files/Delft groundwater.MON') as f:
        df = d.get_data(f)
        print d.header
        