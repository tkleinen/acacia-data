'''
Created on Jun 14, 2015

@author: theo
'''
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from acacia.data.models import MeetLocatie, Chart

# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models as geo

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to='images')

from django.db.models.signals import post_save

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
    
class Adres(models.Model):
    postcode = models.CharField(max_length=7)
    huisnummer = models.IntegerField()
    toevoeging = models.CharField(max_length=20,blank=True,null=True)
    straat = models.CharField(max_length=100)
    plaats = models.CharField(max_length=100)
    
    def __unicode__(self):
        return '%s %d%s, %s'% (self.straat, self.huisnummer, self.toevoeging or '', self.plaats)

    @staticmethod
    def autocomplete_search_fields():
        return ("plaats__icontains", "straat__icontains",)

    class Meta:
        verbose_name_plural = 'Adressen'

from django.core.validators import RegexValidator
phone_regex = RegexValidator(regex=r'^(?:\+)?[0-9\-]{10,11}$',
                             message="Ongeldig telefoonnummer")

class Organisatie(models.Model):
    naam = models.CharField(max_length=50)
    omschrijving = models.TextField(blank=True,null=True)
    website=models.URLField(blank=True)
    email = models.EmailField(blank=True)
    telefoon = models.CharField(max_length=16, validators=[phone_regex], blank=True)
    adres = models.ForeignKey(Adres, null=True, blank=True)

    def __unicode__(self):
        return self.naam

class Waarnemer(models.Model):
    initialen=models.CharField(max_length=6,null=True,blank=True)
    voornaam=models.CharField(max_length=20,null=True,blank=True)
    tussenvoegsel=models.CharField(max_length=10,null=True,blank=True)
    achternaam=models.CharField(max_length=40)

    telefoon = models.CharField(max_length=16, validators=[phone_regex], blank=True)
    email=models.EmailField(blank=True)
    organisatie = models.ForeignKey(Organisatie, blank=True, null=True)
    
    akvoname = models.CharField(max_length=40,verbose_name='Akvo-Id',blank=True,null=True)
    
    def get_absolute_url(self):
        return reverse('waarnemer-detail', args=[self.id])
    
    class Meta:
        verbose_name_plural = 'Waarnemers'
        ordering = ['achternaam']
        
    def __unicode__(self):
        s = ''
        if self.initialen and len(self.initialen) > 0:
            s = self.initialen + ' '
        if self.tussenvoegsel and len(self.tussenvoegsel) > 0:
            s += self.tussenvoegsel + ' '
        return '%s %s' % (s, self.achternaam)
    
    def aantal_meetpunten(self):
        return self.meetpunt_set.count()
    
    def aantal_waarnemingen(self):
        w = sum([m.aantal_waarnemingen() for m in self.meetpunt_set.all()])
        return w
        
class Meetpunt(MeetLocatie):
    # Akvo flow meetpunt gegevens
    identifier=models.CharField(max_length=50)
    submitter=models.CharField(max_length=50)
    device=models.CharField(max_length=50)
    photo_url=models.CharField(max_length=200,null=True,blank=True)
    
    # location -> Meetlocatie.description?
    # Meetpunt ID -> Meetlocatie.name
    # Geolocatie -> MeetLocatie.location (Point)
    # photo -> MeetLocatie.image

    waarnemer=models.ForeignKey(Waarnemer)
    chart_thumbnail = models.ImageField(upload_to='thumbnails/charts', blank=True, null=True, verbose_name='voorbeeld', help_text='Grafiek in popup op cartodb kaartje')
    chart = models.ForeignKey(Chart, verbose_name='grafiek', help_text='Interactive grafiek',null=True,blank=True)
    
    def chart_url(self):
        try:
            return self.chart.get_dash_url()
        except:
            return '#'
        
    class Meta:
        verbose_name_plural = 'Meetpunten'
                
    def get_series(self, name='EC'):
        series = [s for s in self.series() if s.name.startswith(name)]
        return series[0] if len(series)>0 else None

    def aantal_waarnemingen(self):
        return sum([s.aantal() for s in self.manualseries_set.all()])
    
class Waarneming(models.Model):
    waarnemer = models.ForeignKey(Waarnemer)
    locatie = models.ForeignKey(Meetpunt)
    datum = models.DateTimeField()
    grootheid = models.CharField(max_length=20)
    eenheid = models.CharField(max_length=20)
    waarde = models.FloatField()
    foto_url = models.CharField(max_length=200,blank=True,null=True)
    opmerking = models.TextField(blank=True,null=True)
    
class AkvoFlow(models.Model):
    ''' Akvo Flow configuratie '''
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    instance = models.CharField(max_length=100)
    key = models.CharField(max_length=100)    
    secret = models.CharField(max_length=100)
    storage = models.CharField(max_length=100) 
    regform = models.CharField(max_length=100,blank=True, null=True, verbose_name = 'Registratieformulier',help_text='Survey id van registratieformulier')
    monforms = models.CharField(max_length=100,blank=True, null=True, verbose_name = 'Monitoringformulier',help_text='Survey id van monitoringformulier')
    
    class Meta:
        verbose_name = 'Akvoflow API'        
        verbose_name_plural = 'Akvoflow API'
        
    def __unicode__(self):
        return self.name