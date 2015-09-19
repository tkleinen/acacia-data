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

def WaarnemingenToDict(request, pk):
    ''' return dataframe with observations (ec, temp) as dict'''
    mp = get_object_or_404(Meetpunt,pk=pk)
    ec = mp.get_series('EC').to_pandas()
    temp = mp.get_series('Temp').to_pandas()
    df = pd.DataFrame([ec,temp])
    data = df.to_dict()
    dct = [{'date': k, 'EC': v[ec.name], 'Temp': v[temp.name]} for (k, v) in data.iteritems()]
    dct.sort(key=lambda x: x['date'])
    j = json.dumps(dct, default=lambda x: str(x))
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
#         series = meetpunt.get_series('EC')
#         if series is not None:
#             paginator = Paginator(series.datapoints.all(),14)
#             page = self.request.GET.get('page')
#             try:
#                 points = paginator.page(page)
#             except PageNotAnInteger:
#                 points = paginator.page(1)
#             except EmptyPage:
#                 points = paginator.page(paginator.num_pages)
#             context['points'] = points
#             context['series'] = series
        return context
    
class UploadPhotoView(UpdateView):
    model = Meetpunt
    fields = ['photo',]
    template_name_suffix = '_photo_form'
