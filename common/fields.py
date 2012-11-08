# -*- coding: utf-8 -*-
""" common's custom fields """

from django import forms
from django.utils.translation import ugettext_lazy as _
from common.validators import validate_username


class UsernameField(forms.CharField):
    default_error_messages = {
        'invalid': _(u'"This value may contain only letters, numbers and \
        @/./+/-/_ characters."'),
    }
    default_validators = [validate_username]

    def __init__(self, *args, **kwargs):
        """ sets the initial help text """
        super(UsernameField, self).__init__(*args, **kwargs)
        self.help_text = _("Required. 30 characters or fewer. Letters, digits \
        and @/./+/-/_ only.")

    def clean(self, value):
        value = self.to_python(value).strip()
        return super(UsernameField, self).clean(value)


#Snipped from django-extensions
#See here: https://github.com/django-extensions/

# from django.db.models import DateTimeField
# try:
#     from django.utils.timezone import now as datetime_now
# except ImportError:
#     import datetime
#     datetime_now = datetime.datetime.now

# class CreationDateTimeField(DateTimeField):
#     """
#     CreationDateTimeField
#     By default, sets editable=False, blank=True, default=datetime.now
#     """

#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('editable', False)
#         kwargs.setdefault('blank', True)
#         kwargs.setdefault('default', datetime_now)
#         DateTimeField.__init__(self, *args, **kwargs)

#     def get_internal_type(self):
#         return "DateTimeField"

#     def south_field_triple(self):
#         "Returns a suitable description of this field for South."
#         # We'll just introspect ourselves, since we inherit.
#         from south.modelsinspector import introspector
#         field_class = "django.db.models.fields.DateTimeField"
#         args, kwargs = introspector(self)
#         return (field_class, args, kwargs)


# #Snipped from django-extensions
# #See here: https://github.com/django-extensions/
# class ModificationDateTimeField(CreationDateTimeField):
#     """ ModificationDateTimeField

# By default, sets editable=False, blank=True, default=datetime.now

# Sets value to datetime.now() on each save of the model.
# """

#     def pre_save(self, model, add):
#         value = datetime_now()
#         setattr(model, self.attname, value)
#         return value

#     def get_internal_type(self):
#         return "DateTimeField"

#     def south_field_triple(self):
#         "Returns a suitable description of this field for South."
#         # We'll just introspect ourselves, since we inherit.
#         from south.modelsinspector import introspector
#         field_class = "django.db.models.fields.DateTimeField"
#         args, kwargs = introspector(self)
#         return (field_class, args, kwargs)
