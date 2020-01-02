from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections
from envparse import env

# Flask
# ------------------------------------------------------------------------------


# ELASTICSEARCH
# ------------------------------------------------------------------------------
# Elastic Search Model Index
ES_INDEX = "meetup_group"

# https://elasticsearch-dsl.readthedocs.io/en/latest/configuration.html#multiple-clusters
ELASTICSEARCH_CONNECTION = {
    "default": ["{}:{}".format(env("http.host"), env("http.port"))],
}
# https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch
ES: Elasticsearch = Elasticsearch(
    [{"host": env("http.host"), "port": env("http.port")}]
)
# connect to elasticsearch server
connections.create_connection(hosts=ELASTICSEARCH_CONNECTION["default"], timeout=20)
