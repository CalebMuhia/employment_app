# -*- coding: utf-8 -*-
""" common admin """

from django.contrib import admin
from common.models import FeedBack, Challenge_Question, \
    Phone_Number, Skill

admin.site.register(FeedBack)
admin.site.register(Challenge_Question)
admin.site.register(Phone_Number)
admin.site.register(Skill)
