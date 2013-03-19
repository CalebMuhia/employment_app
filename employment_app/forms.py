# -*- coding: utf-8 -*-
""" employment_app's forms """

from django import forms
from django.conf import settings
from django.forms.widgets import RadioSelect
from common.utils import send_html_mail
from employment_app.models import Project
from tinymce.widgets import TinyMCE


class ProjectForm(forms.ModelForm):
    """ Project model form """
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
            attrs={'cols': 800, 'rows': 20})
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


class ContactForm(forms.Form):
    """ contact form """
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'span4'}), label="Your name")
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'span4'}), label="Your email")
    message = forms.CharField(
        max_length=500, widget=forms.Textarea(
            attrs={'class': 'span4', 'rows': 7}),
        label="Your message")

    def save(self):
        """ sends the email """
        c_d = self.cleaned_data
        text_email = "from {0} ({1}): {2}".format(
            c_d['name'], c_d['email'], c_d['message'])
        send_html_mail(
            settings.DEFAULT_FROM_EMAIL, 'New message from contact form!',
            'contact_form_email.html', c_d, settings.CONTACT_FORM_RECIPIENT,
            text_email
        )
