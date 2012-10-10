# -*- coding: utf-8 -*-
""" common admin """

from django.contrib import admin
from common.models import Person, FeedBack, Challengue_Question, \
    Phone_Number, Skill, Person_Skill, Location


class PersonAdmin(admin.ModelAdmin):
    """ admin model of the Person """
    pass

admin.site.register(Person, PersonAdmin)
admin.site.register(FeedBack)
admin.site.register(Challengue_Question)
admin.site.register(Phone_Number)
admin.site.register(Skill)
admin.site.register(Person_Skill)
admin.site.register(Location)
