from flask.testing import FlaskClient
from meetup_search.models.group import Group, Event
from flask.helpers import url_for
from pytest_flask.plugin import JSONResponse
from typing import List
from .utily import create_groups, generate_search_dict, create_events_to_group
from time import sleep
from _datetime import datetime


def test_search_query(client: FlaskClient):
    """
    teste search api for query

    Arguments:
        client {FlaskClient} -- client to access flask web ressource
    """
    # test with no groups
    response_1: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="v")
    )
    assert response_1.status_code == 200
    assert response_1.json == {"results": [], "hits": 0, "map_center": {"lat": 0, "lon": 0}}
    assert isinstance(response_1, JSONResponse)

    # generate match group
    groups_1: List[Group] = create_groups(search_query="v", valid_groups=True, amount=1)

    # test with a single match group
    response_2: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="*v*")
    )
    assert response_2.status_code == 200
    assert response_2.json["results"][0]["name"] == groups_1[0].name
    assert len(response_2.json["results"]) == 1
    assert response_2.json["hits"] == 1
    assert isinstance(response_2, JSONResponse)

    # generate many valid groups
    create_groups(search_query="vu", valid_groups=True, amount=50)

    # test with a many match group
    response_3: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="vu", limit=25)
    )
    assert response_3.status_code == 200
    assert len(response_3.json["results"]) == 25
    assert response_3.json["hits"] == 50
    assert isinstance(response_3, JSONResponse)

    # generate many invalid groups
    create_groups(search_query="vu", valid_groups=False, amount=50)

    # test with a many unmatch groups
    response_4: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="vu", limit=25)
    )
    assert response_4.status_code == 200
    assert len(response_4.json["results"]) == 25
    assert response_4.json["hits"] == 50
    assert isinstance(response_4, JSONResponse)

    # test with missing query
    response_5: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict()
    )
    assert response_5.status_code == 400
    assert isinstance(response_5.json["message"]["query"], str)
    assert isinstance(response_5, JSONResponse)

    # test with empty query
    response_6: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="")
    )
    assert response_6.status_code == 400
    assert isinstance(response_6.json["message"]["query"], str)
    assert isinstance(response_6, JSONResponse)


def test_map_center(client: FlaskClient):
    """
    test if venues output was set right

    Arguments:
        client {FlaskClient} -- client to access flask web ressource
    """

    # test with no groups
    response_1: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="v")
    )
    assert response_1.status_code == 200
    assert response_1.json == {"results": [], "hits": 0, "map_center": {"lat": 0, "lon": 0}}
    assert isinstance(response_1, JSONResponse)

    # add one group
    groups_1: List[Group] = create_groups(
        search_query="v", valid_groups=True, amount=1
    )

    # test with one group
    response_2: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="v")
    )
    assert response_2.status_code == 200
    assert response_2.json['map_center'] == {"lat": 1, "lon": 1}
    assert isinstance(response_2, JSONResponse)

    # create a event with venue to a group
    create_events_to_group(
        search_query="b", valid_events=True, group=groups_1[0], amount=10, venue=True
    )

    # test with one group with mutiple events
    response_3: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="v")
    )
    assert response_3.status_code == 200
    assert response_3.json['map_center'] == {"lat": 5.5, "lon": 5.5}
    assert isinstance(response_3, JSONResponse)

    # add one more group with mutiple events
    groups_2: List[Group] = create_groups(
        search_query="v", valid_groups=True, amount=1
    )
    create_events_to_group(
        search_query="b", valid_events=True, group=groups_2[0], amount=9, venue=True
    )

    # test with two groups with mutiple events
    response_4: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="v")
    )
    assert response_4.status_code == 200
    assert response_4.json['map_center'] == {"lat": 5.25, "lon": 5.25}
    assert isinstance(response_4, JSONResponse)


def test_group_venues(client: FlaskClient):
    """
    check if group venues was set right

    Arguments:
        client {FlaskClient} -- client to access flask web ressource
    """
    # add one group without event
    groups_1: List[Group] = create_groups(
        search_query="v", valid_groups=True, amount=1
    )

    # test with one group without events
    response_1: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="v")
    )
    assert response_1.status_code == 200
    assert len(response_1.json['results'][0]['venues']) == 0
    assert isinstance(response_1, JSONResponse)

    # add mutile events without venue
    create_events_to_group(
        search_query="b", valid_events=True, group=groups_1[0], amount=10, venue=False
    )

    # test with one group with events without venues
    response_2: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="v")
    )
    assert response_2.status_code == 200
    assert len(response_2.json['results'][0]['venues']) == 0
    assert isinstance(response_2, JSONResponse)

    # add mutile events with venues
    create_events_to_group(
        search_query="b", valid_events=True, group=groups_1[0], amount=10, venue=True
    )

    # test with one group with events with venues
    response_3: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="v")
    )
    assert response_3.status_code == 200
    assert len(response_3.json['results'][0]['venues']) == 10
    assert isinstance(response_3, JSONResponse)


