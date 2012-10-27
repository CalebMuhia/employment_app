# -*- coding: utf-8 -*-
""" employemnt_app models """

from django.db import models
from django.core.urlresolvers import reverse
from common.models import Person


class Client(Person):
    """
    uses multitable inheritance
    Stores client's data.
    """
    info = models.TextField()


class Developer(Person):
    """
    uses multitable inheritance
    Stores developer's data.
    """
    bio = models.TextField()


class Project(models.Model):
    """ stores project's data """
    COMPLEXITY = (
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low')
    )
    YESNO = (
        ('Y', 'Yes'),
        ('N', 'No')
    )
    OPENCLOSED = (
        ('O', 'Open'),
        ('C', 'Closed')
    )
    project_id = models.CharField(max_length=15, unique=True, editable=False)
    title = models.CharField(max_length=120)
    short_description = models.CharField(max_length=255)
    public_description = models.CharField(max_length=255)
    long_description = models.TextField()
    payment_description = models.CharField(max_length=255)
    dissolution_strategy = models.TextField()
    estimated_total_project_cost = models.FloatField()
    complexity_rating = models.CharField(max_length=1, choices=COMPLEXITY,
                                         default='M')
    url = models.URLField(blank=True)
    percent_prototype_completed = models.IntegerField(default=0)
    datetime_prototype_completion_anticipated = models.DateTimeField()
    datetime_prototype_actually_completed = models.DateTimeField()
    project_status_history = models.CharField(max_length=255)
    looking_for_developers = models.CharField(max_length=1, choices=YESNO,
                                              default='Y')
    developer_description = models.TextField(blank=True)
    non_disclosure_agreement = models.TextField(blank=True)
    open_or_closed = models.CharField(max_length=1, choices=OPENCLOSED,
                                      default='O')
    comment = models.TextField(blank=True)
    lessons_learned = models.TextField(blank=True)
    registration = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    person = models.ForeignKey('common.Person')
    ###
    title_slug = models.SlugField('slug', unique=True)

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ("company_detail", [str(self.title_slug)])


class Project_Comment(models.Model):
    """ stores the person's comments from a project """
    person = models.ForeignKey('common.Person')
    project = models.ForeignKey('Project')
    comment = models.CharField(max_length=255)
    datetime_comment_submitted = models.DateTimeField(auto_now_add=True)


class Person_Project(models.Model):
    """ relates a project with other persons """
    TYPE_PERSON = (
        ('D', 'Developer'),
        ('S', 'Startup Partner')
    )
    person = models.ForeignKey('common.Person')
    project = models.ForeignKey('Project')
    type_person = models.CharField(max_length=1, choices=TYPE_PERSON)
    comment_by_client = models.CharField(max_length=255, blank=True)
    comment_by_cfgio = models.CharField(max_length=255, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


from employment_app import signals
signals.setup_signals()
