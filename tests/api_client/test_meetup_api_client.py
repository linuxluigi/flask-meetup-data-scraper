import pytest
from meetup_search.meetup_api_client.meetup_api_client import (
    RateLimit,
    MeetupApiClient,
)
from meetup_search.meetup_api_client.exceptions import (
    GroupDoesNotExists,
    HttpNoSuccess,
    HttpNoXRateLimitHeader,
    HttpNotAccessibleError,
    HttpNotFoundError,
)
import time
import requests
import requests_mock
from pytest_httpserver import HTTPServer
from meetup_search.models import Group, Event
from tests.meetup_api_demo_response import get_group_response
from datetime import datetime
from time import sleep


meetup_groups: dict = {
    "sandbox": {"meetup_id": 1556336, "urlname": "Meetup-API-Testing"},
    "not-exist": {"meetup_id": 123456, "urlname": "None"},
    "gone": {"meetup_id": 654321, "urlname": "connectedawareness-berlin"},
}


def test_wait_for_next_request():
    # setup RateLimit
    rate_limit: RateLimit = RateLimit()
    timestamp: float = time.time()
    rate_limit.reset_time = timestamp + 2

    # wait
    rate_limit.wait_for_next_request()

    # assert
    assert time.time() >= rate_limit.reset_time


def test_update_rate_limit():
    # set start timestamp
    timestamp: float = time.time()

    # setup fake http request
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount("mock", adapter)

    adapter.register_uri("GET", "mock://test.com", text="data")
    response = session.get("mock://test.com")

    # use fake response without RateLimit headers
    rate_limit: RateLimit = RateLimit()
    with pytest.raises(HttpNoXRateLimitHeader):
        rate_limit.update_rate_limit(response=response, reset_time=2)

    # set fake response
    default_header_value = 30
    response.headers["X-RateLimit-Limit"] = str(default_header_value)
    response.headers["X-RateLimit-Remaining"] = str(default_header_value)
    response.headers["X-RateLimit-Reset"] = str(default_header_value)

    rate_limit: RateLimit = RateLimit()
    rate_limit.update_rate_limit(response=response, reset_time=2)

    # assert
    assert rate_limit.limit == default_header_value
    assert rate_limit.remaining == default_header_value
    assert rate_limit.reset == default_header_value
    assert rate_limit.reset_time >= timestamp + default_header_value
    assert rate_limit.reset_time <= time.time() + default_header_value


def test_get(httpserver: HTTPServer):
    api_client: MeetupApiClient = MeetupApiClient()

    with pytest.raises(HttpNotFoundError):
        api_client.get(meetup_groups["not-exist"]["urlname"])

    with pytest.raises(HttpNotAccessibleError):
        api_client.get(meetup_groups["gone"]["urlname"])

    json: dict = api_client.get(meetup_groups["sandbox"]["urlname"])
    assert isinstance(json, dict)
    assert json["id"] == meetup_groups["sandbox"]["meetup_id"]

    # test for HttpNoXRateLimitHeader execption
    for _ in range(4):
        httpserver.expect_oneshot_request("/HttpNoXRateLimitHeader").respond_with_data(
            "OK"
        )
    api_client.base_url = httpserver.url_for("/HttpNoXRateLimitHeader")
    with pytest.raises(HttpNoXRateLimitHeader):
        api_client.get(url_path="", reset_time=2)

    # test for HttpNoSuccess execption
    for _ in range(4):
        httpserver.expect_oneshot_request("/HttpNoSuccess")
    api_client.base_url = httpserver.url_for("")
    with pytest.raises(HttpNoSuccess):
        api_client.get(url_path="/", reset_time=2)


def test_get_group(httpserver: HTTPServer):
    # init api client
    api_client: MeetupApiClient = MeetupApiClient()

    # check existing group
    group_1: Group = api_client.get_group(
        group_urlname=meetup_groups["sandbox"]["urlname"]
    )
    assert isinstance(group_1, Group)
    assert group_1.meetup_id == meetup_groups["sandbox"]["meetup_id"]

    # check not existing group
    group_2: Group = api_client.get_group(
        group_urlname=meetup_groups["not-exist"]["urlname"]
    )
    assert group_2 is None

    # create gone group object in elasticsearch
    group_3 = Group(
        meetup_id=20,
        urlname=meetup_groups["gone"]["urlname"],
        created=datetime.now(),
        description="",
        name="",
        link="",
        location=[0, 0],
        members=0,
        status="",
        timezone="",
        visibility="",
    )
    group_3.save()
    sleep(1)

    # check gone group
    group_4: Group = api_client.get_group(
        group_urlname=meetup_groups["gone"]["urlname"]
    )
    sleep(1)
    assert group_4 is None

    # check if gone group was deleted
    assert Group.get_group(urlname=meetup_groups["gone"]["urlname"]) == None


def test_update_group_events():
    # init api client
    api_client: MeetupApiClient = MeetupApiClient()

    # get sandbox group
    group_1: Group = api_client.get_group(
        group_urlname=meetup_groups["sandbox"]["urlname"]
    )

    group_2: Group = api_client.get_group(
        group_urlname=meetup_groups["not-exist"]["urlname"]
    )

    # get events when group has no event
    events_1: [event] = api_client.update_group_events(group=group_1, max_entries=10)
    assert isinstance(events_1[0], Event)
    assert len(events_1) == 10

    # save events into group
    group_1.add_events(events=events_1)
    group_1.save()
    sleep(1)

    # check if there was no double request
    events_2: [event] = api_client.update_group_events(group=group_1, max_entries=10)
    assert isinstance(events_1[0], Event)
    assert len(events_1) == 10
    for event_1 in events_1:
        for event_2 in events_2:
            assert event_1.meetup_id != event_2.meetup_id

    # check for min max_entries
    events_3: [event] = api_client.update_group_events(group=group_1, max_entries=-10)
    assert isinstance(events_3[0], Event)
    assert len(events_3) == 1

    # check for max max_entries
    events_4: [event] = api_client.update_group_events(group=group_1, max_entries=1000)
    assert isinstance(events_3[0], Event)
    assert len(events_4) == 200

    # get events when group does not exists
    with pytest.raises(GroupDoesNotExists):
        api_client.update_group_events(group=group_2, max_entries=10)


def test_update_all_group_events():
    # init api client
    api_client: MeetupApiClient = MeetupApiClient()

    # get sandbox group
    group_1: Group = api_client.get_group(
        group_urlname=meetup_groups["sandbox"]["urlname"]
    )

    # get all events
    events_1: [event] = api_client.update_all_group_events(group=group_1)
    assert isinstance(events_1[0], Event)
    assert len(events_1) > 200

    # load all events from elasticseach
    group_2: Group = api_client.get_group(
        group_urlname=meetup_groups["sandbox"]["urlname"]
    )

    # check if all events was saved into elasticsearch
    assert len(events_1) == len(group_2.events)

    # check if there still some events
    events_3: [event] = api_client.update_all_group_events(group=group_2)
    assert len(events_3) == 0


def test_get_max_entries():
    # init api client
    api_client: MeetupApiClient = MeetupApiClient()

    # test min value
    assert api_client.get_max_entries(max_entries=-1) == 1

    # test max value
    assert api_client.get_max_entries(max_entries=100) == 100

    # test valid value
    assert api_client.get_max_entries(max_entries=1000) == 200
