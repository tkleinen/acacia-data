'''
Created on Jun 1, 2014

@author: theo
'''
import os, pandas as pd, numpy as np
from django.db import models
from django.contrib.gis.db import models as geo
from django.core.urlresolvers import reverse
from gorinchem import settings, util
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Network(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name = 'naam')
    logo = models.ImageField(upload_to='logos')
    last_round = models.DateField(null=True,blank=True,verbose_name = 'laatste uitleesronde')
    next_round = models.DateField(null=True,blank=True,verbose_name = 'volgende uitleesronde')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('network-detail', args=[self.id])

    class Meta:
        verbose_name = 'netwerk'
        verbose_name_plural = 'netwerken'

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    network = models.ManyToManyField(Network,verbose_name='Meetnet') 

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
        
class Well(geo.Model):
    network = models.ForeignKey(Network, verbose_name = 'Meetnet')
    name = models.CharField(max_length=50, unique=True, verbose_name = 'naam')
    nitg = models.CharField(max_length=50, verbose_name = 'TNO/NITG nummer', blank=True)
    bro = models.CharField(max_length=50, verbose_name = 'BRO nummer', blank=True)
    location = geo.PointField(srid=28992,verbose_name='locatie')
    maaiveld = models.FloatField(verbose_name = 'maaiveld', help_text = 'maaiveld in meter tov NAP')
    refpnt = models.FloatField(verbose_name = 'referentiepunt', help_text='referentiepunt in meter tov NAP')
    date = models.DateField(verbose_name = 'constructiedatum')
    straat = models.CharField(max_length=60, blank=True)
    huisnummer = models.CharField(max_length=6, blank=True)
    postcode = models.CharField(max_length=8, blank=True)
    plaats = models.CharField(max_length=60, blank=True)
    log = models.ImageField(null=True,blank=True,upload_to='logs',verbose_name = 'boorstaat')
    chart = models.ImageField(null=True,blank=True, upload_to='charts', verbose_name='grafiek')
    objects = geo.GeoManager()

    def latlon(self):
        return util.toWGS84(self.location)

    def RD(self):
        return util.toRD(self.location)

    def num_filters(self):
        return self.screen_set.count()
    num_filters.short_description='aantal filters'

    def num_photos(self):
        return self.photo_set.count()
    num_photos.short_description='aantal fotos'

    def get_loggers(self):
        loggers = []
        for s in self.screen_set.all():
            loggers.extend(s.datalogger_set.all())
        return loggers
    
    def num_loggers(self):
        return len(get_loggers)
    num_loggers.short_description='aantal dataloggers'
    
    def logger_names(self):
        return ','.join([l.serial for l in self.get_loggers()])
    logger_names.short_description='dataloggers'
    
    def get_absolute_url(self):
        return reverse('well-detail', args=[self.id])

    def __unicode__(self):
        return self.name
    
    def has_data(self):
        for s in self.screen_set.all():
            if s.num_standen() > 0:
                return True
        return False
    
    class Meta:
        verbose_name = 'put'
        verbose_name_plural = 'putten'
        ordering = ['name',]

class Photo(models.Model): 
    well = models.ForeignKey(Well)
    photo = models.ImageField(upload_to = 'fotos') 
    
    def thumb(self):
        url = os.path.join(settings.MEDIA_URL, self.photo.name)
        return '<a href="%s"><img src="%s" height="60px"/></a>' % (url,url)

    def __unicode__(self):
        return os.path.basename(self.photo.file.name)

    thumb.allow_tags=True
    thumb.short_description='voorbeeld'

    class Meta:
        verbose_name = 'foto'
        verbose_name_plural = "foto's"
    
MATERIALS = (
             ('pvc', 'PVC'),
             ('hdpe', 'HDPE'),
             ('ss', 'RVS'),
             ('ms', 'Staal'),
             )                  
class Screen(models.Model):
    well = models.ForeignKey(Well, verbose_name = 'put')
    nr = models.IntegerField(default=1, verbose_name = 'filternummer')
    top = models.FloatField(verbose_name = 'bovenkant', help_text = 'bovenkant filter in meter min maaiveld')
    bottom = models.FloatField(verbose_name = 'onderkant', help_text = 'onderkant filter in meter min maaiveld')
    diameter = models.FloatField(verbose_name = 'diameter', default=32, help_text='diameter in mm (standaard = 32 mm)')
    material = models.CharField(max_length = 10,verbose_name = 'materiaal', default='pvc', choices = MATERIALS)
    
    def num_standen(self):
        return self.datapoint_set.count()

    def last_logger(self):
        return self.datalogger_set.all().order_by('date').last()
        
    def __unicode__(self):
        return '%s/%03d' % (self.well, self.nr)

    def get_absolute_url(self):
        return reverse('screen-detail', args=[self.id])

    def to_pandas(self):
        points = self.datapoint_set.all()
        dates = [dp.date for dp in points]
        values = [dp.level for dp in points]
        return pd.Series(values,index=dates,name=self.__unicode__)
        
    def stats(self):
        df = self.to_pandas()
        s = df.describe(percentiles=[.1,.5,.9])
        s['p10'] = None if np.isnan(s['10%']) else s['10%']
        s['p50'] = None if np.isnan(s['50%']) else s['50%']
        s['p90'] = None if np.isnan(s['90%']) else s['90%']
        return s
        
    class Meta:
        unique_together = ('well', 'nr',)
        verbose_name = 'filter'
        verbose_name_plural = 'filters'
        ordering = ['well', 'nr',]
        
DIVER_TYPES = (
               ('micro','Micro-Diver'),
               ('td', 'TD-Diver'),
               ('ctd','CTD-Diver'),
               ('cera','Cera-Diver'),
               ('mini','Mini-Diver'),
               ('baro','Baro-Diver')
               )
class Datalogger(models.Model):
    serial = models.CharField(max_length=50,verbose_name = 'serienummer', unique=True)
    model = models.CharField(max_length=50,verbose_name = 'type', default='ctd', choices=DIVER_TYPES)
    screen = models.ForeignKey(Screen,verbose_name = 'filter')
    date = models.DateTimeField(verbose_name = 'datum', help_text = 'Datum en tijd van installatie datalogger')
    refpnt = models.FloatField(verbose_name = 'referentiepunt', help_text = 'ophangpunt in meter tov NAP')
    depth = models.FloatField(verbose_name = 'kabellengte', help_text = 'lengte van ophangkabel in meter')

    def __unicode__(self):
        return self.serial

    class Meta:
        ordering = ['serial',]
        
class DataPoint(models.Model):
    screen = models.ForeignKey(Screen, verbose_name = 'filter')
    date = models.DateTimeField(verbose_name = 'datum')
    level = models.FloatField(verbose_name = 'stand', help_text = 'stand in m tov NAP')

    def __unicode__(self):
        return '%s %s' % (self.screen, self.date)
    
    class Meta:
        verbose_name = 'Stand'
        verbose_name_plural = 'Standen'
        unique_together = ('screen', 'date',)
    