#!/usr/bin/env python
# tribe-admin
# Administrative utility for working with Tribe data
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Nov 13 14:08:12 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: tribe-admin.py [] benjamin@bengfort.com $

"""
Administrative utility for working with Tribe data
"""

##########################################################################
## Imports
##########################################################################

import sys
import json
import argparse
import networkx as nx

from tribe.utils import timeit
from tribe.extract import MBoxReader

##########################################################################
## Command Variables
##########################################################################

DESCRIPTION = "An administrative utility for the Tribe Social Network Analysis"
EPILOG      = "If there are any bugs or concerns, submit an issue on Github"
VERSION     = "1.1.2"

##########################################################################
## Commands
##########################################################################

def header_analysis(args):
    """
    Perform a header analysis on an MBox
    """

    @timeit
    def timed_inner(path):
        reader  = MBoxReader(path)
        return reader.header_analysis()

    headers, seconds = timed_inner(args.mbox[0])

    if args.show:
        headers.plot()

    json.dump(headers, args.write)
    return "Analysis complete in %0.3f seconds" % seconds

def extract(args):
    """
    Extract a GraphML file from an MBox
    """

    @timeit
    def timed_inner(path):
        reader = MBoxReader(path)
        return reader.extract_graph()

    print "Starting Graph extraction, could take time ..."
    G, seconds = timed_inner(args.mbox[0])
    print "Graph extraction took %0.3f seconds" % seconds

    nx.write_graphml(G, args.write)
    print "GraphML written out to %s" % (args.write.name)
    return ""

def info(args):
    """
    Print information about a GraphML file
    """
    for idx, path in enumerate(args.graphml):
        G = nx.read_graphml(path)
        print nx.info(G)

        if idx < len(args.graphml) - 1:
            print "----"

    return ""

##########################################################################
## Main Function and Methodology
##########################################################################

def main(*args):

    # Construct the argument parser
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG, version=VERSION)
    subparsers = parser.add_subparsers(title='commands', description='Administrative commands for Tribe')

    # Headers Analysis Command
    headers_parser = subparsers.add_parser('headers', help='Perform an analysis of the email headers in an MBox')
    headers_parser.add_argument('-w', '--write', type=argparse.FileType('w'), default=sys.stdout, help='Location to write data to')
    headers_parser.add_argument('-s', '--show', action='store_true', default=False, help='Show graph of key distribution')
    headers_parser.add_argument('mbox', type=str, nargs=1, help='Path or location to MBox for analysis')
    headers_parser.set_defaults(func=header_analysis)

    # Extract Command
    extract_parser = subparsers.add_parser('extract', help='Extract a GraphML file from an MBox')
    extract_parser.add_argument('-w', '--write', type=argparse.FileType('w'), default=sys.stdout, help='Location to write data to')
    extract_parser.add_argument('mbox', type=str, nargs=1, help='Path or location to MBox for analysis')
    extract_parser.set_defaults(func=extract)

    # Graph Info Command
    info_parser = subparsers.add_parser('info', help='Print information about a GraphML file')
    info_parser.add_argument('graphml', nargs="+", type=argparse.FileType('r'), help='Location of MBox(es) to get info for')
    info_parser.set_defaults(func=info)

    # Handle input from the command line
    args = parser.parse_args()            # Parse the arguments
    try:
        msg = args.func(args)             # Call the default function
        parser.exit(0, msg)               # Exit cleanly with message
    except Exception as e:
        parser.error(str(e))              # Exit with error

if __name__ == '__main__':
    main(*sys.argv[1:])
