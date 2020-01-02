import pytest
from meetup_search.models import Group, Event
from elasticsearch_dsl import connections
from time import sleep
from app import create_app
from flask.app import Flask


@pytest.fixture
def app() -> Flask:
    return create_app(config_path="/app/config/test.py")


def pytest_runtest_setup():
    delte_index()
    init_models()


def pytest_runtest_teardown():
    delte_index()


def delte_index():
    print("delete Elasticsearch index: {}".format(Group.Index.name))
    create_app(config_path="/app/config/test.py").config["ES"].indices.delete(
        index=Group.Index.name, ignore=[400, 404]
    )
    sleep(2)


def init_models():
    Group.init()
    sleep(1)
