# -*- coding: utf-8 -*-
""" employment_app views """

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import TemplateView
from employment_app.models import Project


def home(request):
    """ shows the homepage """
    return render_to_response("home.html",
                              context_instance=RequestContext(request))


# def project_profile(request, slug):
#     """ shows the project's details """
#     obj = get_object_or_404(Project, title_slug=slug)
#     return render_to_response("employment_app/project_profile.html",
#                               {'project': obj},
#                               context_instance=RequestContext(request))


class ContactView(TemplateView):


    #does nothing at the moment, just displace dummy content

    template_name = "contact.html"

    def get(self, request, *args, **kwargs):
        ctx = super(ContactView, self).get_context_data(**kwargs)
        context = RequestContext(request,
            ctx
        )


        return render_to_response(self.template_name, context)