# -*- coding: utf-8 -*-
# Admin user profile info from:
#https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users

""" employment_app admin """

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from employment_app.models import Project, Project_Comment, Person_Project

# # Define an inline admin descriptor for UserProfile model
# # which acts a bit like a singleton
# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'profile'

# # Define a new User admin
# class UserAdmin(UserAdmin):
#     inlines = (UserProfileInline, )

# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'project_id')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Project_Comment)
admin.site.register(Person_Project)
