#!/usr/bin/python
"""CherryPy Status Policy object class."""
from policy.status.user.search import UserSearch
from policy.status.user.lookup import UserLookup


# pylint: disable=too-few-public-methods
class UserQuery(object):
    """CherryPy root object class."""

    exposed = True

    def __init__(self):
        """Create local objects for sub tree items."""
        self.search = UserSearch()
        self.by_id = UserLookup()
# pylint: enable=too-few-public-methods
