import pytest
from meetup_search.models import Group, Event
from time import sleep
from app import create_app
from flask.app import Flask
from datetime import datetime


@pytest.fixture
def app() -> Flask:
    """
    flask app fixture for texting

    Returns:
        Flask -- flask app with testing config
    """
    return create_app(config_path="/app/config/test.py")


@pytest.fixture
def meetup_groups() -> dict:
    """
    test groups with id & real meetup group urlname

    Returns:
        dict -- dict with mutiple meetup groups
    """
    return {
        "sandbox": {"meetup_id": 1556336, "urlname": "Meetup-API-Testing"},
        "not-exist": {"meetup_id": 123456, "urlname": "None"},
        "gone": {"meetup_id": 654321, "urlname": "connectedawareness-berlin"},
    }


def create_group(urlname: str) -> Group:
    """
    create group object 
    
    Arguments:
        urlname {str} -- urlname for group object
    
    Returns:
        Group -- new unsaved group object
    """

    return Group(
        meetup_id=0,
        urlname=urlname,
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


@pytest.fixture
def group_1() -> Group:
    """
    create group object

    Returns:
        Group -- unsaved group object
    """
    return create_group(urlname="1")


@pytest.fixture
def group_2() -> Group:
    """
    create group object with a differnet urlname than group_1

    Returns:
        Group -- unsaved group object
    """
    return create_group(urlname="2")


def pytest_runtest_setup():
    """
    Run for each test

    delete elasticsearch index & init the index afterwards
    """
    delte_index()
    init_models()


def pytest_runtest_teardown():
    """
    Run after each test

    delete elasticsearch index
    """
    delte_index()


def delte_index():
    """
    delte elasticsearch index
    """
    print("delete Elasticsearch index: {}".format(Group.Index.name))
    create_app(config_path="/app/config/test.py").config["ES"].indices.delete(
        index=Group.Index.name, ignore=[400, 404]
    )
    sleep(2)


def init_models():
    """
    init elasticsearch index
    """
    Group.init()
    sleep(1)
