#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the admin command line."""
from unittest import TestCase
from time import time
import requests
from jsonschema import validate
from pacifica.policy.admin_cmd import main
from pacifica.policy.search.projects import ProjectsRender
from pacifica.metadata.orm.transsip import TransSIP
from pacifica.metadata.orm.transactions import Transactions


class TestAdminCMD(TestCase):
    """Test the admin command line tools."""

    project_abstract = u'This is a currently active project with a set end date but no clos\u00e9d date'
    es_schema = {
        'type': 'object',
        'properties': {
            '_source': {
                'type': 'object',
                'properties': {
                    'type': {'const': 'transactions'},
                    'obj_id': {'const': 'transactions_67'},
                    'access_url': {'const': 'https://dx.doi.org/10.25584/data.2018-03.127/123456'},
                    'has_doi': {'const': 'true'},
                    'release': {'const': 'true'},
                    'created_date': {'const': '2017-07-15T00:00:00'},
                    'users': {
                        'type': 'object',
                        'properties': {
                            'submitter': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'type': {'const': 'users'},
                                        'obj_id': {'const': 'users_10'},
                                        'display_name': {'const': u'Brown\u00e9 Jr, David\u00e9 '},
                                        'keyword': {'const': u'Brown\u00e9 Jr, David\u00e9 '}
                                    }
                                }
                            }
                        }
                    },
                    'institutions': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'type': {'const': 'institutions'},
                                'obj_id': {'const': 'institutions_47'},
                                'display_name': {'const': u'University of Washington\u00e9'},
                                'keyword': {'const': u'University of Washington\u00e9'}
                            }
                        }
                    },
                    'instruments': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'type': {'const': 'instruments'},
                                'obj_id': {'const': 'instruments_54'},
                                'display_name': {'const': u'NMR PROBES: Nittany Liquid Prob\u00e9s'},
                                'long_name': {'const': u'NMR PROBES: Nittany Liquid Prob\u00e9s'},
                                'keyword': {'const': u'NMR PROBES: Nittany Liquid Prob\u00e9s'},
                                'key_value_pairs': {
                                    'type': 'object',
                                    'properties': {
                                        'key_value_hash': {
                                            'type': 'object',
                                            'properties': {
                                                'temp_f': {'const': '19'},
                                            }
                                        },
                                        'key_value_objs': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'key': {'const': 'temp_f'},
                                                    'value': {'const': '19'}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'instrument_groups': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'type': {'const': 'groups'},
                                'obj_id': {'const': 'groups_1001'},
                                'display_name': {'const': u'nmr_instrum\u00e9nts'},
                                'keyword': {'const': u'nmr_instrum\u00e9nts'}
                            }
                        }
                    },
                    'projects': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'type': {'const': 'projects'},
                                'obj_id': {'const': 'projects_1234a'},
                                'display_name': {'const': u'Pacifica D\u00e9velopment (active no close)'},
                                'long_name': {'const': ''},
                                'abstract': {'const': project_abstract},
                                'title': {'const': u'Pacifica D\u00e9velopment (active no close)'},
                                'keyword': {'const': u'Pacifica D\u00e9velopment (active no close)'},
                            }
                        }
                    },
                    'science_themes': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'type': {'const': 'science_themes'},
                                'obj_id': {'const': u'science_themes_g\u00e9neral'},
                                'display_name': {'const': u'g\u00e9neral'}
                            }
                        }
                    },
                    'key_value_pairs': {
                        'type': 'object',
                        'properties': {
                            'key_value_hash': {
                                'type': 'object',
                                'properties': {
                                    'temp_f': {'const': '27'}
                                }
                            },
                            'key_value_objs': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'key': {'const': 'temp_f'},
                                        'value': {'const': '27'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    def test_default_search_sync(self):
        """Test the data release subcommand."""
        main('searchsync', '--objects-per-page', '4', '--threads', '1', '--exclude', 'keys.104')
        resp = requests.get('http://localhost:9200/pacifica_search/_stats')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['indices']['pacifica_search']['primaries']['docs']['count'], 44)
        resp = requests.get('http://localhost:9200/pacifica_search/doc/transactions_67')
        self.assertEqual(resp.status_code, 200)
        validate(resp.json(), schema=self.es_schema)

    def test_trans_data_release(self):
        """Test transaction data release."""
        main('--verbose', 'data_release', '--keyword', 'transactions.created',
             '--time-after', '365 days after')
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


class TestPerformanceSearchSync(TestCase):
    """Test the performance of search sync."""

    num_trans = 10000
    first_trans_id = 100000

    @classmethod
    def setUpClass(cls):
        """Create a bunch of transactions attached to a project."""
        all_trans = [
            {'_id': trans_id}
            for trans_id in range(cls.first_trans_id, cls.first_trans_id+cls.num_trans)
        ]
        trans_obj = Transactions()
        trans_obj._insert(all_trans)
        all_transsip = [
            {'_id': trans_id, 'submitter': '10', 'instrument': '54', 'project': '1234a'}
            for trans_id in range(cls.first_trans_id, cls.first_trans_id+cls.num_trans)
        ]
        transsip_obj = TransSIP()
        transsip_obj._insert(all_transsip)

    def test_project_transactions(self):
        """Test getting a projects transactions is performant."""
        start_time = time()
        resp = ProjectsRender.get_transactions(_id='1234a')
        end_time = time()
        self.assertEqual(len(resp), 10002)
        self.assertTrue(end_time - start_time < 1)
