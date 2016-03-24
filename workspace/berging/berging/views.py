'''
Created on Sep 1, 2014

@author: theo
'''
import os,json
import numpy as np
import pandas as pd

from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse
from forms import ScenarioForm,Scenario2Form,Scenario3Form
from models import Matrix, Gift, Scenario
from django.conf import settings
from django.contrib.gis.geos import Point
from .util import OgrInspector

def home(request):
    return render_to_response('home.html')

def select(request):
    return render_to_response('google_select.html')

inspector = OgrInspector()

def query(request):
    ''' Bevraag shapefile met grondsoort, kwel, weerstand deklaag en zout/zout '''
    
    lon = float(request.GET.get('lon'))
    lat = float(request.GET.get('lat'))

    # store in session
    request.session['lon'] = lon
    request.session['lat'] = lat
    
    # shapefile is in RD coordinates, transform
    p = Point((lon,lat),srid=4326)
    p.transform(28992)
    
    if inspector.isclosed():
        # open lazy
        inspector.open(settings.SHAPEFILE)
    return HttpResponse(json.dumps(inspector.inspect(p)), content_type='application/json')

def getseries2(scenario, matrix):
    ''' Haal tijdreeks op uit matrix (neem rij of kolom)'''
    df = matrix.data
    drow = (matrix.rijmax - matrix.rijmin) / (df.shape[0]-1)
    dcol = (matrix.kolmax - matrix.kolmin) / (df.shape[1]-1)

    if scenario.reken == 'v':
        labels = df.index
        index = (scenario.bassin/25000 - matrix.kolmin) / dcol
        data = df[df.columns[int(index)]].values
        series = pd.Series(data,index=labels,name=matrix.code)
    else:
        labels = df.columns
        index = (scenario.perceel - matrix.rijmin) / drow 
        data = df.iloc[int(index)].values
        series = pd.Series(data,index=labels,name=matrix.code)
    return series

def getdata(scenario):
    ''' Haal alle tijdreeksen op voor een scenario '''

    #watertekort
    code1 = scenario.matrix_code()
    matrix1 = get_object_or_404(Matrix,code=code1)
    tekort = getseries2(scenario, matrix1)

    #watervraag
    gift = get_object_or_404(Gift,gewas=scenario.gewas,grondsoort=scenario.grondsoort)
    vraag = pd.Series(data=np.ones(tekort.shape[0])*gift.gift, index=tekort.index)
    
    #beschiklbare waterhoeveelheid zonder bassin
    nul = matrix1.data.iloc[0,0]
    water0 = vraag - pd.Series(data=np.ones(vraag.shape[0]) * nul, index=vraag.index)
    
    #verdamping: eact/epot
    code2 = 'op' + code1
    matrix2 = get_object_or_404(Matrix,code=code2)
    verdamping = getseries2(scenario, matrix2)
    
    #opbrengst in euros
    opbrengst = matrix2.maxopbrengst - (1.0-verdamping) * 100.0 * matrix2.factor
    
    #opbrengst in nulsituatie (zonder bassin)
    nul = matrix2.maxopbrengst - (1.0-matrix2.data.iloc[0,0]) * 100.0 * matrix2.factor
    nulopbrengst = pd.Series(data=np.ones(opbrengst.shape[0]) * nul, index=opbrengst.index)


    scenario.data = pd.DataFrame({
                                  'tekort': tekort, 
                                  'vraag':vraag, 
                                  'verdamping':verdamping, 
                                  'opbrengst': opbrengst, 
                                  'nulopbrengst': nulopbrengst,
                                  'water0': water0
                                  })
    return scenario.data

