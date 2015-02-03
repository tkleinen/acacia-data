'''
Created on Jun 1, 2014

@author: theo
'''
from berging.models import Scenario, Matrix

from django.contrib import admin

class MatrixAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            f = request.FILES['file']
            obj.get_dimensions(f)
        except:
            pass
        obj.save()
        
admin.site.register(Scenario)
admin.site.register(Matrix,MatrixAdmin)
