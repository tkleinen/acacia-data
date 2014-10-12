'''
Created on Oct 4, 2014

@author: theo
'''
from django.shortcuts import render_to_response, get_object_or_404
from acacia.data.models import Project
from acacia.data.views import ProjectDetailView

class HomeView(ProjectDetailView):
    def get_object(self):
        return get_object_or_404(Project,name='Texel')
    
def home(request):
    return render_to_response('home.html')