'''
Created on Jun 1, 2014

@author: theo
'''
from berging.models import Scenario, Matrix, Gift, Scenario2

from django.contrib import admin

class MatrixAdmin(admin.ModelAdmin):
    list_display = ('code','factor', 'maxopbrengst', 'rijmin','rijmax','kolmin','kolmax')
    
    def save_model(self, request, obj, form, change):
        try:
            f = request.FILES['file']
            obj.get_dimensions(f)
        except:
            pass
        obj.save()

class GiftAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'gewas', 'grondsoort', 'gift')
            
admin.site.register(Scenario)
admin.site.register(Scenario2)
admin.site.register(Gift, GiftAdmin)
admin.site.register(Matrix,MatrixAdmin)