def waterchart(scenario):
    if scenario.reken == 'v':
        subtitle = 'Volume bassin = %g m3' % scenario.bassin 
    else:
        subtitle = 'Oppervlakte perceel = %g Ha' % scenario.perceel
    options = {
        'chart': {'type': 'line', 'animation': False, 'zoomType': 'x'},
        'title': {'text': 'Watergift'},
        'subtitle':{'text': subtitle},
        'xAxis': {'title': {'enabled': True},
                  'labels': {'formatter': None} }, # formatter wordt aangepast in template
        'tooltip': {'valueSuffix': ' mm',
                    'shared': True,
                    'valueDecimals': 1,
#                    'pointFormat': '{series.name}: <b>{point.y:.1f} mm </b><br/>',
                    'crosshairs': [True,True],}, 
        'yAxis': [],
        'legend': {'enabled': True},#, 'layout': 'vertical', 'align': 'right', 'verticalAlign': 'top', 'y': 50},
        'plotOptions': {'line': {'marker': {'enabled': False}}},            
        'credits': {'enabled': False},
        }

    options['yAxis'].append({'alignTicks': False, 'min': 0, 'title': {'text': 'mm'},})
    
    tekort = scenario.data['tekort']
    vraag = scenario.data['vraag']
    water0 = scenario.data['water0']

    beschikbaarheid = vraag - tekort - water0
    vraag = vraag - water0
    
    x = vraag.index.values.astype('f8')
    
    if scenario.reken == 'o':
        x = (x * 25000).astype('i8') # Ha -> m3
        options['xAxis']['title']['text'] = 'Volume bassin (m3)'
        options['tooltip']['headerFormat'] = 'Volume: <b>{point.key} m3 </b><br/>'
    else:
        options['xAxis']['title']['text'] = 'Oppervlakte perceel (Ha)'
        options['tooltip']['headerFormat'] = 'Oppervlakte: <b>{point.key} Ha </b><br/>'
    
    options['series'] = [#{'name': 'Zonder bassin', 'type': 'line', 'data': zip(x,water0.values),'dashStyle': 'Dot'},
                         {'name': 'Watergift','type': 'line','data': zip(x,beschikbaarheid.values)},
                         {'name': 'Watervraag','type': 'line','data': zip(x,vraag.values), 'dashStyle': 'Dot'},
                         ]
    return json.dumps(options)

def getkosten2(scenario):
    irri = 'di' if scenario.irrigatie == 'p' else 'dr'
    series = { c: getseries(scenario, get_object_or_404(Matrix,code= c + 'b' + irri)) for c in 'ijt'}
    return pd.DataFrame(series)
    
def kostenchart(scenario):
    
    if scenario.reken == 'v':
        subtitle = 'Volume bassin = %g m3' % scenario.bassin 
    else:
        subtitle = 'Oppervlakte perceel = %g Ha' % scenario.perceel
    options = {
        'chart': {'type': 'line', 'animation': False, 'zoomType': 'x'},
        'title': {'text': 'Kosten'},
        'subtitle': {'text': subtitle},
        'xAxis': {'title': {'enabled': True},
                  'labels': {'formatter': None} }, # formatter wordt aangepast in template
        'tooltip': {'valueSuffix': ' euro',
                    'shared': True,
                    'valueDecimals': 0,
                    'crosshairs': [True,True],}, 
        'legend': {'enabled': True},
        'yAxis': [],               
        'plotOptions': {'line': {'marker': {'enabled': False}}},            
        'credits': {'enabled': False},
        }
    
    scenario.volume = scenario.bassin # Ha -> m3
    scenario.oppervlakte = scenario.perceel # in Ha
    
    cost = getkosten2(scenario)
    x = cost.index.values.astype('f8')
    #inv = cost['i'].values
    #jaar = cost['j'].values
    tot = cost['t'].values

    if scenario.reken == 'o':
        options['xAxis']['title']['text'] = 'Volume bassin (m3)'
        options['tooltip']['headerFormat'] = 'Volume: <b>{point.key} m3 </b><br/>'
    else:
        x = x / 10000.0 # m2 -> Ha
        options['xAxis']['title']['text'] = 'Oppervlakte perceel (Ha)'
        options['tooltip']['headerFormat'] = 'Oppervlakte: <b>{point.key} Ha </b><br/>'
    options['yAxis'].append({'title':{'text': 'euro/Ha'},
                             'labels':{'formatter': None}})
    options['series'] = [
                     {'name': 'Kosten',
                      'type': 'line',
                      'data': zip(x, tot),
                      'tooltip': {'valueSuffix': ' euro/Ha','shared': True},
                     },
                    ]
    return json.dumps(options)

