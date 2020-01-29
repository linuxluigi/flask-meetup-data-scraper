from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections
from environs import Env

env = Env()

# Flask Rest Api
# ------------------------------------------------------------------------------
# Bundle Argument Erros
# https://flask-restful.readthedocs.io/en/latest/reqparse.html#multiple-values-lists
BUNDLE_ERRORS = False


# ELASTICSEARCH
# ------------------------------------------------------------------------------
# Elastic Search Model Index
ES_INDEX = "meetup_group"

# Elasticsearch Connections List
# https://elasticsearch-dsl.readthedocs.io/en/latest/configuration.html#multiple-clusters
ELASTICSEARCH_CONNECTION = {
    "default": ["{}:{}".format(env("http.host"), env("http.port"))],
}

# Single Elastic Search instance
# https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch
ES: Elasticsearch = Elasticsearch(
    [{"host": env("http.host"), "port": env("http.port")}]
)

# connect to elasticsearch server
connections.create_connection(hosts=ELASTICSEARCH_CONNECTION["default"], timeout=20)