def test_search_filter(client: FlaskClient, group_1: Group):
    """
    Test filter param on search request

    Arguments:
        client {FlaskClient} -- client to access flask web ressource
    """
    group_1.save()
    sleep(1)

    # test with a single match group
    response_1: JSONResponse = client.put(
        url_for("meetupsearchapi"),
        data=generate_search_dict(
            query=str(group_1.meetup_id), query_fields=["meetup_id"]
        ),
    )
    assert response_1.status_code == 200
    assert response_1.json["results"][0]["urlname"] == group_1.urlname
    assert len(response_1.json["results"]) == 1
    assert response_1.json["hits"] == 1
    assert isinstance(response_1, JSONResponse)

    # test unmatching query
    response_2: JSONResponse = client.put(
        url_for("meetupsearchapi"),
        data=generate_search_dict(
            query=str(group_1.meetup_id), query_fields=["urlname"]
        ),
    )
    assert response_2.status_code == 200
    assert len(response_2.json["results"]) == 0
    assert response_2.json["hits"] == 0
    assert isinstance(response_2, JSONResponse)


def test_search_pagination(client: FlaskClient):
    """
    Test pagination param on search request

    Arguments:
        client {FlaskClient} -- client to access flask web ressource
    """
    # generate may matching groups
    groups_1: List[Group] = create_groups(
        search_query="v", valid_groups=True, amount=50
    )

    # test page 0 with 25 entries
    response_1: JSONResponse = client.put(
        url_for("meetupsearchapi"),
        data=generate_search_dict(query="v", page=0, limit=25),
    )
    assert response_1.status_code == 200
    assert response_1.json["results"][0]["urlname"] == groups_1[0].urlname
    assert len(response_1.json["results"]) == 25
    assert response_1.json["hits"] == 50
    assert isinstance(response_1, JSONResponse)

    # test page 1 with 25 entries
    response_2: JSONResponse = client.put(
        url_for("meetupsearchapi"),
        data=generate_search_dict(query="v", page=1, limit=25),
    )
    assert response_2.status_code == 200
    assert response_2.json["results"][0]["urlname"] == groups_1[25].urlname
    assert len(response_2.json["results"]) == 25
    assert response_2.json["hits"] == 50
    assert isinstance(response_2, JSONResponse)


def test_search_query_event(client: FlaskClient):
    """
    Test if events will use for a search request

    Arguments:
        client {FlaskClient} -- client to access flask web ressource
    """

    search_query: str = "123456789qwert"

    # generate single unmacht group
    groups_1: List[Group] = create_groups(
        search_query=search_query, valid_groups=False, amount=1
    )

    # test with no event
    response_2: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query=search_query)
    )
    assert response_2.status_code == 200
    assert len(response_2.json["results"]) == 0
    assert response_2.json["hits"] == 0
    assert isinstance(response_2, JSONResponse)

    # add event to unmacht group
    create_events_to_group(
        search_query=search_query, valid_events=True, group=groups_1[0], amount=20
    )

    # test with a single match event
    response_3: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query=search_query)
    )
    assert response_3.status_code == 200
    assert response_3.json["results"][0]["name"] == groups_1[0].name
    assert len(response_3.json["results"]) == 1
    assert response_3.json["hits"] == 1
    assert isinstance(response_3, JSONResponse)

    # generate mutiple unmatching groups with events
    groups_2: List[Group] = create_groups(
        search_query=search_query, valid_groups=False, amount=5
    )
    for group in groups_2:
        create_events_to_group(
            search_query=search_query, valid_events=False, group=group, amount=20
        )

    # test with a single match event and many unmachting events

    response_4: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query=search_query)
    )
    assert response_4.status_code == 200
    assert response_4.json["results"][0]["name"] == groups_1[0].name
    assert len(response_4.json["results"]) == 1
    assert response_4.json["hits"] == 1
    assert isinstance(response_4, JSONResponse)

    # add new matching group with many matching events
    groups_3: List[Group] = create_groups(
        search_query=search_query, valid_groups=False, amount=1
    )
    # add events to unmacht group
    create_events_to_group(
        search_query=search_query, valid_events=True, group=groups_3[0], amount=5
    )

    # test with 2 matching groups
    response_5: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query=search_query)
    )
    assert response_5.status_code == 200
    assert len(response_5.json["results"]) == 2
    assert response_5.json["hits"] == 2
    assert isinstance(response_5, JSONResponse)


def test_search_sort(client: FlaskClient):
    """
    Test sort

    Arguments:
        client {FlaskClient} -- client to access flask web ressource
    """
    # generate mutiple matching groups
    create_groups(
        search_query="v", valid_groups=True, amount=10
    )
    sleep(2)

    # test sort by meetup_id
    response_1: JSONResponse = client.put(
        url_for("meetupsearchapi"),
        data=generate_search_dict(query="v", sort="meetup_id"),
    )
    assert response_1.status_code == 200
    assert len(response_1.json["results"]) == 10
    assert response_1.json["hits"] == 10
    assert isinstance(response_1, JSONResponse)

    for i in range(0, 9):
        assert response_1.json["results"][i]["meetup_id"] == i

    # test sort by -meetup_id
    response_2: JSONResponse = client.put(
        url_for("meetupsearchapi"),
        data=generate_search_dict(query="*", sort="-meetup_id"),
    )
    assert response_2.status_code == 200
    assert len(response_2.json["results"]) == 10
    assert response_2.json["hits"] == 10
    assert isinstance(response_1, JSONResponse)

    for i in range(9, 0, -1):
        assert response_1.json["results"][i]["meetup_id"] == i