def opbrengstchart(scenario):
    if scenario.reken == 'v':
        subtitle = 'Volume bassin = %g m3' % scenario.bassin 
    else:
        subtitle = 'Oppervlakte perceel = %g Ha' % scenario.perceel
    options = {
        'chart': {'type': 'line', 'animation': False, 'zoomType': 'x'},
        'title': {'text': 'Opbrengst'},
        'subtitle':{'text': subtitle},
        'xAxis': {'title': {'enabled': True},
                  'labels': {'formatter': None} }, # formatter wordt aangepast in template
        'tooltip': {'valueSuffix': ' euro/Ha',
                    'shared': True,
                    'valueDecimals': 0,
                    'crosshairs': [True,True],}, 
        'yAxis': [],
        'legend': {'enabled': True},#, 'layout': 'vertical', 'align': 'right', 'verticalAlign': 'top', 'y': 50},
        'plotOptions': {'line': {'marker': {'enabled': False}}},            
        'credits': {'enabled': False},
        }

    options['yAxis'].append({'alignTicks': False, 'title': {'text': 'euro/Ha'}, 'labels':{'formatter': None}})
    
    opbrengst = scenario.data['opbrengst']
    nulopbrengst = scenario.data['nulopbrengst']

    x = opbrengst.index.values.astype('f8')

    if scenario.reken == 'o':
        x = (x * 25000).astype('i8') # Ha -> m3
        options['xAxis']['title']['text'] = 'Volume bassin (m3)'
        options['tooltip']['headerFormat'] = 'Volume: <b>{point.key} m3 </b><br/>'
    else:
        options['xAxis']['title']['text'] = 'Oppervlakte perceel (Ha)'
        options['tooltip']['headerFormat'] = 'Oppervlakte: <b>{point.key} Ha </b><br/>'

    options['series'] = [
                         {'name': 'Met bassin','type': 'line','data': zip(x,opbrengst.values)},
                         {'name': 'Zonder bassin', 'type': 'line', 'data': zip(x,nulopbrengst.values), 'dashStyle': 'Dot'},
                         ]
    return json.dumps(options)

def scenario2(request):
    chart1, chart2, chart3 = (None,None,None)
    if request.method == 'POST':
        form = Scenario2Form(request.POST)
        if form.is_valid():
            scenario = form.save(commit=False)
            request.session['scenario'] = scenario.id
            
            getdata(scenario)

            chart1 = waterchart(scenario)
            chart2 = kostenchart(scenario)
            chart3 = opbrengstchart(scenario)
    else:
#         if 'scenario' in request.session:
#             scenario_id = int(request.session.get('scenario'))
#             scenario = Scenario.objects.get(pk=scenario_id)
#             form = Scenario2Form(instance=scenario)
#         else:
            form = Scenario2Form()

    return render(request, 'scenario2.html', {'form': form,
            'chart1': chart1,
            'chart2': chart2,
            'chart3': chart3},
            context_instance = RequestContext(request))

def waterchart3(scenario):
    if scenario.reken == 'o':
        if scenario.opslag == 'o': # ondergronds
            subtitle = 'Oppervlakte ondergrondse opslag = %g Ha' % scenario.oppervlakte 
        else:
            subtitle = 'Volume bassin = %g m3' % scenario.bassin 
    else:
        subtitle = 'Oppervlakte perceel = %g Ha' % scenario.perceel
    options = {
        'chart': {'type': 'line', 'animation': False, 'zoomType': 'x'},
        'title': {'text': 'Watergift'},
        'subtitle':{'text': subtitle},
        'xAxis': {'title': {'enabled': True},
                  'labels': {'formatter': None} }, # formatter wordt aangepast in template
        'tooltip': {'valueSuffix': ' mm',
                    'shared': True,
                    'valueDecimals': 1,
#                    'pointFormat': '{series.name}: <b>{point.y:.1f} mm </b><br/>',
                    'crosshairs': [True,True],}, 
        'yAxis': [],
        'legend': {'enabled': True},#, 'layout': 'vertical', 'align': 'right', 'verticalAlign': 'top', 'y': 50},
        'plotOptions': {'line': {'marker': {'enabled': False}}},            
        'credits': {'enabled': False},
        }

    options['yAxis'].append({'alignTicks': False, 'min': 0, 'title': {'text': 'mm'},})
    
    tekort = scenario.data['tekort']
    vraag = scenario.data['vraag']

    beschikbaarheid = vraag - tekort
    
    x = vraag.index.values.astype('f8')
    
    if scenario.reken == 'p':
        if scenario.opslag == 'o':
            options['xAxis']['title']['text'] = 'Oppervlakte (Ha)'
            options['tooltip']['headerFormat'] = 'Oppervlakte: <b>{point.key} Ha </b><br/>'
        else:
            options['xAxis']['title']['text'] = 'Volume bassin (m3)'
            options['tooltip']['headerFormat'] = 'Volume: <b>{point.key} m3 </b><br/>'
    else:
        options['xAxis']['title']['text'] = 'Oppervlakte perceel (Ha)'
        options['tooltip']['headerFormat'] = 'Oppervlakte: <b>{point.key} Ha </b><br/>'


    options['series'] = [
                         {'name': 'Watergift','type': 'line','data': zip(x,beschikbaarheid.values)},
                         {'name': 'Watervraag','type': 'line','data': zip(x,vraag.values), 'dashStyle': 'Dot'},
                         ]
    return json.dumps(options)

