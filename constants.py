"""
Created common String constants by the use of named tuple"""

from collections import namedtuple

GeneralMessages = namedtuple(
    "GeneralMessages",
    ["start_message", "access_forbidden", "internal_server_error", "access_token"],
)


GENERAL = GeneralMessages(
    start_message="API is working! Go to /docs for Swagger.",
    access_forbidden="You do not have permission to perform this action",
    internal_server_error="An unexpected error occurred",
    access_token="access_token",
)

