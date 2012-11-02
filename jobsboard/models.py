# -*- coding: utf-8 -*-
""" jobsboard's models """

from datetime import datetime
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from jobsboard.signals import *
from django.db.models.signals import *
from tagging.fields import TagField


# class Company(models.Model):
#     """
#     A company with its details.
#     """
#     name = models.CharField(_('name'), max_length=200)
#     name_slug = models.SlugField(_('slug'))
#     telephone = models.CharField(
#         _('telephone'), max_length=30, blank=True, null=True)
#     fax = models.CharField(_('fax'), max_length=30, blank=True, null=True)
#     address = models.TextField(_('address'))
#     description = models.TextField(_('description'))
#     date_added = models.DateTimeField(
#         _('date added'), default=datetime.now, editable=False)
#     added_by = models.ForeignKey(
#         User, related_name="companies_added", blank=False, null=False)
#     tags = TagField(help_text='separate your tags with a comma and use dash \
#     (-) instead of space between words ( example: music, top, top-artists )')

#     class Meta:
#         ordering = ['name']
#         verbose_name = _('company')
#         verbose_name_plural = _('companies')

#     def __unicode__(self):
#         return self.name

#     def get_absolute_url(self):
#         return ("company_detail", [self.pk])
#     get_absolute_url = models.permalink(get_absolute_url)

#     def save(self):
#         self.name_slug = slugify(self.name)
#         super(Company, self).save()


class Job(models.Model):
    """
    A job with its details.
    """
    STATUS_CHOICES = (
        (1, _('Open')),
        (2, _('Filled')),
        (3, _('Cancelled')),
        (4, _('Stale')),
    )

    posted_by = models.ForeignKey(
        User, related_name="jobs_posted", blank=False, null=False)
    # company = models.ForeignKey(
    #     Company, related_name="company_jobs", blank=False, null=False)
    project = models.ForeignKey('employment_app.Project',
                                related_name="project_jobs",
                                blank=False, null=False)
    title = models.CharField(_('title'), max_length=200)
    title_slug = models.SlugField(_('slug'))
    description = models.TextField(_('description'))
    status = models.IntegerField(
        _('status'), choices=STATUS_CHOICES, default=1)
    date_added = models.DateTimeField(
        _('date added'), auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(
        _('date updated'), auto_now=True, editable=False)
    date_due = models.DateField(_('date due'), blank=False, null=False)
    tags = TagField(help_text='separate your tags with a comma and use dash\
    (-) instead of space between words ( example: music, top, top-artists )')

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ("job_details", [self.pk])
    get_absolute_url = models.permalink(get_absolute_url)

    def get_status(self, set_status):
        return self.set_status

    def save(self, *args, **kwargs):
        job = None
        if self.id:
            job = Job.objects.get(id=self.id)
            if job.status == int(self.status):
                pass
            else:
                job_pre_status_changed.send(
                    sender=self, old_job=job, new_job=self)
                if settings.DEBUG and not settings.PRODUCTION:
                    print '-------------------------------->'
                    print 'old job: %s ======= new job: %s' % (job.status,
                                                               self.status)
                    print '-------------------------------->'
        self.title_slug = slugify(self.title)
        super(Job, self).save(*args, **kwargs)
        if job:
            if job.status == int(self.status):
                pass
            else:
                job_post_status_changed.send(
                    sender=self, old_job=job, new_job=self)
                if settings.DEBUG and not settings.PRODUCTION:
                    print '-------------------------------->'
                    print 'old job: %s ======= new job: %s' % (job.status,
                                                               self.status)
                    print '-------------------------------->'

    # def __eq__(self, y):
    # I'm not overloading the == operator because when doing it an error in
    # form.is_valid() method is raised.
    def compare(self, y):
        """
        It compares all the attributes except the unique attributes.
        """
        if (self.posted_by == y.posted_by
            and self.project == y.project
            and self.title == y.title
            and self.title_slug == y.title_slug
            and self.description == y.description
            and self.status == y.status
            and self.date_added == y.date_added
            and self.date_updated == y.date_updated
            and self.date_due == y.date_due
            and self.tags == y.tags):
            return True
        return False


class Applicant(models.Model):
    """
    A job applicant.
    """
    STATUS_CHOICES = (
        ((0, 'unattended')),
        ((1, 'candidate')),
        ((2, 'not qualified')),
        ((3, 'over qualified')),
        ((4, 'delisted')),
        ((5, 'winner')),
    )
    user = models.ForeignKey(User, related_name="job_applicant")
    job = models.ForeignKey(Job, related_name="job_applicant")
    status = models.IntegerField(
        _('status'), choices=STATUS_CHOICES, default=0)
    date_applied = models.DateTimeField(
        _('date applied'), auto_now_add=True, editable=False)

    class Meta:
        unique_together = (('user', 'job'),)

    def is_at(self):
        if self.status == 0:
            return self.status

    def __unicode__(self):
        return '%s applied for %s' % (self.user.username, self.job)

    def get_absolute_url(self):
        return ("job_details", [self.job.pk])
    get_absolute_url = models.permalink(get_absolute_url)

    # def __eq__(self, y):
    # I'm not overloading the == operator because when doing it an error in
    # form.is_valid() method is raised.
    def compare(self, y):
        """
        It compares all the attributes except the unique attributes.
        """
        if (self.user == y.user and self.job == y.job
            and self.status == y.status
            and self.date_appplied == y.date_applied):
            return True
        return False

    def is_candidate(self):
        if self.status == 1:
            return self.status

    def is_notqualified(self):
        if self.status == 2:
            return self.status

    def is_overqualified(self):
        if self.status == 3:
            return self.status

    def is_delisted(self):
        if self.status == 4:
            return self.status

    def is_winner(self):
        if self.status == 5:
            return self.status

    def save(self, *args, **kwargs):
        instance = None
        super(Applicant, self).save(*args, **kwargs)
