from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from gorinchem.views import NetworkView, WellView, ScreenView, ScreenChartView, WellChartView, UploadFileView, UploadDoneView
from django.contrib.auth.decorators import login_required

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
    url(r'^upload/(?P<id>\d+)/$', login_required(UploadFileView.as_view()), name='upload_file'),
    url(r'^done/(?P<id>\d+)/$', UploadDoneView.as_view(), name='upload_done'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

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
