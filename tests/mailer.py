# tests.mailer
# Small email mbox generation utility with real test accounts.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Jun 22 14:44:00 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: mailer.py [ec79c1d] benjamin@bengfort.com $

"""
This small utility function sends random emails to test accounts to generate
an email fixture with which to conduct tests upon. These test accounts are
owned by the admin, and as such, this script should only be run by a core
contributor who knows the email passwords of the test accounts.

The generated mbox can be found in tests/fixtures.
"""

##########################################################################
## Imports
##########################################################################

import os
import time
import random
import smtplib

try:
    import loremipsum as li
except ImportError:
    li = None

from collections import Counter
from itertools import permutations
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


##########################################################################
## TEST ACCOUNTS | DO NOT EDIT!
##########################################################################

ACCOUNTS = {
    'bertram.moody@gmail.com': os.environ.get('BERTRAM_MOODY'),
    'leopold.wentzel@gmail.com': os.environ.get('LEOPOLD_WENTZEL'),
    'mildred.tilcott@gmail.com': os.environ.get('MILDRED_TILCOTT'),
}


def send_message(message):
    """
    Connects to Gmail and sends the email message
    """
    username = message['From']
    password = ACCOUNTS[username]

    if password is None:
        raise ValueError("Cannot send an email without a password!")

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)
    server.sendmail(message['From'], message['To'], message.as_string())
    server.quit()


def generate_message(sender, recipient):
    """
    Generate a Lorem Ipsum email with sender and recipient.
    """
    if li is None:
        raise ValueError("Could not import loremipsum to generate messages!")

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = li.get_sentences(1)[0]

    body = "\n\n".join(li.get_paragraphs(random.randint(1,12)))
    msg.attach(MIMEText(body, 'plain'))

    return msg


def generate_emails(n=100, addrs=list(ACCOUNTS.keys())):
    """
    Generate and send (if True) n random lorem ipsum emails to random
    combinations of email addresses.
    """

    # Create all possible combinations of from and two addresses
    # TODO: Create multiple recipients for email test set
    combos = list(permutations(addrs, 2))

    # Generate and yield messages
    for idx in range(n):
        sender, recipient = random.choice(combos)
        yield generate_message(sender, recipient)


if __name__ == '__main__':

    start  = time.time()
    counts = Counter()
    for msg in generate_emails(n=2000):
        send_message(msg)
        counts[msg['From']] += 1

    print("Sent {} emails in {:0.3f} seconds".format(sum(counts.values()), time.time() - start))
    for item in counts.most_common():
        print("    {}: {} emails".format(*item))
