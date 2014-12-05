'''
Created on Feb 12, 2014

@author: theo
'''
import os, fnmatch, re
from django.contrib.gis.gdal.srs import SpatialReference, CoordTransform
from django.contrib.gis.geos import Point


import logging
logger = logging.getLogger(__name__)

# EPSG codes
RDNEW=28992
RDOLD=28991
WEBMERC=3857
GOOGLE=900913
AMERSFOORT=4289
WGS84=4326

def toGoogle(p):
    return trans(p,GOOGLE)

def toWGS84(p):
    return trans(p,WGS84)

def toRD(p):
    return trans(p,RDNEW)

def trans(p, srid):
    '''transform Point p to requested srid'''
    if not isinstance(p,Point):
        raise TypeError('django.contrib.gis.geos.Point expected')
    psrid = p.srid
    if not psrid:
        psrid = WGS84
    if (psrid != srid): 
        tr = CoordTransform(SpatialReference(p.srid), SpatialReference(srid))
        p.transform(tr)
    return p
