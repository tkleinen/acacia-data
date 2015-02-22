'''
Created on Jun 3, 2014

@author: theo
'''
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from gorinchem.models import Network, Well, Screen
import json, logging, datetime, time, re
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.size'] = '8'
from StringIO import StringIO
import numpy as  np
import pandas as pd
from forms import UploadFileForm

logger = logging.getLogger(__name__)
import monfile

        
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            for f in form.files.getlist('filename'):
                monfile.save(request,f)
            return redirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request,'gorinchem/upload1.html', {'form': form})

def chart_for_screen(screen):
    plt.figure(figsize=(15,5))
    plt.grid(linestyle='-', color='0.9')
    data = screen.get_levels('nap')
    if len(data)>0:
        x,y = zip(*data)
        plt.plot_date(x, y, '-')
        y = [screen.well.maaiveld] * len(x)
        plt.plot_date(x, y, '-')
    plt.title(screen)
    plt.ylabel('m tov NAP')
    img = StringIO() 
    plt.savefig(img,bbox_inches='tight', format='png')
    plt.close()    
    return img.getvalue()

def chart_for_well(well):
    plt.figure(figsize=(15,5))
    plt.grid(linestyle='-', color='0.9')
    count = 0
    y = []
    for screen in well.screen_set.all():
        data = screen.get_levels('nap')
        if len(data)>0:
            x,y = zip(*data)
            plt.plot_date(x, y, '-', label=screen)
            count += 1
            
    y = [screen.well.maaiveld] * len(x)
    plt.plot_date(x, y, '-', label='maaiveld')

    plt.title(well)
    plt.ylabel('m tov NAP')
    if count > 0:
        plt.legend()
    
    img = StringIO() 
    plt.savefig(img,format='png',bbox_inches='tight')
    plt.close()    
    return img.getvalue()

def encode_chart(chart):
    return 'data:image/png;base64,' + chart.encode('base64')

def make_chart(obj):
    if isinstance(obj,Well):
        return chart_for_well(obj)
    elif isinstance(obj,Screen):
        return chart_for_screen(obj)
    else:
        raise Exception('make_chart(): object must be a well or a screen')
    
def make_encoded_chart(obj):
    return encode_chart(make_chart(obj))

# def topd(xy,name):
#     if len(xy) > 0:
#         x,y = zip(*xy)
#     else:
#         x = y = []
#     return pd.Series(index = x, data = y, name = name)
# 
# def export_series(screen):
#     druk = topd(screen.get_levels('nap','PRESSURE'),'druk')
#     baro = topd(screen.get_baro('nap','PRESSURE'),'druk')
#     stand = topd(screen.get_levels('nap','LEVEL'), 'stand')
    
class WellView(DetailView):
    template = 'gorinchem/well_info.html'
    model = Well

    def get_context_data(self, **kwargs):
        context = super(WellView, self).get_context_data(**kwargs)
#        context['chart'] = make_encoded_chart(self.get_object())
        well = self.get_object()
        context['chart'] = None if well.chart.name is None else well.chart.url
        return context

class ScreenView(DetailView):
    model = Screen
    
    def get_context_data(self, **kwargs):
        context = super(ScreenView, self).get_context_data(**kwargs)
#        context['chart'] = make_encoded_chart(self.get_object())
        screen = self.get_object()
        context['chart'] = None if screen.chart.name is None else screen.chart.url
        return context

class NetworkView(DetailView):
    model = Network
 
    def get_subdomain(self):
        domain = self.request.META.get('HTTP_HOST') or self.request.META.get('SERVER_NAME')
        pieces = domain.split('.')
        subdomain = ".".join(pieces[:-2]) # join all but primary domain
        if subdomain == '':
            return None        
        return subdomain
     
    def get_object(self):
        try:
            return super(NetworkView, self).get_object()
        except:
            subdomain = self.get_subdomain()
            if subdomain is None:
                return None
            return Network.objects.get(name=subdomain)
        
    def get_context_data(self, **kwargs):
        context = super(NetworkView, self).get_context_data(**kwargs)
        network = self.get_object()
        content = []
        for well in network.well_set.all():
            pos = well.latlon()
            content.append({
                            'name': well.name,
                            'lat': pos.y,
                            'lon': pos.x,
                            'info': render_to_string('gorinchem/well_info.html', {'object': well, 
                                                                                  #'chart': make_encoded_chart(well),
                                                                                  'chart': None if well.chart.name is None else well.chart.url,
                                                                                  })
                            })
        context['content'] = json.dumps(content)
        context['maptype'] = 'HYBRID'
        return context
        
