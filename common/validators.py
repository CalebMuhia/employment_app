# -*- coding: utf-8 -*-
""" common's validators """

import re


def validate_username(value):
    """ validates a username """
    username_re = re.compile(r'^[\w.@+-]+$')
    if not username_re.match(value):
        raise ValidationError(_(u'"This value may contain only letters,\
        numbers and @/./+/-/_ characters."'))
