'''
Created on Jul 8, 2014

@author: theo
'''
import os
from django.utils.text import slugify
from views import chart_for_well
import settings
 
def make_thumbnails(modeladmin, request, queryset):
    for w in queryset:
        if not w.has_data:
            continue
        if w.chart.name is None:
            w.chart.name = os.path.join(w.chart.field.upload_to, slugify(unicode(w.name)) +'.png')
            w.save()
            imagedir = os.path.dirname(w.chart.path)
            if not os.path.exists(imagedir):
                os.makedirs(imagedir)
        with open(w.chart.path,'wb') as f:
            f.write(chart_for_well(w))
        
make_thumbnails.short_description = "Grafieken vernieuwen van geseleceerde putten"
    