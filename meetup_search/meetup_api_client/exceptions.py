class HttpNoSuccess(Exception):
    """
    Called when the server sends not 200, 404 or 410.
    """


class HttpNotFoundError(Exception):
    """
    Called when the server sends a 404 error.
    """


class HttpNotAccessibleError(Exception):
    """
    Called when the server sends a 410 error.
    """


class HttpNoXRateLimitHeader(Exception):
    """
    Called when a response has no X-RateLimit header
    """


class EventAlreadyExists(Exception):
    """
    Event already exists in Elasticsearch
    """


class GroupDoesNotExists(Exception):
    """
    Called when try to access a group witch not exists
    """


class GroupDoesNotExistsOnMeetup(Exception):
    """
    Meetup group does not exists (anymore) on meetup.com
    """


class MeetupConnectionError(Exception):
    """
    There is some problem to make a meetup api request
    """


class InvalidResponse(Exception):
    """
    Response has a invalid value
    """
