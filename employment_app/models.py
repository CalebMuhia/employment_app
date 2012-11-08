# -*- coding: utf-8 -*-
""" employemnt_app models """

from django.db import models
from pybb.models import PybbProfile
from common.models import Person

#An app to manage User Profiles
#django-profiles should do all the heavy lifting
# from common.models import TimeStampedModel
# from django.contrib.auth.models import User

# class UserProfile(TimeStampedModel, PybbProfile):
#     user = models.OneToOneField(User)
#     bio = models.TextField()

#     @model.permalink
#     def get_absolute_url(self):
#         return ('profiles_profile_detail', (), { 'username': self.user.username })
#     get_absolute_url = models.permalink(get_absolute_url)


# class Skill(TimeStampedModel):
#     """ stores user's skills """
#     LEVELS = (
#         ('A', 'A'),
#         ('B', 'B'),
#         ('C', 'C'),
#         ('D', 'D'),
#         ('F', 'F'),
#     )
#     user = models.ForeignKey(User)
#     skill = models.CharField(max_length=60)
#     experience_years = models.DecimalField(max_digits=3, decimal_places=1)
#     level = models.CharField(max_length=1, choices=LEVELS)

# class Location(TimeStampedModel):
#     """ stores locations """
#     user = models.ForeignKey(User)
#     address_line_1 = models.CharField(max_length=255)
#     address_line_2 = models.CharField(max_length=255, blank=True)
#     address_line_3 = models.CharField(max_length=255, blank=True)
#     zip = models.CharField(max_length=5)


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

    # def __eq__(self, y):
    # I'm not overloading the == operator because when doing it an error in
    # form.is_valid() method is raised.
    def compare(self, y):
        """
        It compares all the attributes except the unique attributes.
        """
        if (self.title == y.title
            and self.short_description == y.short_description
            and self.public_description == y.public_description
            and self.long_description == y.long_description
            and self.payment_description == y.payment_description
            and self.dissolution_strategy == y.dissolution_strategy
            and self.estimated_total_project_cost == y.
            estimated_total_project_cost
            and self.complexity_rating == y.complexity_rating and
            self.url == y.url
            and self.percent_prototype_completed == y.
            percent_prototype_completed
            and self.datetime_prototype_completion_anticipated == y.
            datetime_prototype_completion_anticipated
            and self.datetime_prototype_actually_completed == y.
            datetime_prototype_actually_completed
            and self.project_status_history == y.project_status_history
            and self.looking_for_developers == y.looking_for_developers
            and self.developer_description == y.developer_description
            and self.non_disclosure_agreement == y.non_disclosure_agreement
            and self.open_or_closed == y.open_or_closed
            and self.comment == y.comment
            and self.lessons_learned == y.lessons_learned
            and self.registration == y.registration
            and self.last_edited == y.last_edited
            and self.person == y.person
            and self.title_slug == y.title_slug):
            return True
        return False


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
