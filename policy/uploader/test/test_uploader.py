#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the uploader with httpretty."""
from unittest import TestCase
from json import dumps
import httpretty
from policy.uploader.rest import UploaderPolicy
from policy.globals import METADATA_ENDPOINT


class TestUploader(TestCase):
    """Test the uploader policy with httpretty."""

    sample_user_id = 23
    admin_user_id = 45
    admin_group_id = 127
    user_group_json = [
        {
            'group_id': admin_group_id,
            'person_id': admin_user_id
        }
    ]
    admin_group_json = [
        {
            '_id': admin_group_id
        }
    ]
    group_url = '{0}/groups'.format(METADATA_ENDPOINT)
    user_group_url = '{0}/user_group'.format(METADATA_ENDPOINT)

    @httpretty.activate
    def test_failed_admin_id(self):
        """check failed admin id fallback works."""
        httpretty.register_uri(httpretty.GET, self.group_url,
                               body=dumps([]),
                               content_type='application/json')
        httpretty.register_uri(httpretty.GET, self.user_group_url,
                               body=dumps([]),
                               content_type='application/json')
        upolicy = UploaderPolicy()
        # pylint: disable=no-member
        # pylint: disable=protected-access
        ret = upolicy._is_admin(10)
        # pylint: enable=protected-access
        # pylint: enable=no-member
        self.assertFalse(ret)
