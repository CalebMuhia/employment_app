# -*- coding: utf-8 -*-
""" common utils """

from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify
import random


def random_string_with_length(string_length=10):
    """
    returns a random string with a defined length
    """
    alphanumeric = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456\
7890"
    return "".join(
        [random.choice(alphanumeric) for i in xrange(string_length)])


def unique_random_string(model, field, string_length=10):
    """
    returns a unique string for the model field.
    """
    unique = False
    while (not unique):
        random_str = random_string_with_length(string_length)
        try:
            model.objects.get(**{'{0}'.format(field): random_str})
        except ObjectDoesNotExist:
            unique = True
    return random_str


def unique_slug(model, slug_field, data):
    """  """
    unique = False
    uslug = slugify(data)
    ucode = 0
    while (not unique):
        try:
            model.objects.get(**{'{0}'.format(slug_field): uslug})
        except ObjectDoesNotExist:
            unique = True
        else:
            uslug += str(ucode)
            ucode += 1
    return uslug