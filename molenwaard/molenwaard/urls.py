from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from .views import HomeView, UploadWizardView

admin.autodiscover()

urlpatterns = patterns('molenwaard.views',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^data/', include('acacia.data.urls',namespace='acacia')),
    url(r'^net/', include('acacia.meetnet.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload/$', UploadWizardView.as_view(), name='upload_files'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
