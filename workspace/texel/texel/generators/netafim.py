'''
Created on Oct 18, 2014

@author: theo
'''
from acacia.data.generators.generator import Generator
import zipfile, xlrd, datetime
import numpy as np
import pandas as pd
import re

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
    
    def get_header(self, f):
        f.seek(0)
        for i in range(5):
            line = f.readline()
        self.skiprows = 5
        return {'COLUMNS': [c.strip() for c in line.split(',')]}

    def get_parameters(self,fil):
        header = self.get_header(fil)
        names = header['COLUMNS'][1:]
        params = {}
        for name in names:
            params[name] = {'description' : name, 'unit': '-'} 
        return params # use only 1st file from archive
 
    def squeeze(self, d):
        ''' squeeze series in d '''
        df = pd.DataFrame()
        series = [d[s].dropna() for s in d]
        return df.join(series, how='outer')

    def get_data(self, f, **kwargs):
        header = self.get_header(f)
        names = header['COLUMNS']
        skiprows = self.skiprows if self.engine == 'python' else 0
        data = self.read_csv(f, header=None, names=names, skiprows=skiprows, index_col=[0], parse_dates = 0, date_parser = date_parser, na_values=[' ','',])
        return self.squeeze(data)

    def parse_filename(self, name):
        return re.split('[_\.]',name)
        
    def download(self, **kwargs):
        #start = kwargs.get('start', None)
        result = {}
        if 'url' in kwargs:
            from urlparse import urlparse
            url = kwargs['url']
            scheme, netloc, path, params, query, fragment = urlparse(url)
            username = kwargs.get('username',None)
            passwd = kwargs.get('password',None)
            self.location = kwargs.get('location', self.location)
            callback = kwargs.get('callback', None)
            start = kwargs.get('start', None)
            
            ftp = scheme == 'ftp'
            if ftp:
                from ftplib import FTP, Error

                ftp = FTP()
                ftp.connect(netloc)
                ftp.login(username, passwd)
                ftp.cwd(path[1:])
                files = ftp.nlst()
                                    
                if start is not None:
                    start = start.replace(tzinfo=None)

                for f in files:

                    try:
                        loc, date, time, ext = self.parse_filename(f)
                    
                        if self.location is not None:
                            #if self.location != loc:
                            if not f.startswith(self.location):
                                continue
                    
                        if start is not None:
                            date = datetime.datetime.strptime(date+time[:6],'%Y%m%d%H%M%S')
                            if date < start:
                                continue
                    
                    except Exception as e:
                        continue 
 
                    def save(data):
                        result[f] = data
                        if callback is not None:
                            callback(f, data)
                    
                    try:
                        ftp.retrbinary('RETR ' + f, save)
                    except Error as e:
                        # timeout?
                        break
        return result
    
class IrriwiseZip(Irriwise):

    def download(self, **kwargs):
        return Generator.download(self, **kwargs)
        
    def get_header(self, f):
        for i in range(5):
            line = f.readline()
        self.skiprows = 0
        return {'COLUMNS': [c.strip() for c in line.split(',')]}

    def get_files(self, zipname):
        ''' get all files in zipfile grouped by location '''
        files = {}
        with zipfile.ZipFile(zipname,'r') as z:
            for info in z.infolist():
                filename = info.filename
                loc = self.parse_filename(filename)[0]
                if loc not in files:
                    files[loc] = []
                files[loc].append(filename)
        return files
    
    def get_data(self, zipname, **kwargs):
        files = self.get_files(zipname)
        data = None
        with zipfile.ZipFile(zipname,'r') as z:
            for loc in files.iterkeys():
                if self.location is None or self.location == loc:
                    for file in files[loc]:
                        with z.open(file) as f:
                            d = super(IrriwiseZip,self).get_data(f,**kwargs)
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
                            return super(IrriwiseZip,self).get_parameters(f)
                            # use only 1st file from archive
def callback(name,data):
    print name
    
if __name__ == '__main__':
    p = IrriwiseZip()
    f = '/home/theo/data/netafim/REF REF 2.zip'
    par = p.get_parameters(f)
    print par
    data = p.get_data(f)
    data.sort()
    print data
    

#     p = Irriwise()
#     #result = p.download(url='ftp://82.192.75.237/Texel/Irriwise',username='arjen',password='acacia1234',filename='Texel/Irriwise',location='REF REF 2', callback = callback)
#     with open('/home/theo/data/netafim/REF REF 2_20150204_223820894.csv','rb') as f:
#         par = p.get_parameters(f)
#         print par
#         data = p.get_data(f)
#         data.sort()
#         print data

    
#     f = '/media/sf_C_DRIVE/projdirs/Texel/data/Bodemvocht.zip'
#     par = p.get_parameters(f)
#     print par
#     data = p.get_data(f).sort()
#     print data
    