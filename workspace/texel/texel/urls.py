from django.conf.urls import patterns, include, url

from django.contrib import admin
from views import HomeView
admin.autodiscover()

urlpatterns = patterns('texel.views',
    url(r'^$',HomeView.as_view(),name='home'),
    #url(r'^home$','home',name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', include('acacia.data.urls',namespace='acacia')), 
    #url(r'^$', ProjectDetailView.as_view(), {'pk':1}),
    #url(r'^(?P<name>\w+)$', DashGroupView.as_view(), name='texel-dashboard'),
)
