from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
import os
urlpatterns = patterns('',
 
    url(r'^$', 'application.views.app', name='app'),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT})
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

STATICFILES_DIRS = [
    os.path.join(settings.BASE_DIR, "static"),
    '/var/www/static/',
]