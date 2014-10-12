'''
Created on Sep 1, 2014

@author: theo
'''
import os,json
import numpy as np
import pandas as pd

from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.loader import render_to_string

import settings
from forms import ScenarioForm
from models import Matrix
    

def home(request):
    return render_to_response('home.html')

def grondsoort(request):
    # TODO: load json with in template using .ajax
    path = os.path.join(settings.MEDIA_ROOT, 'maps', 'nhgrond2m.geojson')
    with open(path) as f:
        return render_to_response('leaflet_grondsoort.html',{'grondsoort': f.read()})

def scenario_highchart(request):
    chart = None
    if request.method == 'POST':
        form = ScenarioForm(request.POST)
        if form.is_valid():
            scenario = form.save(commit=False)
            chart = make_highchart(scenario)
    else:
        form = ScenarioForm()

    toelichting = { 
                   'id_bodem': render_to_string('bodem.html',{'image': "img/grondsoort2.png", 'url': '/grondsoort'}),    
                   'id_neerslag': render_to_string('neerslag.html',{'image': "img/neerslag.jpg"}),
                   'id_kwaliteit': render_to_string('kwaliteit.html',{'image': 'img/zoetzout.jpg'}),
                   'id_irrigatie': render_to_string('irrigatie.html',{'image': 'img/irri1.jpg'}),
                   'id_reken': render_to_string('rekenopties.html',{'image': None})
                   }
    return render(request, 'scenario_highchart.html', {
            'form': form, 
            'toelichting': json.dumps(toelichting), 
            'chart': chart,
            'investering': 'onbekend',
            'afschrijving': 'onbekend',
            'prijs': 'onbekend'})

def getseries(scenario, matrix):
    df = pd.read_csv(matrix.file.path,index_col=0)
    drow = (matrix.rijmax - matrix.rijmin) / (df.shape[0]-1)
    dcol = (matrix.kolmax - matrix.kolmin) / (df.shape[1]-1)

    if scenario.reken == 'v':
        labels = df.index
        index = (scenario.volume - matrix.kolmin) / dcol # naar beneden afronden
        data = df[df.columns[int(index)]].values
        series = pd.Series(data,index=labels)
    else:
        labels = df.columns
        index = (scenario.oppervlakte*10000 - matrix.rijmin) / drow # Ha -> m2
        data = df.iloc[int(index)].values
        series = pd.Series(data,index=labels)
    return series

def getresult(scenario):
    code = scenario.matrix_code()+ 'g'  # gemiddeld
    matrix = get_object_or_404(Matrix,code=code)
    return getseries(scenario, matrix)

def getkosten(scenario):
    code = 'drip' if scenario.irrigatie == 'd' else 'di'
    matrix = get_object_or_404(Matrix,code=code)
    return getseries(scenario, matrix)
    
# referentiewaarden voor neerslagtekort 
P_REF = {'d': 202, 'g': 192, 'n': 182}

def make_highchart(scenario):
    if scenario.reken == 'v':
        title = 'Volume bassin = %g m3' % scenario.volume 
    else:
        title = 'Oppervlakte perceel = %g Ha' % scenario.oppervlakte
    options = {
        'chart': {'type': 'line', 'animation': False, 'zoomType': 'x'},
        'title': {'text': title},
        'xAxis': {'title': {'enabled': True},
                  'labels': {'formatter': None} }, # formatter wordt aangepast in template
        'tooltip': {'valueSuffix': ' mm',
                    'shared': True,
                    'valueDecimals': 1,
#                    'pointFormat': '{series.name}: <b>{point.y:.1f} mm </b><br/>',
                    'crosshairs': [True,True],}, 
        'yAxis': [],
        'legend': {'enabled': False},
        'plotOptions': {'line': {'marker': {'enabled': False}}},            
        'credits': {'enabled': False},
        }

    options['yAxis'].append({'min': 0, 'title': {'text': 'Neerslagtekort (mm)'},})
    options['yAxis'].append({'opposite': 1, 'title': {'text': 'Kosten (euro/m3)'},})
    
    data = getresult(scenario)
    x = data.index.values.astype('f8')
    y = data.values
    pref = np.ones(y.shape) * P_REF[scenario.neerslag]

    if scenario.reken == 'o':
        options['xAxis']['title']['text'] = 'Volume bassin (m3)'
        options['tooltip']['headerFormat'] = 'Volume: <b>{point.key} m3 </b><br/>'
    else:
        x = x / 10000.0 # m2 -> Ha
        options['xAxis']['title']['text'] = 'Oppervlakte (Ha)'
        options['tooltip']['headerFormat'] = 'Oppervlakte: <b>{point.key} Ha </b><br/>'
    
    options['series'] = [{'name': 'Neerslagtekort','type': 'line','data': zip(x,y)},
                         {'name': 'Referentie','type': 'line','data': zip(x,pref)}]
    try:
        cost = getkosten(scenario)
        euros = cost.values
        options['series'].append(
                         {'name': 'Kosten','type': 'line','yAxis': 1, 'data': zip(x,euros),
                          'tooltip': {'valueSuffix': ' euro/m3',
                                    'shared': True,
                                    'valueDecimals': 2}
                         })
    except:
        pass
    return json.dumps(options)
