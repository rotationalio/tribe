# tribe.email
# Data Structures for Email and EmailAddresses
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Nov 14 16:08:56 2014 -0500
#
# Copyright (C) 2014 District Data Labs
# For license information, see LICENSE.txt
#
# ID: emails.py [5232e54] benjamin@bengfort.com $

"""
Data Structures for Email and EmailAddresses
"""

##########################################################################
## Imports
##########################################################################

from collections import namedtuple
from email.utils import parseaddr, formataddr
from tribe.utils import unquote

# 2 to 3 compatibility
from six import string_types
from builtins import str as text

##########################################################################
## EmailMeta NamedTuple
##########################################################################

SENDER      = "sender"      # Should be a single EmailAddress
RECIPIENTS  = "recipients"  # Should be a list of EmailAddresses
COPIED      = "copied"      # Should be a list of EmailAddresses
SUBJECT     = "subject"     # Should be a string or None (not empty string)
DATE        = "date"        # Should be a parsed Python datetime

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

    __slots__ = ('name', 'email')

    def __init__(self, email):
        """
        The email can be either a parsed tuple of (name, addr) pairs or it
        might be a single string that requires parsing for RFC components.
        """

        if isinstance(email, string_types):
            email = parseaddr(unquote(email))

        self.name, self.email  = (unquote(part) for part in email)
        self.email = self.email.lower() # Lowercase the email for normalization

    @property
    def domain(self):
        if self.email:
            return self.email.split("@")[-1]
        return None

    def __repr__(self):
        return "<EmailAddress: %s (%s)>" % (repr(self.name), self.email)

    def __str__(self):
        return text(formataddr((self.name, self.email)))
