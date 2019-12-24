import pytest
from meetup_search.models import Group, Event
from elasticsearch_dsl import connections
from config.base import ELASTICSEARCH_CONN, es
from time import sleep


def pytest_runtest_setup():
    # todo remove double code
    connections.create_connection(hosts=ELASTICSEARCH_CONN["default"], timeout=20)
    delte_index()
    init_models()


def delte_index():
    print("delete Elasticsearch index: {}".format(Group.Index.name))
    es.indices.delete(index=Group.Index.name, ignore=[400, 404])
    sleep(2)


def init_models():
    Group.init()
