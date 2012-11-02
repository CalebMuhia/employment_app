# -*- coding: utf-8 -*-
""" jobsboard's tests """

from django.test import TestCase
from django.conf import settings
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
        """
        Verifies that there are not broken views.
        This doesn't verifies if a view works good or bad, just verifies that
        is not broken.
        """
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

    def test_job_list(self):
        """
        Tests job_list view.
        * Verifies that the view works
        * Verifies that the jobs list is delived to the template
        """
        response = self.client.get(reverse('jobs_list'))
        self.assertEqual(response.status_code, 200, str(response.status_code))
        user = self._create_user(True, True)
        for i in xrange(5):
            self._create_job(user, self._create_project(user.get_profile()))
        response = self.client.get(reverse('jobs_list'))
        self.assertEqual(response.status_code, 200, str(response.status_code))
        self.assertEqual(response.context['jobs'].count(), 5,
                         'job_list view: the jobs are not being delivered to \
                         the template.')

    def test_job_create(self):
        """
        Tests the job_create view.
        * Verifies that the view is reachable just by logged in users.
        * Verifies that after filling the form:
          - A new Job is created.
          - A redirection is made.
        """
        user = self._create_user(True, True)
        response = self.client.get(reverse('job_create'))
        self.assertEqual(response.status_code, 302, str(response.status_code))

        result = self.client.login(username=user.username, password='1')
        self.assertEqual(result, True, 'Login process Failed')

        response = self.client.get(reverse('job_create'))
        self.assertEqual(response.status_code, 200, str(response.status_code))

        response = self.client.post(
            reverse('job_create'),
            {'project': self._create_project(user.get_profile()).id,
             'title': random_string_with_length(),
             'description': random_string_with_length(),
             'status': 1,
             'date_due': datetime.date.today()
             }
        )
        self.assertEqual(response.status_code, 302, str(response.status_code))
        self.assertEqual(Job.objects.count(), 1,
                         'job_create view: The job wasn\'t created.')

    def test_company_create(self):
        """
        Tests company_create view.
        * Verifies that the view is reachable just by logged in users.
        * Verifies that after filling the form:
          - A new Project is created.
          - A redirection is made.
        """
        user = self._create_user(True, True)
        response = self.client.get(reverse('company_create'))
        self.assertEqual(response.status_code, 302, str(response.status_code))

        result = self.client.login(username=user.username, password='1')
        self.assertEqual(result, True, 'Login process Failed')

        response = self.client.get(reverse('company_create'))
        self.assertEqual(response.status_code, 200, str(response.status_code))

        response = self.client.post(
            reverse('company_create'),
            {'title': random_string_with_length(),
             'short_description': random_string_with_length(),
             'public_description': random_string_with_length(),
             'long_description': random_string_with_length(),
             'payment_description': random_string_with_length(),
             'dissolution_strategy': random_string_with_length(),
             'estimated_total_project_cost': random.randint(10000, 500000),
             'complexity_rating': 'M',
             'percent_prototype_completed': 0,
             'datetime_prototype_completion_anticipated': datetime.datetime.
             now(),
             'datetime_prototype_actually_completed': datetime.datetime.now(),
             'looking_for_developers': 'Y',
             'open_or_closed': 'O',
             'project_status_history': random_string_with_length(),
             }
        )
        self.assertEqual(response.status_code, 302, str(response.status_code))
        self.assertEqual(Project.objects.count(), 1,
                         'company_create view: The project wasn\'t created.')

    def test_job_edit(self):
        """
        Tests the job_edit view.
        * verifies that the job_edit view is reachable just for logged in users
        * verifies that the form works properly
        """
        user = self._create_user(True, True)
        project = self._create_project(user.get_profile())
        project2 = self._create_project(user.get_profile())
        job = self._create_job(user, project)
        response = self.client.get(reverse('job_edit', args=(job.id, )))
        self.assertEqual(response.status_code, 302, str(response.status_code))

        result = self.client.login(username=user.username, password='1')
        self.assertEqual(result, True, 'Login process Failed')

        response = self.client.get(reverse('job_edit', args=(job.id, )))
        self.assertEqual(response.status_code, 200, str(response.status_code))

        response = self.client.post(
            reverse('job_edit', args=(job.id, )),
            {'project': project2.id,
             'title': 'new title',
             'description': 'new description',
             'status': 2,
             'date_due': datetime.date.today()
             }
        )
        self.assertFalse(job.compare(Job.objects.get(id=1)),
                         'job_edit view: The job was no updated properly.')
        self.assertEqual(response.status_code, 302, str(response.status_code))
        self.assertEqual(Job.objects.count(), 1,
                         'job_edit view: The job was not updated, instead of \
                         that a new job was recorded.')

    def test_job_details(self):
        """
        Tests job_detail view
        * verifies that the job_detail view is reachable
        * verifies that only logged in users can apply for a job.
        """
        user = self._create_user(True, True)
        job = self._create_job(user, self._create_project(user.get_profile()))
        response = self.client.get(reverse('job_details', args=(job.id, )))
        self.assertEqual(response.status_code, 200, str(response.status_code))

        response = self.client.post(
            reverse('job_details', args=(job.id, )), {})
        self.assertEqual(response.status_code, 200, str(response.status_code))
        self.assertEqual(
            Applicant.objects.count(), 0,
            'job_detail view: The applicant object was created despite of the \
            user was not logged in.')

        result = self.client.login(username=user.username, password='1')
        self.assertEqual(result, True, 'Login process Failed')
        response = self.client.post(
            reverse('job_details', args=(job.id, )), {})
        self.assertEqual(response.status_code, 302, str(response.status_code))
        self.assertEqual(
            Applicant.objects.count(), 1,
            'job_detail view: The applicant object was not created')

    def test_company_list(self):
        """
        Tests the company_list view.
        * Verifies that the projects' list is delivered to the template
          properly.
        * Verifies that the search form works good.
        """
        user = self._create_user(True, True)
        response = self.client.get(reverse('company_list'))
        self.assertEqual(response.status_code, 200, str(response.status_code))
        self.assertEqual(
            response.context['company'].count(), 0,
            'company_list view: Phe list of projects was not empty.')
        for i in xrange(5):
            self._create_project(user.get_profile())
        response = self.client.get(reverse('company_list'))
        self.assertEqual(
            response.status_code, 200, str(response.status_code))
        self.assertEqual(
            response.context['company'].count(), 5,
            'company_list view: Not all the projects were delivered to the \
            template.')

        response = self.client.get(
            reverse('company_list'), {'q': Project.objects.get(id=1).title})
        self.assertEqual(
            response.status_code, 200, str(response.status_code))
        self.assertEqual(
            response.context['company'].count(), 1,
            'company_list view: Project not found.')

    def test_company_edit(self):
        """
        Tests company_edit view.
        * Verifies that the view is reachable and the required object by the
          templates are delivered.
        * Verifies that the form works properly
        """
        user = self._create_user(True, True)
        project = self._create_project(user.get_profile())
        result = self.client.login(username=user.username, password='1')
        self.assertEqual(result, True, 'Login process Failed')
        response = self.client.get(
            reverse('company_edit', args=(project.id, )))
        self.assertEqual(response.status_code, 200, str(response.status_code))
        self.assertTrue(
            'com_form' in response.context,
            'The com_form object was no delivered to the template.')
        self.assertTrue(
            'com_obj' in response.context,
            'The com_obj object was no delivered to the template.')

        response = self.client.post(
            reverse('company_edit', args=(project.id, )),
            {'title': 'new title',
             'short_description': 'new decription',
             'public_description': 'new public description',
             'long_description': 'new long description',
             'payment_description': 'new payment description',
             'dissolution_strategy': 'new dissolution strategy',
             'estimated_total_project_cost': 50000,
             'complexity_rating': 'L',
             'percent_prototype_completed': 50,
             'datetime_prototype_completion_anticipated': datetime.datetime.
             now() + datetime.timedelta(days=1),
             'datetime_prototype_actually_completed': datetime.datetime.
             now() + datetime.timedelta(days=1),
             'looking_for_developers': 'N',
             'open_or_closed': 'C',
             'project_status_history': 'new status history',
             }
        )
        self.assertEqual(response.status_code, 302, str(response.status_code))
        self.assertFalse(
            project.compare(Project.objects.get(id=1)),
            'company_create view: The project wasn\'t updated properly')
        self.assertEqual(
            Project.objects.count(), 1,
            'company_create view: The project wasn\'t updated properly')

    def test_company_detail(self):
        """
        Tests company_detail view.
        * Verifies the view works good and the corresponding objects are
          passed to the template.
        * Verifies that 404 is raised when the slug doesn't belong to any
          project.
        """
        user = self._create_user(True, True)
        project = self._create_project(user.get_profile())
        response = self.client.get(
            reverse('company_detail', args=(project.title_slug, )))
        self.assertEqual(response.status_code, 200, str(response.status_code))
        self.assertTrue(
            'com' in response.context,
            'company_detail view: The project wasn\'t passed to the template')
        self.assertTrue(
            'jobs' in response.context,
            'company_detail view: The jobs weren\'t delivered to the template')

        response = self.client.get(reverse('company_detail', args=('abc', )))
        self.assertEqual(
            response.status_code, 404,
            '%s : A 404 should be raised.' % str(response.status_code))

    def test_apply_remove(self):
        """
        Tests apply_remove view.
        * Verifies that if the user is not logged in, he's redirected to the
          login url
        * Verifies that an application can be removed by its owner.
        * Verifies that an application can't be removed by a user that is not
          the owner of the application.
        """
        application = self._apply()
        response = self.client.get(
            reverse('apply_remove', args=(application.job.id, )))
        self.assertRedirects(
            response,
            settings.LOGIN_URL + '?next=' + reverse(
                'apply_remove',
                args=(application.job.id, )
            )
        )

        result = self.client.login(
            username=application.user.username, password='1')
        self.assertEqual(result, True, 'Login process Failed')
        response = self.client.get(
            reverse('apply_remove', args=(application.job.id, )))
        self.assertEqual(response.status_code, 302, str(response.status_code))
        self.assertEqual(Applicant.objects.count(), 0,
                         'The application was not deleted.')

        self._apply()
        response = self.client.get(
            reverse('apply_remove', args=(application.job.id, )))
        self.assertEqual(response.status_code, 302, str(response.status_code))
        self.assertEqual(Applicant.objects.count(), 1,
                         'The application shouldn\'t be deleted.')

    def test_apply_list(self):
        """
        Tests apply_list view.
        * Verifies that only logged in user can access the view.
        * Verifies that the view is shown properly and the list of jobs is
          passed to the template.
        """
        response = self.client.get(reverse('apply_list'))
        self.assertRedirects(
            response, settings.LOGIN_URL + '?next=' + reverse('apply_list')
        )

        user = self._create_user(True, True)
        result = self.client.login(
            username=user.username, password='1')
        self.assertEqual(result, True, 'Login process Failed')
        response = self.client.get(reverse('apply_list'))
        self.assertEqual(response.status_code, 200, str(response.status_code))
        self.assertTrue('jobs' in response.context,
                        'The job\'s list was not passed to the template')

    def test_apply_remove_from_list(self):
        """
        Tests apply_remove_from_list view.
        1 Verifies that only logged in user can access the view.
        2 Verifies that a logged in user can delete his application and gets
          redirected properly.
        3 Verifies that a logged in user can't delete an application that was
          not created by him and gets redirected properly.
        """
        # 1
        application = self._apply()
        response = self.client.get(reverse('apply_remove_from_list',
                                           args=(application.id, )))
        self.assertRedirects(
            response,
            settings.LOGIN_URL + '?next=' + reverse(
                'apply_remove_from_list', args=(application.id, ))
        )
        # 2
        result = self.client.login(username=application.user.username,
                                   password='1')
        self.assertEqual(result, True, 'Login process Failed')
        response = self.client.get(reverse('apply_remove_from_list',
                                           args=(application.id, )))
        self.assertEqual(
            Applicant.objects.count(), 0,
            'apply_remove_from_list view: The application was not removed.')
        self.assertRedirects(response,
                             reverse('apply_remove_from_list',
                                     args=(application.id, )),
                             302, 302)
        # 3
        application = self._apply()
        response = self.client.get(reverse('apply_remove_from_list',
                                           args=(application.id, )))
        self.assertEqual(
            Applicant.objects.count(), 1,
            'apply_remove_from_list view: The application shouldn\'t be not \
            removed.')
        self.assertRedirects(response,
                             reverse('apply_remove_from_list',
                                     args=(application.id, )),
                             302, 302)

    def test_job_apply_remove(self):
        """
        Tests job_apply_remove view.
        1 Verifies that only logged in user can access the view.
        2 Verifies that if the job or applicant id not exist a 404 is raised.
        3 Verifies that the owner of the application can delete the
          application and gets redirected properly.
        4 Veririfes that and application can be deleted by a user that's not
          owner fo the application, also verifies that the user is redirected
          properly.
        """
        # 1
        application = self._apply()
        job = application.job
        response = self.client.get(reverse('job_apply_remove',
                                           args=(application.id, job.id)))
        self.assertRedirects(
            response,
            settings.LOGIN_URL + '?next=' + reverse(
                'job_apply_remove', args=(application.id, job.id)),
            msg_prefix='job_apply_remove view was not redirected to login url'
        )
        # 2
        result = self.client.login(username=application.user.username,
                                   password='1')
        self.assertEqual(result, True, 'Login process Failed')
        response = self.client.get(reverse('job_apply_remove',
                                           args=(application.id, 2)))
        self.assertEqual(response.status_code, 404,
                         'job_apply_remove view: A 404 should be raised \
                         because the job doesn\'t exist.')
        response = self.client.get(reverse('job_apply_remove',
                                           args=(2, job.id)))
        self.assertEqual(response.status_code, 404,
                         'job_apply_remove view: A 404 should be raised\
                         because the application doesn\'t exist.')
        # 3
        response = self.client.get(reverse('job_apply_remove',
                                           args=(application.id, job.id)))
        self.assertEqual(
            Applicant.objects.count(), 0,
            'job_apply_remove view: The application was not removed.')
        self.assertRedirects(
            response, reverse('job_details', args=(job.id, )),
            msg_prefix='job_apply_remove view does not redirect to \
            job_details view')
        # 4
        application = self._apply()
        job = application.job
        response = self.client.get(reverse('job_apply_remove',
                                           args=(application.id, job.id)))
        self.assertEqual(
            Applicant.objects.count(), 1,
            'job_apply_remove view: The application shouldn\'t be removed.')
        self.assertRedirects(
            response, reverse('job_details', args=(job.id, )),
            msg_prefix='job_apply_remove view does not redirect to \
            job_details view')

    def test_job_remove(self):
        """
        Tests job_remove view.
        1 Verifies that only logged in user can access the view.
        2 Verifies that if the job id does not exist, then a 404 is raised.
        3 Verifies that only the owner of a job can delete it and then is
          redirected properly
        """
        # 1
        user = self._create_user(True, True)
        project = self._create_project(user.get_profile())
        job = self._create_job(user, project)
        response = self.client.get(reverse('job_remove', args=(job.id, )))
        self.assertRedirects(
            response,
            settings.LOGIN_URL + '?next=' + reverse(
                'job_remove', args=(job.id, )),
            msg_prefix='job_remove view does not redirect to login_url.'
        )
        # 2
        result = self.client.login(username=user.username,
                                   password='1')
        self.assertEqual(result, True, 'Login process Failed')
        response = self.client.get(reverse('job_remove',
                                           args=(2, )))
        self.assertEqual(response.status_code, 404, 'A 404 should be raised.')
        # 3
        response = self.client.get(reverse('job_remove', args=(job.id, )))
        self.assertEqual(Job.objects.count(), 0,
                         'job_remove view: The job was not deleted.')
        self.assertRedirects(
            response, reverse('your_job_post'),
            msg_prefix='job_remove view does not redirected to your_job_post \
            view.')
        user = self._create_user(True, True)
        project = self._create_project(user.get_profile())
        job = self._create_job(user, project)
        response = self.client.get(reverse('job_remove', args=(job.id, )))
        self.assertEqual(Job.objects.count(), 1,
                         'job_remove view: The job should not be deleted.')

    def test_com_remove(self):
        """
        Tests company_remove view.
        1 Verifies that only logged in user can access the view.
        2 Verifies that if the project id does not exist, then a 404 is raised.
        3 Verifies that only the owner of a project can delete it and then is
          redirected properly.
        """
        # 1
        user = self._create_user(True, True)
        project = self._create_project(user.get_profile())
        response = self.client.get(reverse('com_remove', args=(project.id, )))
        self.assertRedirects(
            response,
            settings.LOGIN_URL + '?next=' + reverse(
                'com_remove', args=(project.id, )),
            msg_prefix='com_remove view does not redirect to login_url.'
        )
        # 2
        result = self.client.login(username=user.username,
                                   password='1')
        self.assertEqual(result, True, 'Login process Failed')
        response = self.client.get(reverse('com_remove',
                                           args=(2, )))
        self.assertEqual(response.status_code, 404, 'A 404 should be raised.')
        # 3
        response = self.client.get(reverse('com_remove', args=(project.id, )))
        self.assertEqual(Project.objects.count(), 0,
                         'com_remove view: The project was not deleted.')
        self.assertRedirects(
            response, reverse('your_company'),
            msg_prefix='com_remove view was not redirected to your_company \
            view.'
        )
        user = self._create_user(True, True)
        project = self._create_project(user.get_profile())
        response = self.client.get(reverse('com_remove', args=(project.id, )))
        self.assertEqual(Project.objects.count(), 1,
                         'com_remove view: The project should not be deleted.')

    def test_applicant_status(self):
        """
        Tests applicant_status view.
        1 Verifies that only logged in user can access the view.
        2 Verifies that if the applicant does not exist,then a 404 is raised.
        3 Verifies that just the owner of the job can change the status of a
          applicant and then is redirected properly.
        """
        # 1
        user = self._create_user(True, True)
        project = self._create_project(user.get_profile())
        job = self._create_job(user, project)
        applicant = self._apply(user, job)
        response = self.client.get(
            reverse('applicant_status', args=(applicant.id, 1)))
        self.assertRedirects(
            response,
            settings.LOGIN_URL + '?next=' + reverse(
                'applicant_status', args=(applicant.id, 1)),
            msg_prefix='applicant_status view does not redirect to login_url.'
        )
        # 2
        result = self.client.login(username=user.username,
                                   password='1')
        self.assertEqual(result, True, 'Login process Failed')
        response = self.client.get(reverse('applicant_status',
                                           args=(2, 1)))
        self.assertEqual(response.status_code, 404, 'A 404 should be raised.')
        # 3
        response = self.client.get(reverse('applicant_status',
                                           args=(applicant.id, 1)))
        self.assertEqual(
            Applicant.objects.get(id=1).status, 1,
            'applicant_status view: The applicant status was not modified.')
        self.assertRedirects(
            response, reverse("job_details", args=[job.id]),
            msg_prefix='applicant_status view was not redirected properly.')

        user = self._create_user(True, True)
        project = self._create_project(user.get_profile())
        job = self._create_job(user, project)
        applicant = self._apply(user, job)
        response = self.client.get(reverse('applicant_status',
                                           args=(applicant.id, 1)))
        self.assertEqual(
            Applicant.objects.get(id=applicant.id).status, 0,
            'applicant_status view: The applicant status should not be \
            modified.')

    def test_job_status(self):
        """
        Tests job_status view.
        1 Verifies that the job exists
        2 Verifies that just the owner of the job can change its status and
          then is redirected properly.
        """
        # 1
        response = self.client.get(reverse('job_status', args=(1, 1)))
        self.assertEqual(response.status_code, 404,
                         'job_status view: A 404 should be raised.')
        # 2
        user = self._create_user(True, True)
        project = self._create_project(user.get_profile())
        job = self._create_job(user, project)
        result = self.client.login(username=user.username, password='1')
        self.assertEqual(result, True, 'Login process Failed')
        response = self.client.get(reverse('job_status', args=(job.id, 2)))
        self.assertEqual(Job.objects.get(id=job.id).status, 2,
                         'job_status_view: The job status was not updated.')
        self.assertRedirects(
            response, reverse('job_details', args=(job.id, )),
            msg_prefix='job_status view: The view was not redirected to \
            job_detail view.')
        self.client.logout()
        self.client.get(reverse('job_status', args=(job.id, 3)))
        self.assertEqual(
            Job.objects.get(id=job.id).status, 2,
            'job_status_view: The job status should not be updated.')

    def test_your_job_post(self):
        """
        Tests your_job_post view.
        1 Verifies that only logged in user can reach the view.
        2 Verifies that the filters works properly and the job list is
          delivered to the template.
        """
        # 1
        response = self.client.get(reverse('your_job_post'))
        self.assertRedirects(
            response,
            settings.LOGIN_URL + '?next=' + reverse('your_job_post'),
            msg_prefix='your_job_post view does not redirect to login_url.'
        )
        user = self._create_user(True, True)
        result = self.client.login(username=user.username, password='1')
        self.assertEqual(result, True, 'Login process Failed')
        response = self.client.get(reverse('your_job_post'))
        self.assertEqual(response.status_code, 200, str(response.status_code))
        # 2
        project = self._create_project(user.get_profile())
        for i in xrange(10):
            job = self._create_job(user, project)
        response = self.client.get(
            reverse('your_job_post'),
            {'q': Job.objects.get(id=1).title, }
        )
        self.assertIn(
            'jobs', response.context,
            'your_job_post view: The list of jobs was not delivered to the \
            template.')
        self.assertEqual(
            response.context['jobs'].count(), 1,
            'your_job_post view: The job\'s list was not filtered properly.')

    def test_your_company(self):
        """
        Tests your_company view.
        1 Verifies that only logged in user can reach the view.
        2 Verifies that the filters works properly and the project's list is
          delivered to the template.
        """
        # 1
        response = self.client.get(reverse('your_company'))
        self.assertRedirects(
            response,
            settings.LOGIN_URL + '?next=' + reverse('your_company'),
            msg_prefix='your_company view does not redirect to login_url.')
        # 2
        user = self._create_user(True, True)
        for i in xrange(5):
            project = self._create_project(user.get_profile())
        result = self.client.login(username=user.username, password='1')
        self.assertEqual(result, True, 'Login process Failed')
        response = self.client.get(
            reverse('your_company'),
            {'q': Project.objects.get(id=5).title})
        self.assertIn('company', response.context,
                      'your_company view: The project\'s list was no \
                      delivered to the template.')
        self.assertEqual(response.context['company'].count(), 1,
                         'your_company view: The project\'s list was not \
                         filtered properly.')
