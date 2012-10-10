# -*- coding: utf-8 -*-
""" employment_app views """

from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    """ shows the homepage """
    return render_to_response("employment_app/home.html",
                              context_instance=RequestContext(request))
