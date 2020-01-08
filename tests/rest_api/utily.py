import pytest
from flask.testing import FlaskClient
from meetup_search.models import Group, Event
from flask.helpers import url_for
from requests import put, get
from pytest_flask.plugin import JSONResponse
from time import sleep
from typing import List, Dict, Optional
from conftest import create_group
import random
import string
from datetime import datetime


def generate_search_dict(
    query: Optional[str] = None,
    query_fields: Optional[List[str]] = None,
    filters: Optional[dict] = None,
    exclude: Optional[List[str]] = None,
    page: Optional[int] = None,
    limit: Optional[int] = None,
    sort: Optional[List[dict]] = None,
) -> dict:
    """
    Generate a search query object for testing

    Keyword Arguments:
        query {Optional[str]} -- search query (default: {None})
        query_fields {Optional[List[str]]} -- search query_fields (default: {None})
        filters {Optional[dict]} -- search filter (default: {None})
        exclude {Optional[List[str]]} -- exclude fields from search (default: {None})
        page {Optional[int]} -- pagination page (default: {None})
        limit {Optional[int]} -- pagination entry limits per page (default: {None})
        sort {Optional[List[dict]]} -- search dict (default: {None})

    Returns:
        dict -- search object dict for testing
    """

    search_dict: dict = {}
    if query:
        search_dict["query"] = query
    if query_fields:
        search_dict["query_fields"] = query_fields
    if filters:
        search_dict["filter"] = filters
    if exclude:
        search_dict["exclude"] = exclude
    if page:
        search_dict["page"] = page
    if limit:
        search_dict["limit"] = limit
    if sort:
        search_dict["sort"] = sort

    return search_dict


def randomString(search_query: str, valid: bool, stringLength: int = 10) -> str:
    """
    Generate a random string of fixed length

    Keyword Arguments:
        search_query {str} -- use query param for the search request
        valid {bool} -- should searchable by the the query term
        stringLength {int} -- size of random string (default: {10})

    Returns:
        str -- random string
    """
    letters = string.ascii_lowercase

    if valid:
        return "{} {}".format(
            search_query, "".join(random.choice(letters) for i in range(stringLength)),
        )

    while True:
        random_string: str = "".join(
            random.choice(letters) for i in range(stringLength)
        )
        if not search_query in random_string:
            return random_string


def create_events_to_group(
    search_query: str, valid_events: bool, group: Group, amount: int = 1
) -> List[Event]:
    """
    Create random test events and save them to a group

    Arguments:
        search_query {str} -- use query param for the search request
        valid_events {bool} -- should the groups searchable by the the query term
        group {Group} -- group to at the events

    Keyword Arguments:
        amount {int} -- how many events should be created (default: {1})

    Returns:
        List[Event] -- created & saved events
    """

    created_events: List[Event] = []

    for _ in range(0, amount):
        event_name: str = randomString(search_query=search_query, valid=valid_events)
        created_events.append(
            Event(
                meetup_id=event_name,
                time=datetime.now(),
                name=event_name,
                link="http://none",
                date_in_series_pattern=False,
            )
        )

    group.add_events(events=created_events)
    group.save()
    sleep(1)

    return created_events


def create_groups(
    search_query: str, valid_groups: bool, amount: int = 1
) -> List[Group]:
    """
    Create random test groups and save them

    Arguments:
        search_query {str} -- use query param for the search request
        valid_groups {bool} -- should the groups searchable by the the query term

    Keyword Arguments:
        amount {int} -- [description] (default: {1})

    Returns:
        List[Group] -- created groups
    """

    created_groups: List[Group] = []

    for _ in range(0, amount):
        group_name: str = randomString(search_query=search_query, valid=valid_groups)
        created_group: Group = create_group(urlname=group_name, name=group_name)
        created_group.save()
        created_groups.append(created_group)

    sleep(1)

    return created_groups
