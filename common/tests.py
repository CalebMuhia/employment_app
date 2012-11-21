# -*- coding: utf-8 -*-
""" common's tests """

from django.test import TestCase
from django.contrib.auth.models import User
from common.models import Person
from common.utils import random_string_with_length


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
            first_name=random_string_with_length(5),
            last_name=random_string_with_length(5),
            email=random_string_with_length(5) + '@mail.com',
            is_active=active, is_staff=True, is_superuser=superuser)
        u.set_password('1')
        u.save()
        return u


class TestPerson(BaseOperations):
    """ Person model's tests """

    def test_signal_user_created(self):
        """
        Verifies that just when a user is created its userprofile(Person model)
        is created too.
        """
        user = self._create_user()
        self.assertEqual(User.objects.count(), 1, 'user_created signal: \
        The user was no created.')
        self.assertEqual(Person.objects.count(), 1, 'user_created signal: The \
        userprofile was no created.')
        self.assertTrue(user.get_profile(),
                        'user_created_signal: The userprofile was no created.')
        user.username = 'user1'
        user.save()
        self.assertNotEqual(Person.objects.count(), 2, 'user_created signal: \
        A second user profile was created.')
        self.assertNotEqual(Person.objects.count(), 0, 'user_created signal: \
        The userprofile was deleted.')
        self.assertTrue(user.get_profile(),
                        'user_created_signal: The userprofile is not linked \
                        any more with the user.')
