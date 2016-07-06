# tribe.utils
# Utility functions and decorators for Tribe
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Nov 13 13:44:09 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: utils.py [5232e54] benjamin@bengfort.com $

"""
Utility functions and decorators for Tribe
"""

##########################################################################
## Imports
##########################################################################

import os
import time

from functools import wraps
from dateutil import parser
from datetime import datetime
from dateutil.tz import tzlocal, tzutc
from dateutil.relativedelta import relativedelta
from email.utils import unquote as email_unquote
from email.utils import parsedate_tz, mktime_tz


##########################################################################
## Format constants
##########################################################################

EMAIL_DATETIME   = "%a, %d %b %Y %H:%M:%S %z"
EMAIL_TZ_DATE    = "%a, %d %b %Y %H:%M:%S %z (%Z)"
HUMAN_DATETIME   = "%a %b %d %H:%M:%S %Y %z"
HUMAN_DATE       = "%b %d, %Y"
HUMAN_TIME       = "%I:%M:%S %p"
JSON_DATETIME    = "%Y-%m-%dT%H:%M:%S.%fZ" # Must be UTC
ISO8601_DATETIME = "%Y-%m-%dT%H:%M:%S%z"
ISO8601_DATE     = "%Y-%m-%d"
ISO8601_TIME     = "%H:%M:%S"
COMMON_DATETIME  = "%d/%b/%Y:%H:%M:%S %z"


##########################################################################
## Date Parser Utility
##########################################################################

def parse_date(dtstr):
    """
    Attempts to parse a date with given formats first, then default formats
    """
    # Handle empty string or None
    if not dtstr: return None

    try:
        # Attempt to use the email utils parser first
        dt = parsedate_tz(dtstr)
        if dt is not None:
            return datetime.utcfromtimestamp(mktime_tz(dt)).replace(tzinfo=tzutc())

        # Otherwise use the dateutil parser
        return parser.parse(dtstr)
    except Exception:
        return None


def strfnow(fmt=HUMAN_DATETIME):
    """
    Returns a string representation of the current timestamp
    """
    return datetime.now(tzlocal()).strftime(fmt)


def humanizedelta(*args, **kwargs):
    """
    Wrapper around dateutil.relativedelta (same construtor args) and returns
    a humanized string representing the detla in a meaningful way.
    """
    delta = relativedelta(*args, **kwargs)
    attrs = ('years', 'months', 'days', 'hours', 'minutes', 'seconds')
    parts = [
        '%d %s' % (getattr(delta, attr), getattr(delta, attr) > 1 and attr or attr[:-1])
        for attr in attrs if getattr(delta, attr)
    ]

    return " ".join(parts)


##########################################################################
## Other Helpers and Decorators
##########################################################################

def unquote(s):
    """
    Return a new string which is an unquoted version of str. If str ends
    and begins with double quotes, they are stripped off. Likewise if str
    ends and begins with angle brackets, they are stripped off.

    This method continues to unquote until the string is unchanged.
    """
    new = email_unquote(s)
    if new != s:
        return unquote(new)
    return new


def timeit(func):
    """
    Decorator that times the execution of a function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        return result, time.time() - start
    return wrapper


def filesize(path, suffix='B'):
    """
    Computes a human readable file size for the given path
    """
    num = os.path.getsize(path)

    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0

    return "%.1f%s%s" % (num, 'Yi', suffix)

##########################################################################
## Memoization
##########################################################################

def memoized(fget):
    """
    Return a property attribute for new-style classes that only calls its
    getter on the first access. The result is stored and on subsequent
    accesses is returned, preventing the need to call the getter any more.
    https://github.com/estebistec/python-memoized-property
    """
    attr_name = '_{0}'.format(fget.__name__)

    @wraps(fget)
    def fget_memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fget(self))
        return getattr(self, attr_name)

    def fdel(self):
        if hasattr(self, attr_name):
            delattr(self, attr_name)

    return property(fget_memoized, fdel=fdel)
