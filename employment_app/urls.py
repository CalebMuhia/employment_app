# -*- coding: utf-8 -*-
""" employment_app's urls """

from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView
from employment_app.views import ContactView, ContactSuccessView


urlpatterns = patterns(
    'employment_app.views',
    url(r'^$', 'home', name='employment_app_home'),
    # url(r'^project/(?P<slug>[-\w]+)/$', 'project_profile',
    #     name='employment_app_project_profile'),
    url(r'^about_us$', TemplateView.as_view(template_name="about_us.html"), name='about_us'),
    url(r'^contact_us$', ContactView.as_view(), name='contact_us'),
    url(r'^contact_us/message_sent$', ContactSuccessView.as_view(),
        name='contact_success')

)
