# -*- coding: utf-8 -*-
""" employment_app admin """

from django.contrib import admin
from employment_app.models import Client, Developer, \
    Project, Project_Comment, Person_Project


class ClientAdmin(admin.ModelAdmin):
    pass

admin.site.register(Client, ClientAdmin)
admin.site.register(Developer)
admin.site.register(Project)
admin.site.register(Project_Comment)
admin.site.register(Person_Project)
