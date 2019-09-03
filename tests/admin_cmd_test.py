#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the admin command line."""
import logging
from unittest import TestCase
import requests
from pacifica.policy.admin_cmd import main


class TestAdminCMD(TestCase):
    """Test the admin command line tools."""

    def test_trans_data_release(self):
        """Test transaction data release."""
        main('--verbose', 'data_release', '--keyword', 'transactions.created',
             '--time-after', '365 days after')
        # set logger back to info
        logger = logging.getLogger('urllib3')
        logger.setLevel('INFO')
        resp = requests.get('http://localhost:8121/transactions?_id=1234')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()[0]['suspense_date'], '2018-07-15')
        resp = requests.get(
            'http://localhost:8121/transaction_user?transaction=1234')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()[0]['transaction'], 1234)
        resp = requests.get(
            'http://localhost:8121/transaction_user?transaction=1235')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 0)

    def test_default_data_release(self):
        """Test the data release subcommand."""
        main('data_release', '--time-after',
             '365 days after', '--exclude', u'1234cé')
        resp = requests.get('http://localhost:8121/projects?_id=1234b%C3%A9')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()[0]['suspense_date'], '2017-12-10')
        resp = requests.get(
            'http://localhost:8121/transaction_user?transaction=1234')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()[0]['transaction'], 1234)
