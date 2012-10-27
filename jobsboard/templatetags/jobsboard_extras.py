#!/usr/bin/env python

from django.template import Library, Node, TemplateSyntaxError
from django.db.models import get_model

from jobsboard.models import *

register = Library()


class RandomLinksNode(Node):
    """
    Class to view the job in random
    """
    def __init__(self, num, varname):
        self.num, self.varname = num, varname

    def render(self, context):
        context[self.varname] = Job.objects.filter(status=1).order_by("?")[:self.num]
        return ''


def get_random_jobs(parser, token):
    """
    Function to get RandomLinksNode
    Code for displaying the random job.
    You can assign any number you want to view in the list
            {% get_random_job 5 as jobs %}
            {% for job in jobs %}
                {{ job.title }}
            {% endfor %}
    """

    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "get_random_jobs tag takes exactly 2 arguments"

    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to the get_random_jobs tag must be 'as'"

    return RandomLinksNode(bits[1], bits[3])
get_random_jobs = register.tag(get_random_jobs)


class LatestLinksNode(Node):
    """
    Class to view the latest jobs
    """
    def __init__(self, num, varname):
        self.num, self.varname = num, varname

    def render(self, context):
        context[self.varname] = Job.objects.all().order_by('-date_added')[:self.num]
        return ''


def get_latest_jobs(parser, token):
    """
    Function to get the LatestLinksNode to view the Latest job
    Code for displaying the latest job.
            {% get_latest_job 5 as jobs %}
            {% for job in jobs %}
                {{ job.title }}
            {% endfor %}
    """

    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "get_latest_jobs tag takes exactly 2 arguments"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to the get_latest_jobs tag must be 'as'"
    return LatestLinksNode(bits[1], bits[3])
get_latest_jobs = register.tag(get_latest_jobs)
