#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This is the admin main method."""
from __future__ import print_function, absolute_import
import logging
from sys import argv as sys_argv
from argparse import ArgumentParser
from datetime import timedelta
from six import text_type
from .data_release import data_release, VALID_KEYWORDS

logging.basicConfig()
LOGGER = logging.getLogger('urllib3')


def objstr_to_timedelta(obj_str):
    """Turn an object string of the format X unit ago into timedelta."""
    value, unit, check = obj_str.split()
    assert check in ['after', 'ago']
    return timedelta(**{unit: float(value)})


def objstr_to_keyword(obj_str):
    """Verify the obj_str is a valid keyword."""
    assert obj_str in VALID_KEYWORDS
    return obj_str


def datarel_options(datarel_parser):
    """Add data release options to the parser."""
    datarel_parser.add_argument(
        '--exclude', dest='exclude',
        help='id of keyword prefix to exclude.',
        nargs='*', default=set(), type=text_type
    )
    datarel_parser.add_argument(
        '--keyword', dest='keyword', type=objstr_to_keyword,
        help='keyword one of {}.'.format(', '.join(VALID_KEYWORDS)),
        required=False, default=VALID_KEYWORDS[0]
    )
    datarel_parser.add_argument(
        '--time-after', dest='time_after', type=objstr_to_timedelta,
        help='set suspense date on data to X days after keyword (i.e. --time-after="7 days after").',
        required=False, default=timedelta(days=36500)
    )
    datarel_parser.add_argument(
        '--time-ago', dest='time_ago', type=objstr_to_timedelta,
        help='only objects updated after X days ago (i.e. --time-ago="7 days ago").',
        required=False, default=timedelta(days=3650)
    )
    datarel_parser.set_defaults(func=data_release)


def create_subcommands(subparsers):
    """Create the subcommands from the subparsers."""
    datarel_parser = subparsers.add_parser(
        'data_release',
        help='data_release help',
        description='data release by policy'
    )
    return datarel_parser


def main(*argv):
    """Main method for admin command line tool."""
    parser = ArgumentParser()
    parser.add_argument(
        '--verbose', default=False, action='store_true',
        help='enable verbose debug output'
    )
    subparsers = parser.add_subparsers(help='sub-command help')
    datarel_parser = create_subcommands(subparsers)
    datarel_options(datarel_parser)
    if not argv:  # pragma: no cover
        argv = sys_argv[1:]
    args = parser.parse_args(argv)
    if args.verbose:
        LOGGER.setLevel('DEBUG')
    args.func(args)
