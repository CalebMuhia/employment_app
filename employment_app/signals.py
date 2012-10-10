# -*- coding: utf-8 -*-
""" employment_app signals """

from django.db.models.signals import pre_save
from common.utils import unique_random_string


def create_project_id(sender, instance, **kwargs):
    """
    creates and sets the unique project_id only if the project is being
    created
    """
    if not instance.id:
        from employment_app.models import Project
        instance.project_id = unique_random_string(Project, 'project_id', 15)


def setup_signals():
    """ links signals with models """
    from employment_app.models import Project
    pre_save.connect(create_project_id, sender=Project)
