'''
Created on Oct 18, 2014

@author: theo
'''
from acacia.data.generators.generator import Generator

class Regenmeter(Generator):
    ''' Texel regenmeter: date+tick '''

    def get_header(self, f):
        return {'COLUMNS': ['Record', 'Datum', 'Puls'],}
            
    def get_data(self, f, **kwargs):
        header = self.get_header(f)
        names = header['COLUMNS']
        data = self.read_csv(f, header=None, skiprows = 2, names=names, index_col=[0], usecols = [1,2], parse_dates = True)
        data.dropna(inplace=True)
        return data

    def get_parameters(self, fil):
        header = self.get_header(fil)
        names = header['COLUMNS'][2:]
        params = {}
        for name in names:
            params[name] = {'description' : name, 'unit': '-'} 
        return params

if __name__ == '__main__':
    p = Regenmeter()
    with open('/media/sf_C_DRIVE/projdirs/Texel/data/Schermer_PPN-08072014.txt') as f:
        data = p.get_data(f)
        print data
    