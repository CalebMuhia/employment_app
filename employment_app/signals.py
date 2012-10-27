# -*- coding: utf-8 -*-
""" employment_app signals """

from django.db.models.signals import pre_save
from common.utils import unique_random_string, unique_slug


def create_update_project(sender, instance, **kwargs):
    """
    if the project is being created:
      * creates and sets the unique project_id
      * creates  and sets a unique title_slug
    elif the title has changed:
      * creates and sets a unique slug to title_slug
    """
    if not instance.id:
        instance.project_id = unique_random_string(sender, 'project_id', 15)
        instance.title_slug = unique_slug(
            sender, 'title_slug', instance.title)
    elif sender.objects.get(id=instance.id).title != instance.title:
        instance.title_slug = unique_slug(
            sender, 'title_slug', instance.title)


def setup_signals():
    """ links signals with models """
    from employment_app.models import Project
    pre_save.connect(create_update_project, sender=Project)
