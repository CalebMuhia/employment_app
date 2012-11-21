# -*- coding: utf-8 -*-
""" profiles's tests """

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from common.models import Person
from common.tests import BaseOperations as common_BaseOperations
from common.utils import random_string_with_length
from pybb.models import TZ_CHOICES


class BaseOperations(common_BaseOperations):
    """ profiles base operations """

    @staticmethod
    def _init_profile(user):
        """ initializes and returns the user's profile """
        profile = user.get_profile()
        profile.middle_name = random_string_with_length(5)
        profile.gender = Person.GENDER[0][0]
        profile.comment = 'Nothing to say'
        profile.time_zone = TZ_CHOICES[0][0]
        profile.save()
        return profile


class ProfileViewsTests(BaseOperations):
    """ tests for all the proviles views """

    def test_EditProfileWizard(self):
        """
        1.- Verifies that only logged users can reach the view.
        2.- Verifies that the Person Form is initialized properly.
        3.- Verifies that the username will be unique always.
        4.- Verifies that the email will be unique always.
        5.- Verifies that if passwords are provided then they must be equal.
        6.- Verifies that the user and its profile are updated correctly.
        """
        # 1
        response = self.client.get(reverse('profiles_edit_profile'))
        self.assertRedirects(
            response,
            settings.LOGIN_URL + '?next=' + reverse('profiles_edit_profile'),
            msg_prefix='EditProfileWizard view: The view was not redirected \
            properly.')
        user = self._create_user(True)
        profile = self._init_profile(user)
        result = self.client.login(username=user.username, password='1')
        self.assertEqual(result, True, 'Login process Failed')
        response = self.client.get(reverse('profiles_edit_profile'))
        self.assertEqual(
            response.status_code, 200,
            'EditProfileWizard view: The view was not redirected properly.')

        # 2
        form_data = response.context['wizard']['form']
        self.assertTrue(
            form_data['username'].value() == user.username and
            form_data['first_name'].value() == user.first_name and
            form_data['last_name'].value() == user.last_name and
            form_data['email_address'].value() == user.email and
            form_data['id'].value() == profile.id and
            form_data['middle_name'].value() == profile.middle_name and
            form_data['gender'].value() == profile.gender and
            form_data['comment'].value() == profile.comment,
            'EditProfileWizard view: The PersonForm was not \
            initialized properly.')

        # 3
        data = {'0-username': user.username,
                '0-first_name': user.first_name,
                '0-last_name': user.last_name,
                '0-email_address': user.email,
                '0-id': profile.id,
                '0-middle_name': profile.middle_name,
                '0-gender': profile.gender,
                '0-comment': profile.comment,
                '0-time_zone': profile.time_zone
                }
        data_0 = data.copy()
        data_0['edit_profile_wizard-current_step'] = '0'
        response = self.client.post(reverse('profiles_edit_profile'), data_0)
        self.assertFalse(response.context['wizard']['form'].errors,
                         'EditProfileWizard view: No errors should be \
                         raised by the PersonForm.')
        user2 = self._create_user()
        data_0['0-username'] = user2.username
        response = self.client.post(reverse('profiles_edit_profile'), data_0)
        self.assertTrue(response.context['wizard']['form']['username'].errors,
                        'EditProfileWizard view: An error on username \
                        field should be raised because the username is not \
                        unique.')

        # 4
        data_0 = data.copy()
        data_0['edit_profile_wizard-current_step'] = '0'
        data_0['0-email_address'] = user2.email
        response = self.client.post(reverse('profiles_edit_profile'),
                                    data_0)
        self.assertTrue(
            response.context['wizard']['form'].errors and
            response.context['wizard']['form'].errors['email_address'],
            'EditProfileWizard view: An error on email_adress field should \
            be raised because the it\'s not unique.')

        # 5
        data_0 = data.copy()
        data_0['edit_profile_wizard-current_step'] = '0'
        data_0['0-new_password'] = '12345'
        response = self.client.post(reverse('profiles_edit_profile'), data_0)
        self.assertTrue(
            'confirm_new_password' in response.context['wizard'][
                'form'].errors,
            'EditProfileWizard view: An error should be raised because the \
            password was not confirmed.')
        data_0 = data.copy()
        data_0['edit_profile_wizard-current_step'] = '0'
        data_0['0-confirm_new_password'] = '12345'
        response = self.client.post(reverse('profiles_edit_profile'), data_0)
        self.assertTrue(
            'new_password' in response.context['wizard']['form'].errors,
            'EditProfileWizard view: An error should be raised because the \
            password was not confirmed.')
        data_0['0-new_password'] = '54321'
        response = self.client.post(reverse('profiles_edit_profile'), data_0)
        self.assertTrue(
            '__all__' in response.context['wizard']['form'].errors,
            'EditProfileWizard view: An error should be raised because the \
            passwords are no equal.')
        data_0['0-new_password'] = '12345'
        response = self.client.post(reverse('profiles_edit_profile'), data_0)
        self.assertFalse(response.context['wizard']['form'].errors,
                         'EditProfileWizard view: No error should be raised.')

        # 6
        response = self.client.post(reverse('profiles_edit_profile'),
                                    {'0-username': 'user_1',
                                     '0-first_name': 'user_1',
                                     '0-last_name': 'user_1',
                                     '0-email_address': 'user_1@mail.com',
                                     '0-id': profile.id,
                                     '0-middle_name': 'user_1',
                                     '0-gender': Person.GENDER[1][0],
                                     '0-comment': 'aaa',
                                     '0-time_zone': TZ_CHOICES[1][0],
                                     'edit_profile_wizard-current_step': 0
                                     })
        self.assertFalse(response.context['wizard']['form'].errors,
                         'EditProfileWizard view: No error should be raised.')
        response = self.client.post(reverse('profiles_edit_profile'),
                                    {'edit_profile_wizard-current_step': 1,
                                     '1-TOTAL_FORMS': 2,
                                     '1-INITIAL_FORMS': 0})
        user = User.objects.get(id=user.id)
        profile = user.get_profile()
        self.assertRedirects(response, profile.get_absolute_url(),
                             msg_prefix='EditProfileWizard view: The view \
                             wasn\'t redirected properly')
        self.assertTrue(user.username == 'user_1' and
                        user.first_name == 'user_1' and
                        user.last_name == 'user_1' and
                        user.email == 'user_1@mail.com',
                        'EditProfileWizard view: The user wasn\'t \
                        updated properly.')
        self.assertTrue(profile.middle_name == 'user_1' and
                        profile.gender == profile.GENDER[1][0] and
                        profile.comment == 'aaa' and
                        profile.time_zone == TZ_CHOICES[1][0],
                        'EditProfileWizard view: The profile was no updated \
                        properly.')

    def test_profile_detail(self):
        """
        1.- Verifies that a 404 is raised when the username is not found.
        2.- Verifies that if for some reason a user doesn't have a profile a
            404 is raised [This shouldn't happen ever].
        3.- Verifies that the profile object is delivered to the template.
        4.- Verifies that the view is shown properly.
        """
        # 1
        user = self._create_user(True)
        response = self.client.get(
            reverse('profiles_profile_detail', args=('user_0', )))
        self.assertEqual(response.status_code, 404,
                         'profile_detail view: A 404 should be raised because \
                         the username doesn\'t exit.')

        # 2
        user2 = self._create_user()
        profile2 = user2.get_profile()
        profile2.delete()
        response = self.client.get(
            reverse('profiles_profile_detail', args=(user2.username, )))
        self.assertEqual(response.status_code, 404,
                         'profile_detail view: A 404 should be raised because \
                         the profile doesn\'t exit.')

        # 3
        response = self.client.get(
            reverse('profiles_profile_detail', args=(user.username, )))
        self.assertTrue('profile' in response.context,
                        'profile_detail view: The profile object wasn\'t \
                        delivered to the template.')

        # 4
        self.assertEqual(response.status_code, 200,
                         'profile_detail view: The http status code should \
                         be 200.')

    def test_profile_list(self):
        """
        1.- Verifies that the view is shown properly.
        2.- Verifies that a queryset with all the profiles is delivered to the
            template.
        """
        # 1
        response = self.client.get(reverse('profiles_profile_list'))
        self.assertEqual(response.status_code, 200,
                         'profile_list view: The http status code should \
                         be 200.')
        # 2
        for i in xrange(10):
            self._create_user()
        response = self.client.get(reverse('profiles_profile_list'))
        self.assertEqual(response.context['object_list'].count(), 10,
                         'profile_list view: Not all the profiles were \
                         delivered to the template.')
