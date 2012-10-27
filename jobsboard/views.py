# -*- coding: utf-8 -*-
""" jobsboard view """

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden,\
    HttpResponseRedirect
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext


from jobsboard.models import *
from jobsboard.forms import *
from jobsboard.signals import *

from django.core.signals import *
from django.db.models.signals import *

from employment_app.forms import ProjectForm
from employment_app.models import Project


jobstatus = 1


def job_list(request, template_name="jobsboard/jobs_list.html"):
    """
    display the list of jobs
    """
    is_me = False
    jobs = Job.objects.all().order_by('-date_added')
    if request.user.is_authenticated():
        other_user = get_object_or_404(User, username=request.user.username)
        if request.user == request.user:
            is_me = True
        else:
            is_me = False

    search_terms = request.GET.get('q', '')
    if search_terms:
        jobs = (jobs.filter(title_slug__icontains=search_terms)
                | jobs.filter(title__icontains=search_terms)
                | jobs.filter(description__icontains=search_terms)
                | jobs.filter(status__icontains=search_terms)
                | jobs.filter(date_added__icontains=search_terms)
                | jobs.filter(date_updated__icontains=search_terms)
                | jobs.filter(project__title__icontains=search_terms)
                | jobs.filter(date_due__icontains=search_terms)
                | jobs.filter(tags__icontains=search_terms))
    return render_to_response(template_name, dict({
        "jobs": jobs,
        "is_me": is_me,
    }), context_instance=RequestContext(request))


@login_required
def job_create(request, form_class=JobForm,
               template_name="jobsboard/job_form.html"):
    """
    post new job.  the user must be verified first
    """

    job_form = form_class()
    if request.method == "POST":
        #job_form = form_class(request.user, request.POST)
        job_form = form_class(request.POST)
        if job_form.is_valid():
            job = job_form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(
                request, _("The job '%s' was added successfully.") % job.title)

            return HttpResponseRedirect(reverse("jobsboard.views.job_list"))
    else:
        job_form = form_class()

    return render_to_response(template_name, {
        "job_form": job_form
    }, context_instance=RequestContext(request))


@login_required
def job_edit(request, jobid, form_class=JobForm,
             template_name="jobsboard/job_form.html"):
    """
    edit job posted.
    The user may able to set the status and update information about
    the job posted.
    """

    job_obj = Job.objects.get(id=jobid)
    is_edit = True
    if job_obj.posted_by == request.user:
        job_form = form_class(request.POST, instance=job_obj)
        if request.method == "POST":
            if job_form.is_valid():
                job = job_form.save(commit=False)
                job.id = job_obj.id
                job.save()
                messages.success(
                    request,
                    _("The job '%s' was changed successfully. ") % job.title)
                return HttpResponseRedirect(
                    reverse("jobsboard.views.job_detail", args=[job_obj.id]))
        else:
            job_form = form_class(instance=job_obj)
    else:
        return HttpResponseRedirect(reverse("jobsboard.views.job_list"))
    return render_to_response(template_name, {
        "job_form": job_form,
        "job_obj": job_obj,
        "is_edit": is_edit,
    }, context_instance=RequestContext(request))


def job_detail(request, jobid, form_class=ApplicantForm,
               template_name="jobsboard/job_detail.html"):
    """
    display the job information and company.
    the applicant may able to apply if he/she is a verified user
    """
    job_obj = get_object_or_404(Job, id=jobid)
    meapp = Applicant.objects.filter(user=request.user, job=job_obj)
    app = Applicant.objects.filter(job=job_obj)
    job_d = Job.objects.filter(id=jobid)

    if request.method == "POST":
        app_form = form_class(request.POST)
        if app_form.is_valid():
            app = app_form.save(commit=False)
            app.user = request.user
            app.job = job_obj
            app.status = 1
            app.save()
            messages.success(
                request,
                _("The applicant '%s' was applied successfully. ") % app.job)
            return HttpResponseRedirect(
                reverse("jobsboard.views.job_detail", args=[job_obj.id]))
    else:
        app_form = form_class()

    return render_to_response(template_name, {
        "job": job_obj,
        "apps": app,
        "app_form": app_form,
        "jobstatus": jobstatus,
        "meapp": meapp,
    }, context_instance=RequestContext(request))


