# -*- coding: utf-8 -*-
""" profiles's tests """

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
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
        5.- Verifies that if passwords are provided then they're equal.
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
        # print dir(response.context['wizard']['form']['username'])
        # response.context['wizard']['form']['username'].value()
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
        response = self.client.post(reverse('profiles_edit_profile'),
                                    data_0)
        self.assertFalse(response.context['wizard']['form'].errors,
                         'EditProfileWizard view: No errors should be \
                         raised by the PersonForm.')
        user2 = self._create_user()
        data_0['0-username'] = user2.username
        response = self.client.post(reverse('profiles_edit_profile'),
                                    data_0)
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
