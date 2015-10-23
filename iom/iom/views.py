'''
Created on Jun 12, 2015

@author: theo
'''
from django.views.generic import TemplateView, DetailView
from .models import Waarnemer, Meetpunt
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
import pandas as pd
from django.views.generic.edit import UpdateView
from iom.forms import UploadPhotoForm
from django.utils import timezone
import locale
from django.conf import settings
from acacia.data.models import Project, ProjectLocatie

def WaarnemingenToDict(request, pk):
    tz = timezone.get_current_timezone()
    locale.setlocale(locale.LC_ALL,'nl_NL.utf8')
    
    ''' return dataframe with observations (ec, temp) as dict'''
    mp = get_object_or_404(Meetpunt,pk=pk)
    ec = mp.get_series('EC').to_pandas()
    temp = mp.get_series('Temp').to_pandas()
    df = pd.DataFrame([ec,temp])

    # bootstrap data table does not like NaN values
    df.fillna('', inplace=True)
    
    data = df.to_dict()
    #dct = [{'date': k.astimezone(tz).strftime('%c'), 'EC': v[ec.name], 'Temp': v[temp.name]} for (k, v) in data.iteritems()]
    dct = [{'date': k, 'EC': v[ec.name], 'Temp': v[temp.name]} for (k, v) in data.iteritems()]
    dct.sort(key=lambda x: x['date'])
    j = json.dumps(dct, default=lambda x: x.astimezone(tz).strftime('%c'))
    return HttpResponse(j, content_type='application/json')
    
class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        content = []
        meetpunten = Meetpunt.objects.all() 
        for mp in meetpunten:
            pos = mp.latlon()
            content.append({'meetpunt': mp.pk,
                            'name': mp.name,
                            'lat': pos.y,
                            'lon': pos.x,
                            'url': ''#reverse('meetpunt-info', args=[mp.id]),
                            })
        waarnemers = list(Waarnemer.objects.all())
        waarnemers.sort(key = lambda x: -x.aantal_waarnemingen())
        context['waarnemers'] = waarnemers
        context['meetpunten'] = meetpunten
        context['content'] = json.dumps(content)
        context['maptype'] = 'ROADMAP'
        return context

class WaarnemerDetailView(DetailView):
    template_name = 'waarnemer-detail.html'
    model = Waarnemer    

    def get_context_data(self, **kwargs):
        context = super(WaarnemerDetailView, self).get_context_data(**kwargs)
        waarnemer = self.get_object();
        context['meetpunten'] = waarnemer.meetpunt_set.all()
        return context

class MeetpuntDetailView(DetailView):
    template_name = 'meetpunt-grafiek.html'
    model = Meetpunt    

    def get_context_data(self, **kwargs):
        context = super(MeetpuntDetailView, self).get_context_data(**kwargs)
        meetpunt = self.get_object();
        latlon = meetpunt.latlon()
        context['location'] = latlon
        return context
    
class UploadPhotoView(UpdateView):
    model = Meetpunt
    fields = ['photo',]
    template_name_suffix = '_photo_form'

from .akvo import FlowAPI
from .models import AkvoFlow

def importAkvoRegistration(api,surveyId,projectLocatie):
    for key,instance in api.get_registration_instances(surveyId).items():
        answers = api.get_answers(instance['keyId'])
        identifier=instance['surveyedLocaleIdentifier']
        locale = instance['surveyedLocaleDisplayName']
        geoloc = answers['9070917|Geolocatie']        
        try:
            mp = Meetpunt.objects.get(identifier=identifier)
        except Meetpunt.DoesNotExist:
            mp = Meetpunt(identifier = identifier, name=name, projectlocatie = projectlocatie, location=location,description = description)

def importAkvoMonitoring(api,surveys):
    for surveyId in surveys:
        survey = api.get_survey(surveyId)
        instances,meta = api.get_survey_instances(surveyId=surveyId)
        while instances:
            for instance in instances:
                #find related registration form (meetpunt)
                localeId = instance['surveyedLocaleIdentifier']
                try:
                    mp = Meetpunt.objects.get(identifier=localeId)
                except Meetpunt.DoesNotExist:
                    continue
                answers = api.get_answers(instance['keyId'])
                # TODO: create/add datapoints to timeseries

            instances,meta = api.get_survey_instances(surveyId=surveyId, since=meta['since'])
                        
def importAkvo(request):
    '''import data from akvo flow'''
    akvo = get_object_or_404(AkvoFlow,name='Texel Meet')
    api = FlowAPI(instance=akvo.instance, key=akvo.key, secret=akvo.secret)

    project = ProjectLocatie.objects.get(pk=1) # Texel
    importAkvoRegistration(api, akvo.regform, projectLocatie=project)

    surveys = [f.trim() for f in akvo.monforms.split(',')]
    importAkvoMonitoring(api, surveys)

    return 'Done'