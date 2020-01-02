from elasticsearch import Elasticsearch
from os import environ
from elasticsearch_dsl import connections

# GENERAL
# ------------------------------------------------------------------------------
ES_INDEX = "meetup_group"

# ELASTICSEARCH
# ------------------------------------------------------------------------------
# https://elasticsearch-dsl.readthedocs.io/en/latest/configuration.html#multiple-clusters
ELASTICSEARCH_CONNECTION = {
    "default": ["{}:{}".format(environ["http.host"], environ["http.port"])],
}
# https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch
ES: Elasticsearch = Elasticsearch(
    [{"host": environ["http.host"], "port": environ["http.port"]}]
)
# connect to elasticsearch server
connections.create_connection(hosts=ELASTICSEARCH_CONNECTION["default"], timeout=20)
