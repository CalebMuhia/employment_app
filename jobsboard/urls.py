#!/usr/bin/env python
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'jobsboard.views.job_list', name='jobs_list'),
    url(r'^create/$', 'jobsboard.views.job_create', name='job_create'),
    url(r'^createproject/$', 'jobsboard.views.company_create', name='company_create'),
    url(r'^edit/(?P<jobid>\d+)/$', 'jobsboard.views.job_edit', name='job_edit'),
    url(r'^detail/(?P<jobid>\d+)/$', 'jobsboard.views.job_detail', name='job_details'),
    url(r'^projects/$', 'jobsboard.views.company_list', name='company_list'),
    url(r'^project/edit/(?P<comid>\d+)/$', 'jobsboard.views.company_edit', name='company_edit'),
    url(r'^project/detail/(?P<slug>[-\w]+)/$', 'jobsboard.views.company_detail', name='company_detail'),
    url(r'^detail/applicant/remove/(?P<id>\d+)/$', 'jobsboard.views.apply_remove', name='apply_remove'),
    url(r'^applied/$', 'jobsboard.views.apply_list', name='apply_list'),
    url(r'^applied/remove/(?P<id>\d+)/$', 'jobsboard.views.apply_remove_from_list', name='apply_remove_from_list'),
    url(r'^detail/(?P<id>\d+)/appremove/(?P<jobid>\d+)$', 'jobsboard.views.job_apply_remove', name='job_apply_remove'),
    url(r'^detail/(?P<id>\d+)/remove/$', 'jobsboard.views.job_remove', name='job_remove'),
    url(r'^project/(?P<id>\d+)/remove/$', 'jobsboard.views.company_remove', name='com_remove'),
    # url(r'^detail/(?P<id>\d+)/remove/$', 'jobsboard.views.job_remove', name='job_remove'),
    url(r'^detail/applicant/(?P<id>\d+)/status/(?P<status>\d+)/$', 'jobsboard.views.applicant_status', name='applicant_status'),
    url(r'^detail/(?P<id>\d+)/status/(?P<status>\d+)/$', 'jobsboard.views.job_status', name='job_status'),
    url(r'^yourjobpost/$', 'jobsboard.views.your_job_post', name='your_job_post'),
    url(r'^yourprojects/$', 'jobsboard.views.your_company', name='your_company'),
)
