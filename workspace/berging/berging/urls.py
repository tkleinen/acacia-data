from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('berging.views',
    url(r'^$', 'home', name='home'),
    url(r'^select', 'select', name='select'),
    url(r'^query', 'query', name='query'),
    url(r'^scenario2', 'scenario2', name='scenario2'),
    url(r'^scenario', 'scenario_highchart', name='scenario'),
    url(r'^grondsoort', 'grondsoort', name='grondsoort'),
#    url(r'admin/berging/matrix/add/', 'addmatrix'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
