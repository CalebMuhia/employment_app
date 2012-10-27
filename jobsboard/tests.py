# -*- coding: utf-8 -*-
""" jobsboard's tests """

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from jobsboard.models import Job, Applicant
from employment_app.models import Project
from common.utils import random_string_with_length
import random
import datetime


class BaseOperations(TestCase):
    """ holds the basic operations of this application """

    @staticmethod
    def _create_user(active=False, superuser=False):
        """
        Creates a user (the signal creates its profile).
        Returns the user.
        """
        u = User.objects.create(
            username=random_string_with_length(5),
            is_active=active, is_staff=True, is_superuser=superuser)
        u.set_password('1')
        u.save()
        return u

    @staticmethod
    def _create_project(person):
        """ creates and returns a new project """
        return Project.objects.create(
            title=random_string_with_length(),
            short_description=random_string_with_length(),
            public_description=random_string_with_length(),
            long_description=random_string_with_length(),
            payment_description=random_string_with_length(),
            dissolution_strategy=random_string_with_length(),
            estimated_total_project_cost=random.randint(10000, 500000),
            complexity_rating='M',
            percent_prototype_completed=0,
            datetime_prototype_completion_anticipated=datetime.datetime.now(),
            datetime_prototype_actually_completed=datetime.datetime.now(),
            looking_for_developers='Y',
            open_or_closed='O',
            person=person
        )

    @staticmethod
    def _create_job(user, project):
        """ creates and returns a new job """
        return Job.objects.create(
            posted_by=user,
            project=project,
            title=random_string_with_length(),
            description=random_string_with_length(),
            status=1,
            date_due=datetime.date.today(),
            tags=random_string_with_length(5)
        )

    def _apply(self, user=None, job=None):
        """
        creates an application of the user to the job
        if any of the arguments is not provided, creates new one(s)
        returns the application
        """
        user = user or self._create_user(True, True)
        job = job or self._create_job(
            user, self._create_project(user.get_profile()))
        return Applicant.objects.create(user=user, job=job, status=0)


class JobsTests(BaseOperations):
    """ jobs's model tests """

    def test_all_views(self):
        """ Verifies that all views work good """
        user = self._create_user(True, True)
        result = self.client.login(username=user.username, password='1')
        self.assertEqual(result, True, 'Login process Failed')

        views_to_test = (
            (reverse('jobs_list'), 'jobs_list'),
            (reverse('job_create'), 'job_create'),
            (reverse('company_create'), 'company_create'),
            (reverse('company_list'), 'company_list'),
            (reverse('apply_list'), 'apply_list'),
            (reverse('your_job_post'), 'your_job_post'),
            (reverse('your_company'), 'your_company'),
        )

        for view in views_to_test:
            response = self.client.get(view[0])
            self.assertEqual(response.status_code, 200, str(
                response.status_code) + ' ' + view[1])

        project = self._create_project(user.get_profile())
        job = self._create_job(user, project)
        application = self._apply(user, job)

        views_to_test = (
            (reverse('your_company'), 'your_company', 200),
            (reverse('your_job_post'), 'your_job_post', 200),
            (reverse('jobs_list'), 'jobs_list', 200),
            (reverse('job_edit', args=(job.id, )), 'job_edit', 200),
            (reverse('job_details', args=(job.id, )), 'jobd)etails', 200),
            (reverse('company_list'), 'company_list', 200),
            (reverse('company_edit', args=(project.id, )), 'company_edit',
             200),
            (reverse('company_detail', args=(project.title_slug, )),
             'company_detail', 200),
            (reverse('applicant_status', args=(application.id, 0)),
             'applicant_status', 302),
            (reverse('apply_list'), 'apply_list', 200),
            (reverse('apply_remove', args=(application.id, )), 'apply_remove',
             302),
            (reverse('apply_list'), 'apply_list', 200),
            (reverse('job_status', args=(job.id, 0)), 'job_status', 302),
        )

        for view in views_to_test:
            response = self.client.get(view[0])
            self.assertEqual(response.status_code, view[2], str(
                response.status_code) + ' ' + view[1])

        application = self._apply(user, job)

        views_to_test = (
            (reverse('apply_remove_from_list', args=(application.id, )),
             'apply_remove_from_list', 302),
        )

        for view in views_to_test:
            response = self.client.get(view[0])
            self.assertEqual(response.status_code, view[2], str(
                response.status_code) + ' ' + view[1])

        application = self._apply(user, job)

        views_to_test = (
            (reverse('job_apply_remove', args=(application.id, job.id, )),
             'job_apply_remove', 302),
        )

        for view in views_to_test:
            response = self.client.get(view[0])
            self.assertEqual(response.status_code, view[2], str(
                response.status_code) + ' ' + view[1])

        views_to_test = (
            (reverse('job_remove', args=(job.id, )), 'job_remove', 302),
        )

        for view in views_to_test:
            response = self.client.get(view[0])
            self.assertEqual(response.status_code, view[2], str(
                response.status_code) + ' ' + view[1])

        views_to_test = (
            (reverse('com_remove', args=(project.id, )), 'com_remove', 302),
        )

        for view in views_to_test:
            response = self.client.get(view[0])
            self.assertEqual(response.status_code, view[2], str(
                response.status_code) + ' ' + view[1])
