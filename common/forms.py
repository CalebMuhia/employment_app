# -*- coding: utf-8 -*-
""" common's forms """

from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from django.forms.models import inlineformset_factory
from common.models import Person, Person_Skill
from common.fields import UsernameField


SkillsFormSet = inlineformset_factory(Person, Person_Skill, extra=2)


class Person0Form(forms.ModelForm):
    class Meta:
        model = Person


class PersonForm(forms.ModelForm):
    """
    Person model's form.
    This forms has been modified to include the data of the User model
    and to manage the m2m relations using its intermediary model.
    """
    id = forms.IntegerField(widget=forms.HiddenInput)
    username = UsernameField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    new_password = forms.CharField(
        required=False, widget=forms.PasswordInput(render_value=True))
    confirm_new_password = forms.CharField(
        required=False, widget=forms.PasswordInput(render_value=True))
    email_address = forms.EmailField()

    class Meta:
        """ Form's meta class """
        model = Person
        exclude = ('skills', 'user', 'post_count')

    def __init__(self, *args, **kwargs):
        """ initializes the fields added to the form """
        user = None
        if 'user' in kwargs:
            user = kwargs.pop('user')
        super(PersonForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email_address'].initial = user.email
        self.fields.keyOrder = [
            'id', 'username', 'first_name', 'middle_name', 'last_name',
            'email_address', 'gender',
            'new_password', 'confirm_new_password', 'signature',
            'signature_html', 'time_zone', 'language', 'show_signatures',
            'avatar', 'autosubscribe', 'comment'
        ]

    def clean_username(self):
        """ Verifies that the username is unique """
        c_d = self.cleaned_data
        if User.objects.exclude(id=c_d['id']).filter(
                username=c_d['username']):
            raise forms.ValidationError(u'The Username is already registered.')
        return c_d['username']

    def clean_email_address(self):
        """ Verifies that the email is unique """
        c_d = self.cleaned_data
        if User.objects.exclude(id=c_d['id']).filter(
                email=c_d['email_address']):
            raise forms.ValidationError(u'The email is already registered.')
        return c_d['email_address']

    def clean(self):
        """ Verifies that if the passwords are provided, they must be equal """
        c_d = super(PersonForm, self).clean()
        pass1 = c_d.get('new_password')
        pass2 = c_d.get('confirm_new_password')
        if pass1 and pass2 and (pass1 == pass2):
            return c_d
        if pass1:
            if not pass2:
                self._errors['confirm_new_password'] = self.error_class([
                    'Confirm your new password.'])
                # del c_d['new_password']
            elif pass1 != pass2:
                del c_d['new_password']
                del c_d['confirm_new_password']
                raise forms.ValidationError(
                    'The passwords typed are not equal.')
        elif pass2:
            if not pass1:
                self._errors['new_password'] = self.error_class([
                    'Type your new password.'])
                # del c_d['confirm_new_password']
        return c_d

    @transaction.commit_on_success
    def save(self, *args, **kwargs):
        """ saves the data to the corresponding Person and User objects """
        person = super(PersonForm, self).save(*args, **kwargs)
        user = person.user
        c_d = self.cleaned_data
        user.username = c_d['username']
        user.first_name = c_d['first_name']
        user.last_name = c_d['last_name']
        user.email = c_d['email_address']
        pass1 = c_d.get('new_password')
        if pass1:
            user.set_password(pass1)
        user.save()
        return person
