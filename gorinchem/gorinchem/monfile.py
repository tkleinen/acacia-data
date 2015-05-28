# -*- coding: UTF-8 -*-
'''
Created on Feb 9, 2015

@author: theo
'''

from acacia.data.generators import sws
from models import Network, MonFile, Channel, Datalogger, LoggerDatasource
from acacia.data.models import SourceFile

import datetime
import re, binascii
import StringIO
from django.core.files.base import ContentFile

def create(source, generator=sws.Diver()):
    ''' create sourcefile instance for monfile '''
    headerdict = generator.get_header(source)
    mon = MonFile()
    header = headerdict['HEADER']
    mon.company = header.get('COMPANY',None)
    mon.compstat = header.get('COMP.STATUS',None)
    if 'DATE' in header and 'TIME' in header:
        dt = header.get('DATE') + ' ' + header.get('TIME')
        mon.date = datetime.datetime.strptime(dt,'%d/%m/%Y %H:%M:%S')
    else:
        mon.date = datetime.datetime.now()
    mon.monfilename = header.get('FILENAME',None)
    mon.createdby = header.get('CREATED BY',None)
    mon.num_points = int(header.get('Number of points','0'))
    
    s = headerdict['Logger settings']
    mon.instrument_type = s.get('Instrument type',None)
    mon.status = s.get('Status',None)
    serial = s.get('Serial number',None)
    if serial is not None:
        serial = re.split(r'[-\s+]',serial)[1]
    mon.serial_number = serial
    mon.instrument_number = s.get('Instrument number',None)
    mon.location = s.get('Location',None)
    mon.sample_period = s.get('Sample period',None)
    mon.sample_method = s.get('Sample method','T')
    mon.num_channels = int(s.get('Number of channels','1'))

    s = headerdict['Series settings']
    mon.start_date = datetime.datetime.strptime(s['Start date / time'],'%H:%M:%S %d/%m/%y')    
    mon.end_date = datetime.datetime.strptime(s['End date / time'], '%H:%M:%S %d/%m/%y')    

    channels = []
    for i in range(mon.num_channels):
        channel = Channel(number = i+1)
        name = 'Channel %d' % (i+1)
        s = headerdict[name]
        channel.identification = s.get('Identification',name)
        t = s.get('Reference level','0 -')
        channel.reference_level, channel.reference_unit = re.split(r'\s+',t)
        channel.range, channel.range_unit = re.split(r'\s+', s.get('Range','0 -'))

        # omit degree symbol
        channel.reference_unit= ''
        channel.range_unit= ''
        
        channels.append(channel)
    return (mon, channels)

def save(request,f,net=-1):
    #contents = f.read().decode('ISO-8859-1') # needed for degree symbol
    contents = f.read()
    io = StringIO.StringIO(contents)
    mon, channels = create(io)
    serial = mon.serial_number
    try:
        logger = Datalogger.objects.get(serial=serial)
        ds = LoggerDatasource.objects.get(logger=logger)
        if net > 0:
            # validate if logger exists in network
            try:
                network = logger.screen.well.network
            except:
                # logger not installed in a well
                project = ds.project()
                network = Network.objects.get(name=project.name)
            if network.id != net:
                raise Exception('Datalogger %s is geregistreerd in een ander meetnet (%s)' % (serial,network))
        mon1 = ds.sourcefiles.get(name=f.name)
        return (mon1, False)
    except Network.DoesNotExist:
        raise Exception('Onbekend meetnet')
    except Datalogger.DoesNotExist:
        raise Exception('Datalogger %s is onbekend' % serial)
    except LoggerDatasource.DoesNotExist:
        raise Exception('Gegevensbron voor datalogger %s is onbekend' % serial)
    except SourceFile.DoesNotExist:
        mon.crc = abs(binascii.crc32(contents))
        try:
            mon1 = ds.sourcefiles.get(crc=mon.crc)
            return (mon1, False)
        except SourceFile.DoesNotExist:
            mon.name = mon.filename = f.name
            mon.datasource = ds
            mon.user = ds.user
            mon.file.save(name=f.name, content=ContentFile(contents))
            mon.get_dimensions()
            mon.save()
            mon.channel_set.add(*channels)
            return (mon, True)
