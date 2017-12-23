#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy Status Metadata object class."""
import requests
from cherrypy import tools, request
from policy.validation import validate_user
from policy.globals import METADATA_ENDPOINT
from policy.reporting.transaction.query_base import QueryBase


# pylint: disable=too-few-public-methods
class TransactionDetails(QueryBase):
    """Retrieves a list of all transactions matching the search criteria."""

    exposed = True

    @staticmethod
    def _get_transaction_list_details(transaction_list, user_id):
        header_list = {'Content-Type': 'application/json'}
        req = requests.post(
            url='{0}/summaryinfo/transaction_details'.format(
                METADATA_ENDPOINT),
            json=transaction_list,
            headers=header_list
        )

        user_info = QueryBase._merge_two_dicts(
            QueryBase.base_user_info,
            QueryBase.get_full_user_info(user_id)
        )

        results = {}
        req_json = req.json()
        for transaction_id in req_json.keys():
            info = req_json[transaction_id]
            if user_info['emsl_employee'] or (
                    info['proposal_id'] in user_info['proposal_list'] and
                    info['instrument_id'] in user_info['instrument_list']
            ):
                results[transaction_id] = info
        return results

    # CherryPy requires these named methods
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_in()
    @tools.json_out()
    @validate_user()
    def POST(user_id=None):
        """CherryPy GET method."""
        return TransactionDetails._get_transaction_list_details(request.json, user_id)
# pylint: enable=too-few-public-methods