class ScreenChartView(TemplateView):
    template_name = 'gorinchem/plain_chart.html'
    
    def get_context_data(self, **kwargs):
        context = super(ScreenChartView, self).get_context_data(**kwargs)
        filt = Screen.objects.get(pk=context['pk'])
        name = unicode(filt)
        data = filt.get_levels(ref='nap')
        options = {
            'chart': {'type': 'line', 'animation': False, 'zoomType': 'x'},
            'title': {'text': name},
            'xAxis': {'type': 'datetime'},
            'yAxis': [{'title': {'text': 'm'}}
                      ],
            'tooltip': {'valueSuffix': ' m tov NAP',
                        'valueDecimals': 2,
                        'shared': True,
                       }, 
            'legend': {'enabled': False},
            'plotOptions': {'line': {'marker': {'enabled': False}}},            
            'credits': {'enabled': True, 
                        'text': 'acaciawater.com', 
                        'href': 'http://www.acaciawater.com',
                       },
            'series': [{'name': name,
                        'type': 'line',
                        'data': data
                        },
                       ]
            }
            
        context['options'] = json.dumps(options, default=lambda x: int(time.mktime(x.timetuple())*1000))
        context['screen'] = filt
        return context

class WellChartView(TemplateView):
    template_name = 'gorinchem/plain_chart.html'
    
    def get_context_data(self, **kwargs):
        context = super(WellChartView, self).get_context_data(**kwargs)
        well = Well.objects.get(pk=context['pk'])
        name = unicode(well)
        options = {
             'rangeSelector': { 'enabled': True,
                               'inputEnabled': True,
                               },
            'navigator': {'adaptToUpdatedData': True, 'enabled': True},
            'chart': {'type': 'arearange', 'zoomType': 'x'},
            'title': {'text': name},
            'xAxis': {'type': 'datetime'},
            'yAxis': [{'title': {'text': 'm tov NAP'}}
                      ],
            'tooltip': {'valueSuffix': ' m',
                        'valueDecimals': 2,
                        'shared': True,
                       }, 
            'legend': {'enabled': True},
            'plotOptions': {'line': {'marker': {'enabled': False}}},            
            'credits': {'enabled': True, 
                        'text': 'acaciawater.com', 
                        'href': 'http://www.acaciawater.com',
                       },
            }
        series = []
        xydata = []
        for screen in well.screen_set.all():
            name = unicode(screen)
            data = screen.to_pandas(ref='nap')
            xydata = zip(data.index.to_pydatetime(), data.values)
            series.append({'name': name,
                        'type': 'line',
                        'data': xydata,
                        'zIndex': 1,
                        })
            mean = pd.expanding_mean(data)
#             series.append({'name': 'gemiddelde',
#                         'type': 'line',
#                         'data': zip(mean.index.to_pydatetime(), mean.values),
#                         'linkedTo' : ':previous',
#                         })
            std = pd.expanding_std(data)
            a = (mean - std).dropna()
            b = (mean + std).dropna()
            ranges = zip(a.index.to_pydatetime(), a.values, b.values)
            series.append({'name': 'spreiding',
                        'data': ranges,
                        'type': 'arearange',
                        'lineWidth': 0,
                        'fillOpacity': 0.2,
                        'linkedTo' : ':previous',
                        'zIndex': 0,
                        })

        if len(xydata)>0:
            mv = []
            for i in range(len(xydata)):
                mv.append((xydata[i][0], screen.well.maaiveld))
            series.append({'name': 'maaiveld',
                        'type': 'line',
                        'data': mv
                        })

        options['series'] = series
        context['options'] = json.dumps(options, default=lambda x: int(time.mktime(x.timetuple())*1000))
        context['object'] = well
        return context
