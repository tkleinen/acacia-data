from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'acacia.views.home', name='home'),
    url(r'^cam/(?P<how>\w+)?$', 'acacia.views.cam', name='cam'),
    url(r'^mail$', 'acacia.views.mail'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^knmi/', include('acacia.data.knmi.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', include('acacia.data.urls',namespace='acacia')),
    #url(r'^spaarwater/', include('spaarwater.urls')),
    url(r'^spaarwater/', 'acacia.views.spaarwater'),
)

from django.contrib.auth import views as auth_views
urlpatterns += patterns('',
    url(r'^password/change/$',
                    auth_views.password_change,
                    name='password_change'),
    url(r'^password/change/done/$',
                    auth_views.password_change_done,
                    name='password_change_done'),
    url(r'^password/reset/$',
                    auth_views.password_reset,
                    name='password_reset'),
    url(r'^accounts/password/reset/done/$',
                    auth_views.password_reset_done,
                    name='password_reset_done'),
    url(r'^password/reset/complete/$',
                    auth_views.password_reset_complete,
                    name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                    auth_views.password_reset_confirm,
                    name='password_reset_confirm'),
    url(r'^accounts/', include('registration.backends.default.urls'))    
)
 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
