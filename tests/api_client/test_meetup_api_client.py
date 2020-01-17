import pytest
from meetup_search.meetup_api_client.meetup_api_client import (
    RateLimit,
    MeetupApiClient,
)
from meetup_search.meetup_api_client.exceptions import (
    GroupDoesNotExists,
    GroupDoesNotExistsOnMeetup,
    HttpNoSuccess,
    HttpNoXRateLimitHeader,
    HttpNotAccessibleError,
    HttpNotFoundError,
    MeetupConnectionError,
)
import time
import requests
import requests_mock
from pytest_httpserver import HTTPServer
from meetup_search.models.group import Group, Event
from time import sleep
from typing import List
from conftest import create_group


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
    rate_limit_fake: RateLimit = RateLimit()
    with pytest.raises(HttpNoXRateLimitHeader):
        rate_limit_fake.update_rate_limit(response=response, reset_time=2)

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


def test_get(httpserver: HTTPServer, meetup_groups: dict):
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


def test_get_group(httpserver: HTTPServer, meetup_groups: dict):
    # init api client
    api_client: MeetupApiClient = MeetupApiClient()

    # check existing group
    group_1: Group = api_client.get_group(
        group_urlname=meetup_groups["sandbox"]["urlname"]
    )
    assert isinstance(group_1, Group)
    assert group_1.meetup_id == meetup_groups["sandbox"]["meetup_id"]

    # check not existing group
    with pytest.raises(GroupDoesNotExistsOnMeetup):
        api_client.get_group(group_urlname=meetup_groups["not-exist"]["urlname"])

    # create gone group object in elasticsearch
    group_2 = create_group(urlname=meetup_groups["gone"]["urlname"])
    group_2.save()
    sleep(1)

    # check gone group
    with pytest.raises(GroupDoesNotExistsOnMeetup):
        api_client.get_group(group_urlname=meetup_groups["gone"]["urlname"])
    sleep(1)

    # check if gone group was deleted
    with pytest.raises(GroupDoesNotExists):
        Group.get_group(urlname=meetup_groups["gone"]["urlname"])

    # create gone group object in elasticsearch
    group_2 = create_group(urlname=meetup_groups["gone"]["urlname"])
    group_2.save()
    sleep(1)

    # test for HttpNoXRateLimitHeader execption
    for _ in range(4):
        httpserver.expect_oneshot_request("/HttpNoXRateLimitHeader").respond_with_data(
            "OK"
        )
    api_client.base_url = httpserver.url_for("/HttpNoXRateLimitHeader")
    with pytest.raises(MeetupConnectionError):
        api_client.get_group(group_urlname=meetup_groups["gone"]["urlname"])

    # check if gone group was not deleted
    assert Group.get_group(urlname=meetup_groups["gone"]["urlname"]) is not None

    # test for HttpNoSuccess execption
    for _ in range(4):
        httpserver.expect_oneshot_request("/HttpNoSuccess")
    api_client.base_url = httpserver.url_for("")
    with pytest.raises(MeetupConnectionError):
        api_client.get_group(group_urlname=meetup_groups["gone"]["urlname"])

    # check if gone group was not deleted
    assert Group.get_group(urlname=meetup_groups["gone"]["urlname"]) is not None


def test_update_group_events(meetup_groups: dict):
    # init api client
    api_client: MeetupApiClient = MeetupApiClient()

    # get sandbox group
    group_1: Group = api_client.get_group(
        group_urlname=meetup_groups["sandbox"]["urlname"]
    )

    # get events when group has no event
    events_1: List[Event] = api_client.update_group_events(
        group=group_1, max_entries=10
    )
    assert isinstance(events_1[0], Event)
    assert len(events_1) == 10

    # save events into group
    group_1.add_events(events=events_1)
    group_1.save()
    sleep(1)

    # check if there was no double request
    events_2: List[Event] = api_client.update_group_events(
        group=group_1, max_entries=10
    )
    assert isinstance(events_1[0], Event)
    assert len(events_1) == 10
    for event_1 in events_1:
        for event_2 in events_2:
            assert event_1.meetup_id != event_2.meetup_id

    # check for min max_entries
    events_3: List[Event] = api_client.update_group_events(
        group=group_1, max_entries=-10
    )
    assert isinstance(events_3[0], Event)
    assert len(events_3) == 1

    # check for max max_entries
    events_4: List[Event] = api_client.update_group_events(
        group=group_1, max_entries=1000
    )
    assert isinstance(events_3[0], Event)
    assert len(events_4) == 200


def test_update_all_group_events(meetup_groups: dict):
    # init api client
    api_client: MeetupApiClient = MeetupApiClient()

    # get sandbox group
    group_1: Group = api_client.get_group(
        group_urlname=meetup_groups["sandbox"]["urlname"]
    )

    # get all events
    events_1: List[Event] = api_client.update_all_group_events(group=group_1)
    assert isinstance(events_1[0], Event)
    assert len(events_1) > 200

    # load all events from elasticseach
    group_2: Group = api_client.get_group(
        group_urlname=meetup_groups["sandbox"]["urlname"]
    )

    # check if all events was saved into elasticsearch
    assert len(events_1) == len(group_2.events)

    # check if there still some events
    events_3: List[Event] = api_client.update_all_group_events(group=group_2)
    assert len(events_3) == 0


def test_get_max_entries():
    # test min value
    assert MeetupApiClient.get_max_entries(max_entries=-1) == 1

    # test max value
    assert MeetupApiClient.get_max_entries(max_entries=100) == 100

    # test valid value
    assert MeetupApiClient.get_max_entries(max_entries=1000) == 200


def test_get_zip_from_meetup():
    # init api client
    api_client: MeetupApiClient = MeetupApiClient()

    # get zip codes
    zip_code_list: List[str] = api_client.get_zip_from_meetup(lat=52.1, lon=13.1)

    assert len(zip_code_list) > 0
    for zip_code in zip_code_list:
        assert isinstance(zip_code, str)


def test_get_all_zip_from_meetup():
    # init api client
    api_client: MeetupApiClient = MeetupApiClient()

    # get all zip codes from Switzerland
    zip_code_list: List[str] = api_client.get_all_zip_from_meetup(
        min_lat=47.270114,
        max_lat=55.099161,
        min_lon=5.8663153,
        max_lon=15.0418087
    )

    assert len(zip_code_list) > 10000
    for zip_code in zip_code_list:
        assert isinstance(zip_code, str)
