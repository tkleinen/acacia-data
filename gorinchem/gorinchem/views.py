'''
Created on Jun 3, 2014

@author: theo
'''
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import View, FormView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from django.contrib import messages
from gorinchem.models import Network, Well, Screen, LoggerDatasource
from acacia.data.models import Datasource, Formula
import json, logging, datetime, time, re
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.size'] = '8'
from StringIO import StringIO
import numpy as  np
import pandas as pd
from forms import UploadFileForm

logger = logging.getLogger('upload')
import monfile


class UploadDoneView(TemplateView):
    template_name = 'gorinchem/done.html'

    def get_context_data(self, **kwargs):
        context = super(UploadDoneView, self).get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        pk = self.kwargs.get('id')
        self.network = Network.objects.get(pk=pk)
        context['network'] = self.network
        if not 'request' in context:
            context['request'] = self.request
        return context

    
class UploadFileView(FormView):

    template_name = 'gorinchem/upload.html'
    form_class = UploadFileForm
    success_url = '/done/1'
    
    def get_success_url(self):
        return '/done/' + self.kwargs.get('id')

    def get_context_data(self, **kwargs):
        context = super(UploadFileView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('id')
        self.network = Network.objects.get(pk=pk)
        context['network'] = self.network
        return context

    def form_valid(self, form):
        monfiles = []
        netid = int(self.kwargs.get('id','1'))
        messages.set_level(self.request, messages.DEBUG)
        def msg(how, what):
            log = getattr(logger,how)
            log(what);
            mes = getattr(messages,how)
            mes(self.request,what)
        
        for f in form.files.getlist('filename'):
            try:
                msg('debug','Verwerking van MON file %s' % f.name)
                mon, saved = monfile.save(self.request,f,net=netid)
                if saved:
                    msg('info','Bestand toegevoegd: %s' % mon.file)
                    monfiles.append(mon)
                else:
                    msg('warning','Identiek bestand bestaat al: %s' % mon.file)
                    continue
            except Exception as e:
                msg('error',e)
                continue
            
        for mon in monfiles:
            # actualiseren PRESSURE tijdreeksen
            for s in mon.datasource.getseries():
                msg('debug','Tijdreeks actualiseren:  %s' % s)
                try:
                    s.update()
                except Exception as e:
                    msg('error','Fout bij actualisatie van tijdreeks %s: %s' %(s, e))

        locs = set([mon.meetlocatie() for mon in monfiles])
        for loc in locs:
            # dependent series (LEVEL) actualiseren voor alle geactualiseerde meetlocaties
            for fm in loc.formula_set.all():
                msg('debug','Berekenen van tijdreeks %s (%s)' % (fm,fm.locatie.name))
                try:
                    fm.update()
                except Exception as e:
                    msg('error','Fout bij berekening van tijdreeks %s: %s' % (fm, e))
                break
            
        return super(UploadFileView,self).form_valid(form)
        
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
        try:
            context['chart'] = well.chart.url
        except:
            context['chart'] = None 
        return context

class ScreenView(DetailView):
    model = Screen
    
    def get_context_data(self, **kwargs):
        context = super(ScreenView, self).get_context_data(**kwargs)
#        context['chart'] = make_encoded_chart(self.get_object())
        screen = self.get_object()
        try:
            context['chart'] = screen.chart.url
        except:
            context['chart'] = None 
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
            try:
                chart_url = well.chart.url
            except:
                chart_url = None 
            content.append({
                            'name': well.name,
                            'lat': pos.y,
                            'lon': pos.x,
                            'info': render_to_string('gorinchem/well_info.html', {'object': well, 
                                                                                  #'chart': make_encoded_chart(well),
                                                                                  'chart': chart_url,
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