@login_required
def applicant_status(request, id, status):
    """
    change the status of the applicant
        1 - Open
        2 - Filled
        3 - Cancelled
        4 - Stale

    the user who post the job is authorize to change the applicants status
    """

    applicant = Applicant.objects.get(pk=id)
    job = get_object_or_404(Job, id=applicant.job.id)

    if job.posted_by == request.user:
        applicant.status = status
        applicant.save()
        messages.success(
            request,
            _("The applicant '%s' was changed successfully.") % applicant.user)
        return HttpResponseRedirect(
            reverse("jobsboard.views.job_detail", args=[job.id]))
    else:
        messages.error(
            request,
            _("Not successfully save. May be you are not authorize"))
        return HttpResponseRedirect(reverse("jobsboard.views.job_detail",
                                            args=[job.id]))


@login_required
def apply_remove(request, id):
    """
    remove applicant from applied jobs
    """

    apply = Applicant.objects.get(pk=id)
    if apply.user == request.user:
        apply.delete()
        messages.success(
            request, _("Successfully remove from '%s'") % apply.job)
    else:
        messages.error(
            request, _("Not successfully remove from '%s'") % apply.job)
    return HttpResponseRedirect(reverse("jobsboard.views.job_list"))


@login_required
def apply_list(request, template_name='jobsboard/applied_jobs.html'):
    """
    display the list of users applied jobs
    """
    job = Applicant.objects.filter(user=request.user)
    return render_to_response(template_name, {
        "jobs": job,
    }, context_instance=RequestContext(request))


@login_required
def apply_remove_from_list(request, id):
    """
    remove applicant from the list user''s applied
    """
    try:
        apply = Applicant.objects.get(pk=id)
    except Exception:
        return HttpResponseRedirect(reverse('jobsboard.views.apply_list'))

    if apply.user == request.user:
        apply.delete()
        msg = "Your application has been successfully removed from '%s'" % (
            apply.job,)
        messages.success(request, _(msg))
    else:
        msg = "Your application has not been removed from '%s'" % (apply.job,)
        messages.error(request, _(msg))
    return HttpResponseRedirect('')


@login_required
def job_apply_remove(request, id, jobid):
    """
    remove applicant by employers
    """
    job = get_object_or_404(Job, id=jobid)
    apply = Applicant.objects.get(pk=id)
    if job.posted_by == request.user:
        apply.delete()
        messages.success(
            request, _("Successfully remove from '%s'") % apply.job)
    else:
        messages.error(
            request, _("Not successfully remove from '%s'") % apply.job)
    return HttpResponseRedirect(
        reverse("jobsboard.views.job_detail", args=[jobid]))


@login_required
def job_remove(request, id):
    """
    removes job by the employer
    """
    job = get_object_or_404(Job, id=id)
    if job.posted_by == request.user:
        job.delete()
        messages.success(
            request, _("Successfully remove from '%s'") % job.title)
    else:
        messages.error(
            request, _("Not successfully remove from '%s'") % job.title)
    return HttpResponseRedirect(reverse('jobsboard.views.your_job_post'))


def job_status(request, status, id):
    """
    employer change the status of applicant
    """

    job = get_object_or_404(Job, id=id)
    if job.posted_by == request.user:
        job.status = status
        job.save()
        messages.success(
            request, _("Successfully update the '%s'") % job.title)
    else:
        messages.error(
            request, _("Not successfully update the '%s'") % job.title)
    return HttpResponseRedirect(
        reverse("jobsboard.views.job_detail", args=[id]))


@login_required
def company_remove(request, id):
    """
    remove the company by the user who added the company
    """
    com = get_object_or_404(Project, id=id)
    if com.person.user == request.user:
        com.delete()
        messages.success(
            request, _("Successfully remove from '%s'") % com.title)
    else:
        messages.error(
            request, _("Not successfully remove from '%s'") % com.title)
    return HttpResponseRedirect(reverse('jobsboard.views.your_company'))


