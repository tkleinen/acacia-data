'''
Created on Sep 1, 2014

@author: theo
'''
from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator
import pandas as pd

NEERSLAG = (('d','droog'),('g','gemiddeld'),)
BODEMTYPE = (('z','zand op klei'),)
KWALITEIT=(('f', 'zoet'),('b','brak'),('s','zout'))
IRRIGATIE=(('i', 'DI systeem'),('d','druppelbevloeiing'))
REKENTYPE = (('o','oppervlakte'),('v','volume'))
           
class Scenario(models.Model):
    naam = models.CharField(max_length=100)
    neerslag = models.CharField(max_length=1,choices=NEERSLAG,default='g',verbose_name='waterbehoefte')
    bodem = models.CharField(max_length=1,choices=BODEMTYPE,default='z',verbose_name='bodemtype')
    kwaliteit = models.CharField(max_length=1,choices=KWALITEIT,default='f',verbose_name='waterkwaliteit')
    irrigatie = models.CharField(max_length=1,choices=IRRIGATIE,default='d',verbose_name='methode van watergift')
    reken = models.CharField(max_length=1,choices=REKENTYPE,default='o',verbose_name='berekeningsmethode')
    oppervlakte = models.FloatField(default=1, validators = [MinValueValidator(0.1), MaxValueValidator(1000)], verbose_name='grootte', help_text = 'oppervlakte perceel (Ha)')
    volume = models.FloatField(default=5000, validators = [MinValueValidator(0.1), MaxValueValidator(1000000)], verbose_name='grootte', help_text = 'volume bassin (m3)')

    def __unicode__(self):
        return self.naam

    def matrix_code(self):
        ''' bepaal matrix code adhv gemaakte keuzes'''
        return self.neerslag+self.bodem+self.kwaliteit+self.irrigatie
    
GEWAS= (('t', 'tulp'), ('n','narcis'),('a', 'aardappel'), ('m', 'mais'), ('g', 'graan'))
GROND = (('k','klei'),('z','zand'),('v','veen'),)
KWEL = (('k', 'kwel'), ('i', 'infiltratie'),)
ZOUT=(('f', 'zoet'),('s','zout'))
WDEK=(('h', 'hoog'),('l','laag'))
IRRI=(('p', 'DI systeem'),('d','druppelbevloeiing'))
REKEN = (('o','perceel'),('v','bassin'))

class Gift(models.Model):
    gewas = models.CharField(max_length=1,choices=GEWAS,default='t',verbose_name='gewas')
    grondsoort = models.CharField(max_length=1,choices=GROND,default='k',verbose_name='grondsoort')
    gift = models.FloatField(verbose_name='optimale watergift')
    
    class Meta:
        unique_together = ('gewas', 'grondsoort')
        
    def __unicode__(self):
        return self.gewas+self.grondsoort
    
class Scenario2(models.Model):
    naam = models.CharField(max_length=100,default='scenario')
    gewas = models.CharField(max_length=1,choices=GEWAS,default='t',verbose_name='gewas')
    irrigatie = models.CharField(max_length=1,choices=IRRI,default='d',verbose_name='methode van watergift')
    grondsoort = models.CharField(max_length=1,choices=GROND,default='z',verbose_name='grondsoort')
    kwaliteit = models.CharField(max_length=1,choices=ZOUT,default='f',verbose_name='waterkwaliteit')
    kwel=models.CharField(max_length=1,choices=KWEL,default='i',verbose_name='kwel of infiltratie')
    weerstand=models.CharField(max_length=1,choices=WDEK,default='h',verbose_name='weerstand deklaag')
    reken = models.CharField(max_length=1,choices=REKEN,default='o',verbose_name='berekeningsmethode')
    perceel = models.FloatField(default=5, verbose_name='oppervlakte perceel', help_text = 'oppervlakte perceel in hectare')
    bassin = models.FloatField(default=5000, verbose_name='volume bassin', help_text = 'volume bassin in m3')
    lon = models.FloatField(null=True,blank=True)
    lat = models.FloatField(null=True,blank=True)
    #adres = models.CharField(max_length=256,null=True,blank=True)
    user = models.ForeignKey(User,null=True,blank=True)

    def __unicode__(self):
        return self.matrix_code()

    def matrix_code(self):
        ''' bepaal matrix code adhv gemaakte keuzes'''
        return self.gewas+self.irrigatie+self.grondsoort+self.kwaliteit+self.weerstand+self.kwel

