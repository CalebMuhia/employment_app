# -*- coding: utf-8 -*-
""" employment_app views """

from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from common.utils import send_html_mail
from employment_app.models import Project
from employment_app.forms import ContactForm


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


# class ContactView(TemplateView):


#     #does nothing at the moment, just displace dummy content

#     template_name = "contact.html"

#     def get(self, request, *args, **kwargs):
#         ctx = super(ContactView, self).get_context_data(**kwargs)
#         context = RequestContext(request,
#             ctx
#         )


#         return render_to_response(self.template_name, context)

class ContactView(FormView):
    """ shows/process the page with the contact form """
    template_name = 'contact_us.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        form.save()
        return super(self.__class__, self).form_valid(form)


class ContactSuccessView(TemplateView):
    """ shows a page with a message for sending successfully a contact form """
    template_name = "contact_success.html"
