# -*- coding: utf-8 -*-
'''
Created on May 19, 2016

@author: theo
'''
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.decorators.clickjacking import xframe_options_exempt

from acacia.data.models import MeetLocatie, KeyFigure

class PictureView(TemplateView):
    template_name = 'picture.html'
    
    def get_context_data(self, **kwargs):
        context = super(PictureView,self).get_context_data(**kwargs)
        pk = context.get('pk',1)
        locatie = get_object_or_404(MeetLocatie,pk=pk)
        context['locatie'] = locatie
        keys = KeyFigure.objects.filter(locatie=locatie)
        for key in keys:
            context[key.name] = str(key.value)
        return context    
        
class PFView(PictureView):
    template_name = 'pict/pf.html'
    
class PFDripView(PFView):
    template_name = 'pict/pfdrip.html'
    
class PFRefView(PFView):
    template_name = 'pict/pfref.html'

class InfiltratieView(PictureView):
    template_name = 'pict/infiltratie.html'
        
class OpslagView(PictureView):
    template_name = 'pict/opslag.html'
        
    