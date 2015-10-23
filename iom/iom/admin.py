'''
Created on Jun 16, 2015

@author: theo
'''
from django.contrib import admin
from django import forms
from django.forms import Textarea
from django.contrib.gis.db import models
from .models import UserProfile, Adres, Waarnemer, Meetpunt, Organisatie, AkvoFlow
from acacia.data.models import DataPoint, ManualSeries

from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .util import maak_meetpunt_grafiek

import re

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class DataPointInline(admin.TabularInline):
#class DataPointInline(nested_admin.TabularInline):
    model = DataPoint

class SeriesInline(admin.StackedInline):
#class SeriesInline(nested_admin.NestedStackedInline):
    model = ManualSeries
    fields = ('name',)
    inlines = (DataPointInline,)
    verbose_name = 'Tijdreeks'
    verbose_name_plural = 'Tijdreeksen'

def maak_grafiek(modeladmin, request, queryset):
    for m in queryset:
        maak_meetpunt_grafiek(m,request.user)
maak_grafiek.short_description = "Maak grafieken voor geselecteerde meetpunten"
        
@admin.register(Meetpunt)
class MeetpuntAdmin(admin.ModelAdmin):
#class MeetpuntAdmin(nested_admin.NestedAdmin):
    actions = [maak_grafiek,]
    list_display = ('name', 'waarnemer', 'description')
    list_filter = ('waarnemer', )
    inlines = [SeriesInline,]
    search_fields = ('name', 'waarnemer__achternaam', )
    fields = ('name', 'waarnemer', 'location', ('photo_url','chart_thumbnail'), 'description',)
    formfield_overrides = {models.PointField:{'widget': Textarea}}
    
class AdresForm(forms.ModelForm):
    model = Adres
    
    def clean_postcode(self):
        pattern = r'\d{4}\s*[A-Za-z]{2}'
        data = self.cleaned_data['postcode']
        if re.search(pattern, data) is None:
            raise ValidationError('Onjuiste postcode')
        return data

@admin.register(Adres)
class AdresAdmin(admin.ModelAdmin):
    form = AdresForm
    fieldsets = (
                  ('', {'fields': (('straat', 'huisnummer', 'toevoeging'),('postcode', 'plaats')),
                        'classes': ('grp-collapse grp-open',),
                       }
                  ),
                )
    
@admin.register(Waarnemer)
class WaarnemerAdmin(admin.ModelAdmin):        
    list_display = ('achternaam', 'tussenvoegsel', 'voornaam', 'organisatie', 'akvoname', 'aantal_meetpunten', 'aantal_waarnemingen')
    list_filter = ('achternaam', 'organisatie','akvoname',)
    search_fields = ('achternaam', 'voornaam', 'akvoname', )
    ordering = ('achternaam', )

@admin.register(Organisatie)
class OrganisatieAdmin(admin.ModelAdmin):        
    raw_id_fields = ('adres',)
    autocomplete_lookup_fields = {
        'fk': ['adres',],
    }
    
@admin.register(AkvoFlow)
class AkvoAdmin(admin.ModelAdmin):
    list_display = ('name', 'instance', 'description')
    list_filter = ('name', )
    search_fields = ('name', 'instance', )
