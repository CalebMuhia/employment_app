from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from employment_program.settings import STATIC_ROOT

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('employment_app.urls')),
    # url(r'^/', include('registration.backends.default.urls')),
    url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^faq/', include('faq.urls')),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^jobsboard/', include('jobsboard.urls')),
    # django-tinymce
    url(r'^tinymce/', include('tinymce.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #the registration app
    (r'^accounts/', include('registration.backends.default.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': STATIC_ROOT}),
)