def opbrengstchart3(scenario):
    if scenario.reken == 'o':
        if scenario.opslag == 'o':
            subtitle = 'Oppervlakte ondergrondse opslag = %g Ha' % scenario.oppervlakte 
        else:
            subtitle = 'Volume bassin = %g m3' % scenario.bassin 
    else:
        subtitle = 'Oppervlakte perceel = %g Ha' % scenario.perceel

    options = {
        'chart': {'type': 'line', 'animation': False, 'zoomType': 'x'},
        'title': {'text': 'Opbrengst'},
        'subtitle':{'text': subtitle},
        'xAxis': {'title': {'enabled': True},
                  'labels': {'formatter': None} }, # formatter wordt aangepast in template
        'tooltip': {'valueSuffix': ' euro/Ha',
                    'shared': True,
                    'valueDecimals': 0,
                    'crosshairs': [True,True],}, 
        'yAxis': [],
        'legend': {'enabled': True},#, 'layout': 'vertical', 'align': 'right', 'verticalAlign': 'top', 'y': 50},
        'plotOptions': {'line': {'marker': {'enabled': False}}},            
        'credits': {'enabled': False},
        }

    options['yAxis'].append({'alignTicks': False, 'title': {'text': 'euro/Ha'}, 'labels':{'formatter': None}})
    
    opbrengst = scenario.data['opbrengst']

    x = opbrengst.index.values.astype('f8')

    if scenario.reken == 'p':
        if scenario.opslag == 'o':
            options['xAxis']['title']['text'] = 'Oppervlakte (Ha)'
            options['tooltip']['headerFormat'] = 'Oppervlakte: <b>{point.key} Ha </b><br/>'
        else:
            options['xAxis']['title']['text'] = 'Volume bassin (m3)'
            options['tooltip']['headerFormat'] = 'Volume: <b>{point.key} m3 </b><br/>'
    else:
        options['xAxis']['title']['text'] = 'Oppervlakte perceel (Ha)'
        options['tooltip']['headerFormat'] = 'Oppervlakte: <b>{point.key} Ha </b><br/>'

    options['series'] = [
                         {'name': 'Opbrengst','type': 'line','data': zip(x,opbrengst.values)},
                         ]
    return json.dumps(options)

def getseries3(scenario, matrix):
    ''' Haal tijdreeks op uit matrix (neem rij of kolom)'''
    df = matrix.data
    drow = (matrix.rijmax - matrix.rijmin) / (df.shape[0]-1)
    dcol = (matrix.kolmax - matrix.kolmin) / (df.shape[1]-1)

    if scenario.reken == 'o': # opslag vast, perceelsgrootte varieert
        labels = df.columns
        if scenario.opslag == 'o': # ondergronds
            index = (scenario.oppervlakte - matrix.rijmin) / drow
        else: # bassin
            index = (scenario.bassin/25000 - matrix.rijmin) / drow
        data = df.iloc[int(index)].values
        series = pd.Series(data,index=labels,name=matrix.code)
    else: # perceel vast
        labels = df.index
        index = (scenario.perceel - matrix.kolmin) / dcol 
        data = df[df.columns[int(index)]].values
        series = pd.Series(data,index=labels,name=matrix.code)
    return series

