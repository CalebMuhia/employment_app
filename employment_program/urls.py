from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from employment_program.settings import STATIC_ROOT

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'employment_app.views.home', name='home'),
    url(r'^/', include('registration.backends.default.urls')),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url('^faq/', include('faq.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #the registration app
    (r'^accounts/', include('registration.backends.default.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':STATIC_ROOT}),

)