GEWAS3= (('t', 'tulp'), ('n','narcis'),('a', 'aardappel'), ('m', 'mais'), ('g', 'graan'))
GROND3 = (('k','klei'),('z','zand'),('v','veen'),)
KWEL3 = (('k', 'kwel'),)
ZOUT3=(('s','zout'),)
WDEK3=(('h', 'hoog'),)
IRRI3=(('d','druppelbevloeiing'),)
OPSLAG3 = (('b','bassin'),('o','ondergronds'))
REKEN3 = (('p','vaste perceelsgrootte, varierende opslag'),('o','vaste opvang, varierende perceelsgrootte'))


class Scenario3(models.Model):
    naam = models.CharField(max_length=100,default='scenario')
    gewas = models.CharField(max_length=1,choices=GEWAS3,default='t',verbose_name='gewas')
    irrigatie = models.CharField(max_length=1,choices=IRRI3,default='d',verbose_name='methode van watergift')
    grondsoort = models.CharField(max_length=1,choices=GROND3,default='z',verbose_name='grondsoort')
    kwaliteit = models.CharField(max_length=1,choices=ZOUT3,default='s',verbose_name='waterkwaliteit')
    kwel=models.CharField(max_length=1,choices=KWEL3,default='k',verbose_name='kwel of infiltratie')
    weerstand=models.CharField(max_length=1,choices=WDEK3,default='h',verbose_name='weerstand deklaag')
    opslag = models.CharField(max_length=1,choices=OPSLAG3,default='o',verbose_name='opslag van water')
    reken = models.CharField(max_length=1,choices=REKEN3,default='o',verbose_name='berekeningsmethode')
    perceel = models.FloatField(default=5, verbose_name='oppervlakte perceel', help_text = 'oppervlakte te irrigeren perceel in hectare')
    oppervlakte = models.FloatField(default=5, verbose_name='oppervlakte opvang')
    bassin = models.FloatField(default=5000, verbose_name='volume bassin', help_text = 'volume bassin in m3')
    lon = models.FloatField(null=True,blank=True)
    lat = models.FloatField(null=True,blank=True)
    #adres = models.CharField(max_length=256,null=True,blank=True)
    user = models.ForeignKey(User,null=True,blank=True)

    def translate(self, choice, choices1, choices2):
        try:
            for c1,c2 in zip(choices1,choices2):
                if choice == c1:
                    return c2
        except:
            pass
        return choice

    def as_scenario2(self):
        s2 = Scenario2()
        s2.naam = self.naam
        s2.gewas = self.gewas
        s2.irrigatie = self.irrigatie
        s2.grondsoort = self.grondsoort
        s2.kwaliteit = self.kwaliteit
        s2.kwel = self.kwel
        s2.weerstand = self.weerstand
        s2.reken = 'o' if self.reken == 'p' else 'v'
        s2.perceel = self.perceel
        s2.bassin = self.bassin
        s2.lon = self.lon
        s2.lat = self.lat
        s2.user = self.user
        return s2

    def __unicode__(self):
        return self.matrix_code()

    def matrix_code(self):
        ''' bepaal matrix code adhv gemaakte keuzes'''
        code = self.gewas
        if self.opslag == 'o':
            code += 'o'
        else:
            code +=self.irrigatie
        code += self.grondsoort+self.kwaliteit+self.weerstand+self.kwel
        return code
            
class Matrix(models.Model):
    code = models.CharField(max_length=10, unique=True)
    toelichting = models.TextField(blank=True)
    file = models.FileField(upload_to='matrix')
    rijnaam = models.CharField(default = 'Oppervlakte perceel (Ha)', max_length=50)
    rijmin = models.FloatField(blank=True)
    rijmax = models.FloatField(blank=True)
    kolomnaam = models.CharField(default = 'Oppervlakte bassin (Ha)', max_length=50)
    kolmin = models.FloatField(blank=True)
    kolmax = models.FloatField(blank=True)
    maxopbrengst = models.FloatField(verbose_name = 'maximum opbrengst', default = 0)
    factor = models.FloatField(verbose_name = 'omrekenfactor', default = 0)
    
    def get_dimensions(self, f=None):
        src = f or self.file.path
        df = pd.read_csv(src,index_col=0)
        self.code = df.index.name
        self.rijmin = float(df.index[0]) 
        self.rijmax = float(df.index[-1]) 
        self.kolmin = float(df.columns[0]) 
        self.kolmax = float(df.columns[-1])
        drow = (self.rijmax - self.rijmin) / (df.shape[0]-1)
        dcol = (self.kolmax - self.kolmin) / (df.shape[1]-1)
        return (drow,dcol)
        
    def __unicode__(self):
        return self.code

    @property
    def data(self):
        if not hasattr(self,'_data'):
            self._data = pd.read_csv(self.file.path,index_col=0)
        return self._data

    class Meta:
        verbose_name_plural = 'matrices'