def test_search_load_events(client: FlaskClient):
    """
    Test load_events

    Arguments:
        client {FlaskClient} -- client to access flask web ressource
    """
    search_query: str = "v"

    # generate match group with 5 events
    groups_1: List[Group] = create_groups(search_query=search_query, valid_groups=True, amount=1)
    create_events_to_group(
        search_query=search_query, valid_events=True, group=groups_1[0], amount=5
    )

    # test with load events
    response_1: JSONResponse = client.put(
        url_for("meetupsearchapi"),
        data=generate_search_dict(query=search_query, load_events=True),
    )
    assert response_1.status_code == 200
    assert len(response_1.json["results"]) == 1
    assert len(response_1.json["results"][0]['events']) == 5
    assert response_1.json["hits"] == 1
    assert isinstance(response_1, JSONResponse)

    # test without load events
    response_2: JSONResponse = client.put(
        url_for("meetupsearchapi"),
        data=generate_search_dict(query=search_query, load_events=False),
    )
    assert response_2.status_code == 200
    assert len(response_2.json["results"]) == 1
    assert len(response_2.json["results"][0]['events']) == 0
    assert response_2.json["hits"] == 1
    assert isinstance(response_2, JSONResponse)


def test_search_geo_distance(client: FlaskClient, group_1: Group):
    """
    Test geo_distance filter

    Arguments:
        client {FlaskClient} -- client to access flask web ressource
    """
    # init group with no location
    group_1.save()
    sleep(1)

    # test no location in groups, search for potsdam
    response_1: JSONResponse = client.put(
        url_for("meetupsearchapi"),
        data=generate_search_dict(
            query="*", geo_distance="100km", geo_lat=52.396149, geo_lon=13.058540
        ),
    )
    assert response_1.status_code == 200
    assert len(response_1.json["results"]) == 0
    assert response_1.json["hits"] == 0
    assert isinstance(response_1, JSONResponse)

    # add berlin as location for group
    event_berlin: Event = Event(
        meetup_id="berlin",
        time=datetime.now(),
        name="berlin",
        link="http://none",
        date_in_series_pattern=False,
        venue_name="Café",
        venue_location={"lat": 52.520008, "lon": 13.404954}
    )
    group_1.add_event(event=event_berlin)
    group_1.save()
    sleep(1)

    # check if potsdam is in 100km from berlin center
    response_2: JSONResponse = client.put(
        url_for("meetupsearchapi"),
        data=generate_search_dict(
            query="*", geo_distance="100km", geo_lat=52.396149, geo_lon=13.058540
        ),
    )
    assert response_2.status_code == 200
    assert len(response_2.json["results"]) == 1
    assert response_2.json["hits"] == 1
    assert isinstance(response_2, JSONResponse)

    # check if potsdam is in 1km from berlin center
    response_3: JSONResponse = client.put(
        url_for("meetupsearchapi"),
        data=generate_search_dict(
            query="*", geo_distance="0.5km", geo_lat=52.396149, geo_lon=13.058540
        ),
    )
    assert response_3.status_code == 200
    assert len(response_3.json["results"]) == 0
    assert response_3.json["hits"] == 0
    assert isinstance(response_3, JSONResponse)


def test_suggest(client: FlaskClient):
    # test with no groups
    response_1: JSONResponse = client.put(
        url_for("meetupsearchsuggestapi"),
        data=generate_search_dict(query="v"),
    )
    assert response_1.status_code == 200
    assert response_1.json == {"suggestions": []}

    # add one group
    groups_1: List[Group] = create_groups(
        search_query="vuu", valid_groups=True, amount=1
    )

    # test with one groups
    response_2: JSONResponse = client.put(
        url_for("meetupsearchsuggestapi"),
        data=generate_search_dict(query="v"),
    )
    assert response_2.status_code == 200
    assert response_2.json["suggestions"][0] in groups_1[0].name
    assert len(response_2.json["suggestions"]) == 1

    create_groups(search_query="vuu", valid_groups=False, amount=20)

    # test with many groups
    response_3: JSONResponse = client.put(
        url_for("meetupsearchsuggestapi"),
        data=generate_search_dict(query="vu"),
    )
    assert response_3.status_code == 200
    assert response_3.json["suggestions"][0] in groups_1[0].name
    assert len(response_3.json["suggestions"]) == 1

    # add groups wich should been suggest
    create_groups(search_query="vuu", valid_groups=True, amount=20)

    # test with many groups return max 5 suggestions
    response_4: JSONResponse = client.put(
        url_for("meetupsearchsuggestapi"),
        data=generate_search_dict(query="vu"),
    )
    assert response_4.status_code == 200
    assert len(response_4.json["suggestions"]) == 5
