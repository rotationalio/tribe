# tribe.email
# Data Structures for Email and EmailAddresses
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Nov 14 16:08:56 2014 -0500
#
# Copyright (C) 2014 District Data Labs
# For license information, see LICENSE.txt
#
# ID: email.py [] benjamin@bengfort.com $

"""
Data Structures for Email and EmailAddresses
"""

##########################################################################
## Imports
##########################################################################

import re

from collections import namedtuple

##########################################################################
## EmailMeta NamedTuple
##########################################################################

SENDER      = "sender"      # Should be a single EmailAddress
RECIPIENTS  = "recipients"  # Should be a list of EmailAddresses
COPIED      = "copied"      # Should be a list of EmailAddresses
SUBJECT     = "subject"     # Should be a string or None (not empty string)
DATE        = "date"        # Should be a parsed Python datetime

EMAILRE     = re.compile(r'"?(.*)"?\s*\<(.+@.+)\>', re.I)
META_FIELDS = (SENDER, RECIPIENTS, COPIED, SUBJECT, DATE)

EmailMeta   = namedtuple("EmailMeta", META_FIELDS)

##########################################################################
## Email Parser
##########################################################################

class EmailAddress(object):
    """
    Implements a simple email parser for storing email data where an email
    is represented as follows: John Doe <jdoe@example.com>.
    """

    __slots__ = ('_raw', 'name', 'email')

    def __init__(self, raw):
        self._raw  = raw.strip()               # Store raw data without whitespace
        self.name  = self._parse_name(raw)     # Extract the name if it exists
        self.email = self._parse_email(raw)    # Extract the email or just use the raw

    def _parse_name(self, email):
        match = EMAILRE.match(email)
        if match:
            return match.group(1).strip()
        return None

    def _parse_email(self, email):
        match = EMAILRE.match(email)
        if match:
            return match.group(2)
        return email.strip().lstrip("<").rstrip(">")

    def is_parsed(self):
        """
        Determines if the email was able to be parsed or not.
        """
        if EMAILRE.match(self._raw):
            return True
        return False

    @property
    def domain(self):
        if self.email:
            return self.email.split("@")[-1]
        return None

    def __repr__(self):
        if self.is_parsed():
            return "<ParsedEmail: %s (%s)>" % (self.name, self.email)
        else:
            return self._raw

    def __str__(self):
        return unicode(self)

    def __unicode__(self):
        if self.name and self.email:
            return u"%s <%s>" % (self.name, self.email)
        elif self.email:
            return self.email
        else:
            return u"Unknown Email"
