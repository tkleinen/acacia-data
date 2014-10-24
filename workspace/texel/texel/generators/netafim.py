'''
Created on Oct 18, 2014

@author: theo
'''
from acacia.data.generators.generator import Generator
import zipfile, xlrd, datetime
import numpy as np
import pandas as pd

def convert(dt):
    tup = xlrd.xldate_as_tuple(dt, 0)
    dt = datetime.datetime(*tup)
    return dt

def date_parser(dt):
    return np.array([convert(float(t)) for t in dt])

class Irriwise(Generator):

    def __init__(self, *args, **kwargs):
        self.location = kwargs.get('location', None)
        return super(Irriwise, self).__init__(*args, **kwargs)
    
    def get_files(self, zipname):
        ''' get all files in zipfile grouped by location '''
        files = {}
        with zipfile.ZipFile(zipname,'r') as z:
            for info in z.infolist():
                filename = info.filename
                root = filename.split('_')[0]
                loc = root.split(' ')[-1] # laatste woord voor eerste underscore is locatienaam
                if loc not in files:
                    files[loc] = []
                files[loc].append(filename)
        return files
    
    def get_file_header(self, f):
        for i in range(5):
            line = f.readline()
        return {'COLUMNS': [c.strip() for c in line.split(',')]}

    def squeeze(self, d):
        ''' squeeze series in d '''
        df = pd.DataFrame()
        return df.join([d[s].dropna() for s in d], how='outer')

    def get_file_data(self, f, **kwargs): 
        header = self.get_file_header(f)
        names = header['COLUMNS']
        data = self.read_csv(f, header=None, names=names, index_col=[0], parse_dates = 0, date_parser = date_parser, na_values=[' ','',])
        return self.squeeze(data)

    def get_data(self, f, **kwargs):
        files = self.get_files(f)
        data = None
        with zipfile.ZipFile(f,'r') as z:
            for loc in files.iterkeys():
                if self.location is None or self.location == loc:
                    for file in files[loc]:
                        with z.open(file) as f:
                            d = self.get_file_data(f,**kwargs)
                            if data is None:
                                data = d
                            else:
                                data = data.append(d)
                if self.location is None:
                    # geen locatie opgegeven: gebruik alleen eerste locatie in zip file                    
                    break 
        return data
    
    def get_parameters(self, fil):
        files = self.get_files(fil)
        with zipfile.ZipFile(fil,'r') as z:
            for loc in files.iterkeys():
                if self.location is None or self.location == loc:
                    for file in files[loc]:
                        with z.open(file) as f:
                            header = self.get_file_header(f)
                            names = header['COLUMNS'][1:]
                            params = {}
                            for name in names:
                                params[name] = {'description' : name, 'unit': '-'} 
                            return params # use only 1st file from archive
    
if __name__ == '__main__':
    p = Irriwise()
    f = '/media/sf_C_DRIVE/projdirs/Texel/data/Bodemvocht.zip'
    par = p.get_parameters(f)
    print par
    data = p.get_data(f).sort()
    print data
    