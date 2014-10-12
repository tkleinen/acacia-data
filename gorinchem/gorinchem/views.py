'''
Created on Jun 3, 2014

@author: theo
'''
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import DetailView, TemplateView
from django.template.loader import render_to_string
from gorinchem.models import Network, Well, Screen, DataPoint
import json, logging, datetime, re
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.size'] = '8'
from StringIO import StringIO

logger = logging.getLogger(__name__)
    
def chart_for_screen(screen):
    plt.figure(figsize=(15,5))
    plt.grid(linestyle='-', color='0.9')
    data = [(p.date, p.level) for p in screen.datapoint_set.all()]
    if len(data)>0:
        x,y = zip(*data)
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
    for screen in well.screen_set.all():
        data = [(p.date, p.level) for p in screen.datapoint_set.all()]
        if len(data)>0:
            x,y = zip(*data)
            plt.plot_date(x, y, '-', label=screen)
            count += 1
    plt.title(well)
    plt.ylabel('m tov NAP')
    if count > 0:
        plt.legend()
    #plt.legend(loc="upper left", bbox_to_anchor=(1,1.025))
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

class WellView(DetailView):
    template = 'gorinchem/well_info.html'
    model = Well

    def get_context_data(self, **kwargs):
        context = super(WellView, self).get_context_data(**kwargs)
        context['chart'] = make_encoded_chart(self.get_object())
        return context

class ScreenView(DetailView):
    model = Screen
    
    def get_context_data(self, **kwargs):
        context = super(ScreenView, self).get_context_data(**kwargs)
        context['chart'] = make_encoded_chart(self.get_object())
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
                                                                                  'chart': make_encoded_chart(well),
#                                                                                  'chart': well.chart,
                                                                                  })
                            })
        context['content'] = json.dumps(content)
        context['maptype'] = 'HYBRID'
        return context
        
def tojs(d):
    ''' python datetime to javascript '''
    return 'Date.UTC(%d,%d,%d,%d,%d,%d)' % (d.year, d.month-1, d.day, d.hour, d.minute, d.second)
 
def date_handler(obj):
    return tojs(obj) if isinstance(obj, datetime.date) or isinstance(obj, datetime.datetime) else obj

class ScreenChartView(TemplateView):
    template_name = 'gorinchem/plain_chart.html'
    
    def get_context_data(self, **kwargs):
        context = super(ScreenChartView, self).get_context_data(**kwargs)
        filt = Screen.objects.get(pk=context['pk'])
        name = unicode(filt)
        options = {
            'chart': {'type': 'line', 'animation': False, 'zoomType': 'x'},
            'title': {'text': name},
            'xAxis': {'type': 'datetime'},
            'yAxis': [{'title': {'text': 'm'}}
                      ],
            'tooltip': {'valueSuffix': ' m tov NAP',
                        'valueDecimals': 2
                       }, 
            'legend': {'enabled': False},
            'plotOptions': {'line': {'marker': {'enabled': False}}},            
            'credits': {'enabled': True, 
                        'text': 'acaciawater.com', 
                        'href': 'http://www.acaciawater.com',
                       },
            'series': [{'name': name,
                        'type': 'line',
                        'data': [[p.date,p.level] for p in filt.datapoint_set.all().order_by('date')]
                        },
                       ]
            }
            
        jop = json.dumps(options,default=date_handler)
        # remove quotes around date stuff
        jop = re.sub(r'\"(Date\.UTC\([\d,]+\))\"',r'\1', jop)
        context['options'] = jop
        return context

class WellChartView(TemplateView):
    template_name = 'gorinchem/plain_chart.html'
    
    def get_context_data(self, **kwargs):
        context = super(WellChartView, self).get_context_data(**kwargs)
        well = Well.objects.get(pk=context['pk'])
        name = unicode(well)
        options = {
            'chart': {'type': 'line', 'animation': False, 'zoomType': 'x'},
            'title': {'text': name},
            'xAxis': {'type': 'datetime'},
            'yAxis': [{'title': {'text': 'm tov NAP'}}
                      ],
            'tooltip': {'valueSuffix': ' m',
                        'valueDecimals': 2
                       }, 
            'legend': {'enabled': True},
            'plotOptions': {'line': {'marker': {'enabled': False}}},            
            'credits': {'enabled': True, 
                        'text': 'acaciawater.com', 
                        'href': 'http://www.acaciawater.com',
                       },
            }
        series = []
        for screen in well.screen_set.all():
            name = unicode(screen)
            series.append({'name': name,
                        'type': 'line',
                        'data': [[p.date,p.level] for p in screen.datapoint_set.all().order_by('date')]
                        })
        options['series'] = series
        jop = json.dumps(options,default=date_handler)
        # remove quotes around date stuff
        jop = re.sub(r'\"(Date\.UTC\([\d,]+\))\"',r'\1', jop)
        context['options'] = jop
        context['object'] = well
        return context
