'''
Created on Feb 21, 2015

@author: theo
'''
# from acacia.data.models import Series, MeetLocatie
# from django.db import models
# 
# # Series that can be edited manually
# class ManualSeries(Series):
#     locatie = models.ForeignKey(MeetLocatie)
#      
#     def meetlocatie(self):
#         return self.locatie
#          
#     def __unicode__(self):
#         return self.name
#  
#     def get_series_data(self,data,start=None):
#         return self.to_pandas(start=start)
#      
#     class Meta:
#         verbose_name = 'Handmatige reeks'
#         verbose_name_plural = 'Handmatige reeksen'
#          
