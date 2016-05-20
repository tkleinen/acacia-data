'''
Created on Oct 4, 2014

@author: theo
'''
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from acacia.data.models import Project, MeetLocatie, TabGroup, KeyFigure
from acacia.data.views import ProjectDetailView

class HomeView(ProjectDetailView):
    template_name = 'spaarwater_detail.html'

    def get_object(self):
        return get_object_or_404(Project,pk=1)
    
class DashGroupView(TemplateView):
    template_name = 'dashgroup.html'
    
    def get_context_data(self, **kwargs):
        context = super(DashGroupView,self).get_context_data(**kwargs)
        name = context.get('name')
        page = int(self.request.GET.get('page', 1))
        group = get_object_or_404(TabGroup, name__iexact=name)
        dashboards =[p.dashboard for p in group.tabpage_set.order_by('order')]
        context['group'] = group
        page = min(page, len(dashboards))
        if page > 0:
            pages = list(group.pages())
            context['title'] = 'Dashboard %s - %s' % (group.name, pages[page-1].name)
            context['page'] = int(page)
            context['dashboard'] = dashboards[page-1]
        return context    

class OverviewView(TemplateView):
    template_name = 'overview.html'
    
    def get_context_data(self, **kwargs):
        context = super(OverviewView,self).get_context_data(**kwargs)
        pk = context.get('pk',1)
        locatie = get_object_or_404(MeetLocatie,pk=pk)
        context['locatie'] = locatie
        keys = KeyFigure.objects.filter(locatie=locatie)
        for key in keys:
            context[key.name] = key.value
        return context    
    
    