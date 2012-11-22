# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('employment_app.urls')),
    # url(r'^/', include('registration.backends.default.urls')),
    # django-profiles
    url(r'^profiles/', include('profiles.urls')),
    url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^faq/', include('faq.urls')),
    url(r'^jobsboard/', include('jobsboard.urls')),
    # django-tinymce
    url(r'^tinymce/', include('tinymce.urls')),
    #the registration app
    (r'^accounts/', include('registration.backends.default.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
     
)
