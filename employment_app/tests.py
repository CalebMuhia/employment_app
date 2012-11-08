# -*- coding: utf-8 -*-
""" employment_app's tests """

from django.contrib.auth.models import User
from common.utils import random_string_with_length
from common.tests import BaseOperations as common_BaseOperations
from employment_app.models import Project
import random
import datetime


class BaseOperations(common_BaseOperations):
    """ holds the basic operations of this application """
    @staticmethod
    def _create_project(person, title=''):
        """ creates and returns a new project """
        return Project.objects.create(
            title=title or random_string_with_length(),
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


class TestProject(BaseOperations):
    """ Project model's tests """

    def test_signal_create_update_project(self):
        """
        1 Verifies that when a project is created, it has unique project_id
          and title_slug.
        2 Verifies that when the project's title is changed, a unique
          title_slug is created.
        """
        # 1
        for i in xrange(100):
            project = self._create_project(self._create_user().get_profile(),
                                           title='Sony project')
            self.assertEqual(
                Project.objects.filter(project_id=project.project_id).count(),
                1,
                'create_update_project signal: The project_id is not unique'
            )
            self.assertEqual(
                Project.objects.filter(title_slug=project.title_slug).count(),
                1,
                'create_update_project signal: The title_slug is not unique'
            )
        # 2
        project.title = 'Sony project 4'
        project.save()
        self.assertEqual(
            Project.objects.filter(title_slug=project.title_slug).count(), 1,
            'create_update_project signal: The title_slug is not unique'
        )
