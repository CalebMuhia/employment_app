# -*- coding: utf-8 -*-
""" common signals """

from django.contrib.auth.models import User, Permission
from django.db.models import ObjectDoesNotExist
from django.db.models.signals import post_save
from common.utils import unique_random_string


def user_created(sender, instance, created, **kwargs):
    """
    sets the pybbm user permissions and creates the profile Person only if the
    User has been just created
    """
    if created:
        try:
            add_post_permission = Permission.objects.get_by_natural_key(
                'add_post', 'pybb', 'post')
            add_topic_permission = Permission.objects.get_by_natural_key(
                'add_topic', 'pybb', 'topic')
        except ObjectDoesNotExist:
            pass
        else:
            instance.user_permissions.add(add_post_permission,
                                          add_topic_permission)
            instance.save()
        from common.models import Person
        person_id = unique_random_string(Person, 'person_id', 16)
        Person(user=instance, person_id=person_id).save()


def setup_signals():
    """ links signals with models """
    post_save.connect(user_created, sender=User)
