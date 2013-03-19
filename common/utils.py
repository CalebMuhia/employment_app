# -*- coding: utf-8 -*-
""" common utils """

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
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


def send_html_mail(from_email, subject, template_name, data, to_,
                   text_content='', files=None, path='email_templates/'):
    """
    Sends an email using an html template.
    Data: is a dictionary with the data that will be used with the template
    files: attached data list.
    """
    #  hack to send the email with a defined name
    try:
        from_email = "%s <%s>" % (settings.SENDER_NAME, from_email)
    except AttributeError:
        pass

    context = Context(data)
    html_content = mark_safe(render_to_string(
        '%s%s' % (path, template_name), context))
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_])
    msg.attach_alternative(html_content, "text/html")
    if files:
        for afile in files:
            msg.attach_file(afile)
    else:
        pass
    msg.send()
