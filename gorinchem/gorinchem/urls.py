from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from gorinchem.views import NetworkView, WellView, ScreenView, ScreenChartView, WellChartView

admin.autodiscover()

urlpatterns = patterns('gorinchem.views',
#    url(r'^$', 'home', name='home'),
    url(r'^$', NetworkView.as_view(), name='home'),
    url(r'^network/(?P<pk>\d+)$', NetworkView.as_view(), name='network-detail'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^data/', include('acacia.data.urls',namespace='acacia')),
    url(r'^well/(?P<pk>\d+)$', WellView.as_view(), name='well-detail'),
    url(r'^screen/(?P<pk>\d+)$', ScreenView.as_view(), name='screen-detail'),
    url(r'^chart/(?P<pk>\d+)/$', WellChartView.as_view(), name='chart-detail'),
    url(r'^upload/$', 'upload_file', name='upload_file'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
