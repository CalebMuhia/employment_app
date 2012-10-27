from django.contrib import admin

from tagging.models import Tag
from jobsboard.models import Job, Applicant


# class Company_Admin(admin.ModelAdmin):
#     fieldsets = (
#         (None, {
#             'fields': ('added_by', 'name',
#                        'address', 'description',
#                        ('telephone', 'fax'), 'tags', )
#         }),
#     )
#     list_display = ('added_by', 'name', 'telephone', 'fax', 'address',
#                     'tags',)
#     list_display_links = ('added_by', 'name', 'telephone', 'fax',
#                           'address', 'tags',)
#     list_filter = ('added_by',)
#     search_fields = ('name', 'telephone', 'fax', 'description', 'address',
#                      'tags',)
#     ordering = ('name', 'added_by',)
#     save_on_top = True


class Job_Admin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('posted_by', 'project', 'title',
                       'description', 'status', 'date_due', 'tags',)
        }),
    )
    list_display = ('posted_by', 'project', 'title', 'description', 'status',
                    'date_due', 'tags')
    list_display_links = ('posted_by', 'project', 'title', 'description',
                          'status', 'date_due', 'tags')
    list_filter = ('status', 'date_due', 'project',)
    search_fields = ('title', 'description', 'tags',)
    ordering = ('status', 'project', 'title', 'posted_by',)
    save_on_top = True


class Applicant_Admin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('job', 'user', 'status',)
        }),
    )
    list_display = ('job', 'user', 'status', 'date_applied',)
    list_display_links = ('job', 'user', 'status', 'date_applied',)
    list_filter = ('status', 'job', 'date_applied',)
    ordering = ('job', 'user',)
    save_on_top = True


admin.site.register(Job, Job_Admin)
admin.site.register(Applicant, Applicant_Admin)
