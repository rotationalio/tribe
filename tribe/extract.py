# tribe.extract
# Extracts social network data from an email mbox
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Nov 12 21:19:51 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: extract.py [6c9398c] benjamin@bengfort.com $

"""
Extracts social network data from an email mbox and exports it as a GraphML
file format (which is suitable to use with Gephi, Neo4j etc)
"""

##########################################################################
## Imports
##########################################################################

import networkx as nx

from mailbox import mbox
from tribe.stats import FreqDist
from itertools import combinations
from email.utils import getaddresses
from tribe.emails import EmailMeta, EmailAddress
from tribe.progress import AsyncProgress as Progress
from tribe.utils import parse_date, strfnow, filesize


##########################################################################
## MBoxReader
##########################################################################

class MBoxReader(object):

    def __init__(self, path):
        self.path  = path
        self.mbox  = mbox(path)

        # Track errors through extraction process
        self.errors = FreqDist()

    def __iter__(self):
        for msg in self.mbox:
            yield msg

    def __len__(self):
        return self.count()

    def header_analysis(self):
        """
        Performs an analysis of the frequency of headers in the Mbox
        """
        headers = FreqDist()
        for msg in self:
            headers['X-Tribe-Message-Count'] += 1
            for key in msg.keys():
                headers[key] += 1

        return headers

    def count(self):
        """
        Returns the number of emails in the MBox
        """
        return sum(1 for msg in self)

    def extract(self):
        """
        Extracts the meta data from the MBox
        """

        def parse(msg):
            """
            Inner function that knows how to extract an EmailMeta
            """
            source = msg.get('From', '')
            if not source: return None

            tos = msg.get_all('To', []) + msg.get_all('Resent-To', [])
            ccs = msg.get_all('Cc', []) + msg.get_all('Resent-Cc', [])

            # construct data output
            return EmailMeta(
                EmailAddress(source),
                [EmailAddress(to) for to in getaddresses(tos)],
                [EmailAddress(cc) for cc in getaddresses(ccs)],
                msg.get('Subject', '').strip() or None,
                parse_date(msg.get('Date', '').strip() or None),
            )

        # Iterate through all messages in self, tracking errors
        # Catch any exceptions and record them, then move forward
        # NOTE: This will allow the progress bar to work
        for msg in self:
            try:
                email = parse(msg)
                if email is not None:
                    yield email
            except Exception as e:
                self.errors[e] += 1
                continue

    def extract_graph(self):
        """
        Extracts a Graph where the nodes are EmailAddress
        """

        def relationships(email):
            """
            Inner function that constructs email relationships
            """
            people = [email.sender,]
            people.extend(email.recipients)
            people.extend(email.copied)

            people = filter(lambda p: p is not None, people)            # Filter out any None addresses
            people = set(addr.email for addr in people if addr.email)   # Obtain only unique people
            people = sorted(people)                                     # Sort lexicographically for combinations

            for combo in combinations(people, 2):
                yield combo


        # Keep track of all the email to email links
        links  = FreqDist()
        emails = 0

        # Iterate over all the extracted emails
        # Catch exceptions, if any, and move forward
        # NOTE: This will allow the progress bar to work
        # NOTE: This will build the graph data structure in memory
        for email in self.extract():
            emails += 1
            try:
                for combo in relationships(email):
                    links[combo] += 1
            except Exception as e:
                self.errors[e] += 1
                continue

        # Construct the networkx graph with details about generation.
        G = nx.Graph(
            name="Email Network", mbox=self.path,
            extracted=strfnow(), n_emails=emails,
            mbox_size=filesize(self.path),
        )

        # Add edges to the graph with various weight properties from counts.
        # NOTE: memoization is used here in the FreqDist to speed things up.
        for link in links.keys():
            link_data = {
                "weight": links.freq(link),
                "count":  links[link],
                "norm":   links.norm(link),
            }
            G.add_edge(*link, **link_data)

        # Return the generated graph
        return G


class ConsoleMBoxReader(MBoxReader):
    """
    Wraps the __iter__ class with a console based progress bar for console
    output and timing information (especially for large MBox files).

    Note: in order for this to work, the super class must always use __iter__
    Note: this is a bit more expensive because a count is always performed.
    """

    def __init__(self, *args, **kwargs):
        # Get console settings from the kwargs
        self.verbose = kwargs.pop('verbose', True)

        # Initialize the MBoxReader
        super(ConsoleMBoxReader, self).__init__(*args, **kwargs)

    def __iter__(self):
        if self.verbose:
            print("Initializing MBox iteration on {} ({})".format(
                self.path, filesize(self.path)
            ))

        # Build the progress bar
        pbar = Progress()

        # Iterate through the messages and update the progress bar
        for msg in super(ConsoleMBoxReader, self).__iter__():
            yield msg
            pbar.update()

        # Stop the progress bar and flush
        pbar.stop()

    def count(self, refresh=False):
        """
        Memoize the count function to minimize the reads of large MBox files.
        """
        if not hasattr(self, '_count') or refresh:
            self._count = sum(1 for _ in super(ConsoleMBoxReader, self).__iter__())
        return self._count


if __name__ == '__main__':
    # Dump extracted email meta data to a pickle file for testing
    import pickle

    reader = MBoxReader("fixtures/benjamin@bengfort.com.mbox")
    emails = list(reader.extract())
    with open('fixtures/emails.pickle', 'w') as f:
        pickle.dump(emails, f, pickle.HIGHEST_PROTOCOL)
