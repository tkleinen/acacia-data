'''
Created on Sep 4, 2015

@author: theo
'''

import os,math
from django.utils.text import slugify
from django.conf import settings
from iom.models import Meetpunt
from acacia.data.models import Chart

def distance(obj, pnt):
    dx = obj.location.x - pnt.x
    dy = obj.location.y - pnt.y
    return math.sqrt(dx*dx+dy*dy)

def closest_object(query,target):
    closest = None
    dist = 1e99
    for obj in query:
        d = distance(obj, target)
        if d < dist:
            closest = obj
            dist = d
    return closest

def sort_objects(query,target):
    objs = []
    for obj in query:
        obj.distance = distance(obj, target)
        objs.append(obj)
    return sorted(objs, key=lambda x: x.distance)

def zoek_meetpunten(target, tolerance=1.0):
    mps = sort_objects(Meetpunt.objects.all(), target)
    return [m for m in mps if m.distance < tolerance]

def zoek_tijdreeksen(target,tolerance=1.0):
    ''' haal alle tijdreeksen op rond een locatie '''
    mps = zoek_meetpunten(target, tolerance)
    series = []
    for mp in mps:
        series.extend(mp.series())
    return series

import matplotlib.pyplot as plt
import pandas as pd

def maak_meetpunt_thumbnail(meetpunt):
    
    imagefile = os.path.join(meetpunt.chart_thumbnail.field.upload_to,slugify(unicode(meetpunt.identifier))+'.png')
    imagepath = os.path.join(settings.MEDIA_ROOT,imagefile)
    imagedir = os.path.dirname(imagepath)
    if not os.path.exists(imagedir):
        os.makedirs(imagedir)
    
    meetpunt.chart_thumbnail.name = imagefile
    
    plt.figure(figsize=(9,3))
    options = {'grid': False, 'legend': True, 'title': 'Meetpunt {num}'.format(num=meetpunt)}

    mps = zoek_meetpunten(meetpunt.location, 1)
    for mp in mps:
        s = mp.get_series('EC')
        if s:
            s =s.to_pandas()
            s.name = 'ondiep' if s.name.endswith('o') else 'diep'
            ax=s.plot(**options)
            ax.set_ylabel('EC')
    plt.savefig(imagepath)
    
    plt.close()
    
    meetpunt.save()

def maak_meetpunt_grafiek(meetpunt,user):
    try:
        chart = meetpunt.chart
    except Exception as e:
        chart = None

    if chart is None:
        name = meetpunt.name
        chart, created = Chart.objects.get_or_create(name = name, defaults = {
                                                             'user': user, 
                                                             'title': 'Meetpunt %s' % (meetpunt.name), 
                                                             'description': unicode(meetpunt.waarnemer)})
        meetpunt.chart=chart
        meetpunt.save()
                                                             
    series = zoek_tijdreeksen(meetpunt.location,1)
    for s in series:
        pos, ax = ('l', 1) if s.name.startswith('EC') else ('r', 2)
        cs, created = chart.series.get_or_create(series=s, defaults={'name': s.name, 'axis': ax, 'axislr': pos, 'type': s.type})
    chart.save()
    
    maak_meetpunt_thumbnail(meetpunt)
    