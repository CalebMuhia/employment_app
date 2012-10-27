#!/usr/bin/env python
""" jobsboard's forms """

from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
from django import forms
from datetime import datetime
from jobsboard.models import *
from jobsboard.forms import *
from tinymce.widgets import TinyMCE


class JobForm(forms.ModelForm):
    """ Job Model's Form """
    class Meta:
        """ Form's meta class """
        model = Job
        exclude = ('posted_by', 'date_added', 'tags', 'title_slug',)

    class Media:
        """ Form's media files """
        css = {
            'all': ('common/css/ui-lightness/jquery-ui-timepicker-addon.css',
                    'common/css/ui-lightness/jquery-ui-1.9.0.custom.min.css'),
        }
        js = ('common/js/jquery-ui-1.9.0.custom.min.js',
              'common/js/jquery-ui-timepicker-addon.js',
              )

    def __init__(self, *args, **kwargs):
        """ customizes some field's widgets """
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = TinyMCE(
            attrs={'cols': 80, 'rows': 20})


# class CompanyForm(forms.ModelForm):

#     class Meta:
#         model = Company
#         exclude = ('added_by', 'name_slug',)


class ApplicantForm(forms.ModelForm):

    class Meta:
        model = Applicant
        exclude = ('user', 'job', 'status', 'date_applied')
