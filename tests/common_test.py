#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Common server setup code for CherryPy testing."""
# import logging
import os
from json import dumps, loads
import cherrypy
from pacifica.policy.root import Root, error_page_default


class CommonCPSetup:
    """Common CherryPy setup class."""

    # pylint: disable=no-member
    def get_json_page(self, path, valid_query):
        """Get a json page and validate its return format."""
        self.getPage(path,
                     self.headers +
                     [('Content-Length', str(len(dumps(valid_query))))],
                     'POST',
                     dumps(valid_query))
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'application/json')
        return loads(self.body.decode('UTF-8'))

    @staticmethod
    def setup_server():
        """Setup each test by starting the CherryPy server."""
        # logger = logging.getLogger('urllib2')
        # logger.setLevel(logging.DEBUG)
        # logger.addHandler(logging.StreamHandler())
        os.environ['POLICY_CPCONFIG'] = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), '..', 'server.conf')
        cherrypy.config.update({'error_page.default': error_page_default})
        cherrypy.config.update(os.environ['POLICY_CPCONFIG'])
        cherrypy.tree.mount(Root(), '/', os.environ['POLICY_CPCONFIG'])