def getdata3(scenario):
    ''' Haal alle tijdreeksen op voor een scenario '''

    #watertekort
    code1 = scenario.matrix_code()
    matrix1 = get_object_or_404(Matrix,code=code1)
    tekort = getseries3(scenario, matrix1)

    #watervraag (constant)
    gift = get_object_or_404(Gift,gewas=scenario.gewas,grondsoort=scenario.grondsoort)
    vraag = pd.Series(data=np.ones(tekort.shape[0])*gift.gift, index=tekort.index)
    
    #verdamping: eact/epot
    code2 = 'op' + code1
    matrix2 = get_object_or_404(Matrix,code=code2)
    verdamping = getseries3(scenario, matrix2)
    
    #opbrengst in euros
    opbrengst = matrix2.maxopbrengst - (1.0-verdamping) * 100.0 * matrix2.factor
    
    scenario.data = pd.DataFrame({
                                  'tekort': tekort, 
                                  'vraag':vraag, 
                                  'verdamping':verdamping, 
                                  'opbrengst': opbrengst, 
                                  })
    return scenario.data

def scenario3(request):
    chart1, chart2, chart3 = (None,None,None)
    if request.method == 'POST':
        form = Scenario3Form(request.POST)
        if form.is_valid():
            scenario = form.save(commit=False)
            request.session['scenario'] = scenario.id
            getdata3(scenario)
            chart1 = waterchart3(scenario)
            chart3 = opbrengstchart3(scenario)
                
    else:
            form = Scenario3Form()

    return render(request, 'scenario3.html', {'form': form,
            'chart1': chart1,
            'chart2': chart2,
            'chart3': chart3},
            context_instance = RequestContext(request))

# OUDE WEBSITE HIERONDER
    
def scenario_highchart(request):
    chart1 = None
    chart2 = None
    if request.method == 'POST':
        form = ScenarioForm(request.POST)
        if form.is_valid():
            scenario = form.save(commit=False)
            chart1 = make_chart(scenario)
            chart2 = make_costchart(scenario)
    else:
        form = ScenarioForm()

    toelichting = { 
                   'id_bodem': render_to_string('bodem.html',{'image': "img/grondsoort2.png", 'url': '/grondsoort'}),    
                   'id_neerslag': render_to_string('neerslag.html',{'image': "img/neerslag.jpg"}),
                   'id_kwaliteit': render_to_string('kwaliteit.html',{'image': 'img/zzhhnk.jpeg'}),
                   'id_irrigatie': render_to_string('irrigatie.html',{'image': 'img/irri1.jpg'}),
                   'id_reken': render_to_string('rekenopties.html',{'image': None})
                   }
    return render(request, 'scenario_highchart.html', {
            'form': form, 
            'toelichting': json.dumps(toelichting), 
            'chart1': chart1,
            'chart2': chart2})

def getseries(scenario, matrix):
    df = pd.read_csv(matrix.file.path,index_col=0)
    drow = (matrix.rijmax - matrix.rijmin) / (df.shape[0]-1)
    dcol = (matrix.kolmax - matrix.kolmin) / (df.shape[1]-1)

    if scenario.reken == 'v':
        labels = df.index
        index = (scenario.volume - matrix.kolmin) / dcol # naar beneden afronden
        data = df[df.columns[int(index)]].values
        series = pd.Series(data,index=labels,name=matrix.code)
    else:
        labels = df.columns
        index = (scenario.oppervlakte*10000 - matrix.rijmin) / drow # Ha -> m2
        data = df.iloc[int(index)].values
        series = pd.Series(data,index=labels,name=matrix.code)
    return series

def getresult(scenario):
    code = scenario.matrix_code()+ 'g'  # gemiddeld
    matrix = get_object_or_404(Matrix,code=code)
    return getseries(scenario, matrix)

def getkosten(scenario):
    irri = 'di' if scenario.irrigatie == 'i' else 'dr'
    series = { c: getseries(scenario, get_object_or_404(Matrix,code= c + 'b' + irri)) for c in 'ijt'}
    return pd.DataFrame(series)

# referentiewaarden voor neerslagtekort voor droog, gemiddeld en nat 
P_REF = {'d': 202, 'g': 192, 'n': 182}

