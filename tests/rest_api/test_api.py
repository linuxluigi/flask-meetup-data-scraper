import pytest
from flask.testing import FlaskClient
from meetup_search.models import Group, Event
from flask.helpers import url_for
from requests import put, get
from pytest_flask.plugin import JSONResponse
from typing import List, Dict
from .utily import create_groups, generate_search_dict, create_events_to_group
from time import sleep


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
    assert response_1.json == {"results": [], "hits": 0}
    assert isinstance(response_1, JSONResponse)

    # generate match group
    groups_1: List[Group] = create_groups(search_query="v", valid_groups=True, amount=1)

    # test with a single match group
    response_2: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="v")
    )
    assert response_2.status_code == 200
    assert response_2.json["results"][0]["name"] == groups_1[0].name
    assert len(response_2.json["results"]) == 1
    assert response_2.json["hits"] == 1
    assert isinstance(response_2, JSONResponse)

    # generate many valid groups
    create_groups(search_query="vu", valid_groups=True, amount=100)

    # test with a many match group
    response_3: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="vu")
    )
    assert response_3.status_code == 200
    assert len(response_3.json["results"]) == 25
    assert response_3.json["hits"] == 100
    assert isinstance(response_3, JSONResponse)

    # generate many invalid groups
    create_groups(search_query="vu", valid_groups=False, amount=100)

    # test with a many unmatch groups
    response_4: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="vu")
    )
    assert response_4.status_code == 200
    assert len(response_4.json["results"]) == 25
    assert response_4.json["hits"] == 100
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


def test_suggest(client: FlaskClient):
    # test with no groups
    response_1: JSONResponse = client.get(url_for("meetupsearchsuggestapi", query="v"))
    assert response_1.status_code == 200
    assert response_1.json == {"suggestions": []}

    # add one group
    groups_1: List[Group] = create_groups(
        search_query="vuu", valid_groups=True, amount=1
    )

    # test with one groups
    response_2: JSONResponse = client.get(url_for("meetupsearchsuggestapi", query="v"))
    assert response_2.status_code == 200
    assert response_2.json["suggestions"][0] == groups_1[0].name
    assert len(response_2.json["suggestions"]) == 1

    groups_2: List[Group] = create_groups(
        search_query="vuu", valid_groups=False, amount=20
    )

    # test with many groups
    response_3: JSONResponse = client.get(url_for("meetupsearchsuggestapi", query="vu"))
    assert response_3.status_code == 200
    assert response_3.json["suggestions"][0] == groups_1[0].name
    assert len(response_3.json["suggestions"]) == 1

    # add groups wich should been suggest
    create_groups(search_query="vuu", valid_groups=True, amount=20)

    # test with many groups return max 5 suggestions
    response_4: JSONResponse = client.get(url_for("meetupsearchsuggestapi", query="vu"))
    assert response_4.status_code == 200
    assert len(response_4.json["suggestions"]) == 5
