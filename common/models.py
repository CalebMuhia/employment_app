#-*- coding: utf-8  -*-
""" common models """

from django.db import models
from django.contrib.auth.models import User
from pybb.models import PybbProfile

# THERE IS NO NEED TO USE THIS BECAUSE WE CAN REPLATE ALL THIS CODE JUST USING
# THE DATETIMEFIELD OPTIONS auto_now and auto_now_add
#TimeStampedModel plundered from django-extensions. Aargh Jim Lad.
#See here: https://github.com/django-extensions/
# from fields import CreationDateTimeField, ModificationDateTimeField
# from django.utils.translation import ugettext_lazy as _

# class TimeStampedModel(models.Model):
#     """
#     TimeStampedModel
#     An abstract base class model that provides self-managed "created" and
#     "modified" fields.
#     """
#     created = CreationDateTimeField(_('created'))
#     modified = ModificationDateTimeField(_('modified'))

#     class Meta:
#         get_latest_by = 'modified'
#         ordering = ('-modified', '-created',)
#         abstract = True


class Person(PybbProfile):
    """
    For the Person class I am using the built-in User object
    provided by Django's contrib.auth module. From there
    we can extend it out to create a fairly robust Person
    object/user profile type of object.
    """
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    person_id = models.CharField(max_length=16, unique=True, editable=False)
    user = models.ForeignKey(User, unique=True)
    middle_name = models.CharField(max_length=25, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    # time_zone = models.CharField(max_length=25, blank=True)
    comment = models.TextField(blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    skills = models.ManyToManyField('Skill', through='Person_Skill')

    def __unicode__(self):
        return u'%s %s %s' % (
            self.user.first_name, self.middle_name or '', self.user.last_name)

    @models.permalink
    def get_absolute_url(self):
        return (
            'profiles_profile_detail', (), {'username': self.user.username})


class FeedBack(models.Model):
    """ stores the users's feedback """
    comment = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey('Person')


class Challenge_Question(models.Model):
    """ stores the questions to recover user accounts """
    question = models.CharField(max_length=120)
    answer = models.CharField(max_length=120)
    datetime = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey('Person')


class Phone_Number(models.Model):
    """ stores users' phone numbers """
    PURPOSES = (
        ('H', 'Home'),
        ('W', 'Work'),
        ('V', 'Vacation'),
    )
    """ stores the users's phone numbers """
    phone_number = models.CharField(max_length=20)
    purpose = models.CharField(max_length=1, choices=PURPOSES)
    comment = models.CharField(max_length=120, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey('Person')


class Skill(models.Model):
    """ stores person's skills """
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return u'%s' % self.name


class Person_Skill(models.Model):
    """ intermediate table that stores extra data from person's skills """
    LEVELS = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    )
    person = models.ForeignKey('Person')
    skill = models.ForeignKey('Skill')
    experience_years = models.DecimalField(max_digits=3, decimal_places=1)
    level = models.CharField(max_length=1, choices=LEVELS)
    datetime = models.DateTimeField(auto_now_add=True)


class Location(models.Model):
    """ stores locations """
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    address_line_3 = models.CharField(max_length=255, blank=True)
    city = models.ForeignKey('cities_light.City')
    country = models.ForeignKey('cities_light.Country')
    state = models.ForeignKey('cities_light.Region')
    zip = models.CharField(max_length=5)
    purpose = models.CharField(max_length=100)
    touch_date = models.DateTimeField(auto_now_add=True)
    user_comment = models.TextField()
    person = models.ForeignKey('Person')


from common import signals
signals.setup_signals()
