from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ripozo.exceptions import RestException


class MethodNotAllowed(RestException):
    """
    Raised when an unavailable http
    verb is used.
    """
    def __init__(self, message=None, status_code=405):
        super(MethodNotAllowed, self).__init__(message=message, status_code=status_code)

