'''
Created on Mar 24, 2015

@author: theo
'''
from acacia.meetnet.views import NetworkView
from acacia.meetnet.models import Network, Datalogger, LoggerDatasource, LoggerPos
from acacia.data.models import MeetLocatie, Generator, SourceFile
import monfile

from django.shortcuts import render, redirect, render_to_response
from django.core.files.base import ContentFile

import StringIO, binascii
 
class HomeView(NetworkView):
    def get_object(self):
        return Network.objects.get(name = 'Molenwaard')

def addmon(request,f):
    user = request.user
    generator = Generator.objects.get(name='Schlumberger')
    
    contents = f.read() 
    io = StringIO.StringIO(contents)

    mon, channels = monfile.create(io)
    mon.user = user
    serial = mon.serial_number

    logger, new_logger = Datalogger.objects.get_or_create(serial=serial,defaults={'model': mon.instrument_type})
    pos, new_pos = logger.loggerpos_set.get_or_create(start_date=mon.start_date,end_date=mon.end_date)
    if new_pos:
        # let user fill in screen, refpnt and baro
        pass

    loc = MeetLocatie.objects.get(name=unicode(pos.screen))
    
    # get/create datasource for logger
    ds, new_ds = LoggerDatasource.objects.get_or_create(name=serial,meetlocatie=loc,
                                                         defaults = {'logger': logger, 'generator': generator, 'user': user, 'timezone': 'CET'})
    
    mon.crc = abs(binascii.crc32(contents))
    try:
        ds.sourcefiles.get(crc=mon.crc)
    except SourceFile.DoesNotExist:
        # add source file
        mon.name = mon.filename = f.name
        mon.datasource = ds
        mon.user = ds.user
        contentfile = ContentFile(contents)
        mon.file.save(name=mon.name, content=contentfile)
        mon.get_dimensions()
        mon.save()
        mon.channel_set.add(*channels)
        pos.monfile_set.add(mon)

        print pos.screen, serial, mon.num_points, mon.start_date, mon.end_date

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadForm1(request.POST, request.FILES)
#         if form.is_valid():
#             #handle_uploaded_file(request.FILES['file'])
#             for f in form.files.getlist('filename'):
#                 addmon(request,f)
#             return redirect('/success/url/')
#     else:
#         form = UploadForm1()
#     return render(request,'upload.html', {'form': form})


from forms import UploadForm1, UploadForm2, LoggerPosForm
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class UploadWizardView(SessionWizardView):
    form_list = [UploadForm2,UploadForm1]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'mon'))
        
    def done(self, form_list, **kwargs):
        return render_to_response('upload_done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
