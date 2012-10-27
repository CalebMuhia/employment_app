# -*- coding: utf-8 -*-
""" employment_app's forms """

from django import forms
from django.forms.widgets import RadioSelect
from employment_app.models import Project
from tinymce.widgets import TinyMCE


class ProjectForm(forms.ModelForm):
    """ form's Project model """
    class Meta:
        """ Form's meta class """
        model = Project
        exclude = ('title_slug', 'person')

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
        """ customize some field's widgets """
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['long_description'].widget = TinyMCE(
            attrs={'cols': 80, 'rows': 20})
        self.fields['dissolution_strategy'].widget = TinyMCE(
            attrs={'cols': 80, 'rows': 20})
        self.fields['developer_description'].widget = TinyMCE(
            attrs={'cols': 80, 'rows': 20})
        self.fields['non_disclosure_agreement'].widget = TinyMCE(
            attrs={'cols': 80, 'rows': 20})
        self.fields['comment'].widget = TinyMCE(
            attrs={'cols': 80, 'rows': 20})
        self.fields['lessons_learned'].widget = TinyMCE(
            attrs={'cols': 80, 'rows': 20})
        # to use these fields as radio select, it's necessary create some
        # style to print them good
        # self.fields['open_or_closed'].widget = RadioSelect(
        #     choices=Project.OPENCLOSED)
        # self.fields['looking_for_developers'].widget = RadioSelect(
        #     choices=Project.YESNO)