def company_list(request, template_name="jobsboard/company_list.html"):
    """
    display the list of company
    """
    is_me = False
    project = Project.objects.all().order_by('title')
    if request.user.is_authenticated():
        other_user = get_object_or_404(User, username=request.user.username)

        if request.user == other_user:
            is_me = True
        else:
            is_me = False

    search_terms = request.GET.get('q', '')
    if search_terms:
        project = (project.filter(title__icontains=search_terms)
                   | project.filter(public_description__icontains=search_terms)
                   | project.filter(
                       person__user__first_name__icontains=search_terms)
                   | project.filter(
                       person__middle_name__icontains=search_terms)
                   | project.filter(
                       person__user__last_name__icontains=search_terms)
                   | project.filter(registration__icontains=search_terms))
    return render_to_response(template_name, dict({
        "company": project,
        "is_me": is_me,
    }), context_instance=RequestContext(request))


@login_required
def company_create(request, form_class=ProjectForm,
                   template_name="jobsboard/company_form.html"):
    """
    add company.  verified user only can be able to add new company
    """
    if request.method == "POST":
        com_form = form_class(request.POST)
        if com_form.is_valid():
            com = com_form.save(commit=False)
            com.person = request.user.get_profile()
            com.save()
            messages.success(
                request, _("Successfully saved post '%s'") % com.title)
            return HttpResponseRedirect(
                reverse("jobsboard.views.company_list"))
    else:
        com_form = form_class()

    return render_to_response(template_name, {
        "com_form": com_form
    }, context_instance=RequestContext(request))


#Modify the existing company
@login_required
def company_edit(request, comid, form_class=ProjectForm,
                 template_name="jobsboard/company_form.html"):
    """
    edit the company detail by verified user who added the company
    """

    com_obj = get_object_or_404(Project, id=comid)
    if com_obj.person == request.user.get_profile():
        if request.method == "POST":
            com_form = form_class(request.POST, instance=com_obj)
            if com_form.is_valid():
                com = com_form.save(commit=False)
                com.id = com_obj.id
                com.save()
                messages.success(
                    request, _("Successfully saved '%s'") % com.title)
                return HttpResponseRedirect(
                    reverse("jobsboard.views.company_list"))
        else:
            com_form = form_class(instance=com_obj)
    else:
        return HttpResponseRedirect(reverse("jobsboard.views.company_list"))
    return render_to_response(template_name, {
        "com_form": com_form,
        "com_obj": com_obj,
    }, context_instance=RequestContext(request))


def company_detail(request, slug,
                   template_name="jobsboard/company_detail.html"):
    """
    displays the detail of the company
    """
    com_d = get_object_or_404(Project, title_slug=slug)
    job_d = Job.objects.filter(project=com_d)
    return render_to_response(template_name, {
        "com": com_d,
        "jobs": job_d,
    }, context_instance=RequestContext(request))


@login_required
def your_job_post(request, template_name="jobsboard/your_job_post.html"):
    """
    display the list of job posted by verified user
    """
    job = Job.objects.filter(posted_by=request.user)

    search_terms = request.GET.get('q', '')
    if search_terms:
        job = (job.filter(title_slug__icontains=search_terms)
               | job.filter(title__icontains=search_terms)
               | job.filter(description__icontains=search_terms)
               | job.filter(status__icontains=search_terms)
               | job.filter(date_added__icontains=search_terms)
               | job.filter(date_updated__icontains=search_terms)
               | job.filter(project__title__icontains=search_terms)
               | job.filter(date_due__icontains=search_terms)
               | job.filter(tags__icontains=search_terms))

    return render_to_response(template_name, {
        "jobs": job,
    }, context_instance=RequestContext(request))


#List of project you added
@login_required
def your_company(request, template_name="jobsboard/your_company.html"):
    """
    display the list of company of verified user added
    """
    company = Project.objects.filter(person__user=request.user)
    search_terms = request.GET.get('q', '')
    if search_terms:
        company = (company.filter(title__icontains=search_terms)
                   | company.filter(public_description__icontains=search_terms)
                   | company.filter(registration__icontains=search_terms))
    return render_to_response(template_name, dict({
        "company": company,
    }), context_instance=RequestContext(request))