def make_chart(scenario):
    if scenario.reken == 'v':
        subtitle = 'Volume bassin = %g m3' % scenario.volume 
    else:
        subtitle = 'Oppervlakte perceel = %g Ha' % scenario.oppervlakte
    options = {
        'chart': {'type': 'line', 'animation': False, 'zoomType': 'x'},
        'title': {'text': 'Watergift'},
        'subtitle':{'text': subtitle},
        'xAxis': {'title': {'enabled': True},
                  'labels': {'formatter': None} }, # formatter wordt aangepast in template
        'tooltip': {'valueSuffix': ' mm',
                    'shared': True,
                    'valueDecimals': 1,
#                    'pointFormat': '{series.name}: <b>{point.y:.1f} mm </b><br/>',
                    'crosshairs': [True,True],}, 
        'yAxis': [],
        'legend': {'enabled': True},#, 'layout': 'vertical', 'align': 'right', 'verticalAlign': 'top', 'y': 50},
        'plotOptions': {'line': {'marker': {'enabled': False}}},            
        'credits': {'enabled': False},
        }

    options['yAxis'].append({'min': 0, 'max': 250, 'alignTicks': False, 'title': {'text': 'Watergift (mm)'},})
    
    data = getresult(scenario)
    pref = np.ones(data.shape[0]) * P_REF[scenario.neerslag]
    x = data.index.values.astype('f8')
    y = pref - data.values

    if scenario.reken == 'o':
        options['xAxis']['title']['text'] = 'Volume bassin (m3)'
        options['tooltip']['headerFormat'] = 'Volume: <b>{point.key} m3 </b><br/>'
    else:
        x = x / 10000.0 # m2 -> Ha
        options['xAxis']['title']['text'] = 'Oppervlakte (Ha)'
        options['tooltip']['headerFormat'] = 'Oppervlakte: <b>{point.key} Ha </b><br/>'
    
    options['series'] = [{'name': 'Optimale watergift','type': 'line','data': zip(x,pref), 'dashStyle': 'Dot'},
                         {'name': 'Beschikbare watergift','type': 'line','data': zip(x,y)},]
    return json.dumps(options)

def make_costchart(scenario):
    if scenario.reken == 'v':
        subtitle = 'Volume bassin = %g m3' % scenario.volume 
    else:
        subtitle = 'Oppervlakte perceel = %g Ha' % scenario.oppervlakte
    options = {
        'chart': {'type': 'line', 'animation': False, 'zoomType': 'x'},
        'title': {'text': 'Kosten'},
        'subtitle': {'text': subtitle},
        'xAxis': {'title': {'enabled': True},
                  'labels': {'formatter': None} }, # formatter wordt aangepast in template
        'tooltip': {'valueSuffix': ' euro',
                    'shared': True,
                    'valueDecimals': 0,
                    'crosshairs': [True,True],}, 
        'yAxis': [],               
        'legend': {'enabled': True},#, 'layout': 'vertical', 'align': 'right', 'verticalAlign': 'top', 'y': 50},
        'plotOptions': {'line': {'marker': {'enabled': False}}},            
        'credits': {'enabled': False},
        }
    
    cost = getkosten(scenario)
    x = cost.index.values.astype('f8')
    inv = cost['i'].values
    #jaar = cost['j'].values
    tot = cost['t'].values

    if scenario.reken == 'o':
        options['xAxis']['title']['text'] = 'Volume bassin (m3)'
        options['tooltip']['headerFormat'] = 'Volume: <b>{point.key} m3 </b><br/>'
    else:
        x = x / 10000.0 # m2 -> Ha
        options['xAxis']['title']['text'] = 'Oppervlakte (Ha)'
        options['tooltip']['headerFormat'] = 'Oppervlakte: <b>{point.key} Ha </b><br/>'
    options['yAxis'].append({'title':{'text': 'Kosten (euro/Ha/jaar)'},
                             'labels':{'formatter': None}})
    options['yAxis'].append({'opposite': True, 
                             'title':{'text': 'Investering (euro)'},
                             'labels':{'formatter': None}})
    options['series'] = [
                     {'name': 'Inversteringskosten',
                      'type': 'line',
                      'data': zip(x, inv),
                      'yAxis': 1},
                     {'name': 'Totale kosten',
                      'type': 'line',
                      'data': zip(x, tot),
                      'tooltip': {'valueSuffix': ' euro/Ha/jaar','shared': True},}
                    ]
    return json.dumps(options)

def grondsoort(request):
    # TODO: load json with in template using .ajax
    path = os.path.join(settings.MEDIA_ROOT, 'maps', 'nhgrond2m.geojson')
    with open(path) as f:
        return render_to_response('leaflet_grondsoort.html',{'grondsoort': f.read()})
