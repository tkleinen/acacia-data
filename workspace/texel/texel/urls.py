from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from views import HomeView
admin.autodiscover()

urlpatterns = patterns('texel.views',
    url(r'^$',HomeView.as_view(),name='home'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', include('acacia.data.urls',namespace='acacia')), 
    #url(r'^$', ProjectDetailView.as_view(), {'pk':1}),
    #url(r'^(?P<name>\w+)$', DashGroupView.as_view(), name='texel-dashboard'),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.IMG_URL, document_root=settings.IMG_ROOT)
