# -*- coding: utf-8 -*-
""" employment_app's urls """

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'employment_app.views',
    url(r'^$', 'home', name='employment_app_home'),
    # url(r'^project/(?P<slug>[-\w]+)/$', 'project_profile',
    #     name='employment_app_project_profile'),
)
