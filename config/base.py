from elasticsearch import Elasticsearch
from os import environ
from elasticsearch_dsl import connections

# GENERAL
# ------------------------------------------------------------------------------

DEBUG: bool = bool(environ["DEBUG"])

# ELASTICSEARCH
# ------------------------------------------------------------------------------
# https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch
es: Elasticsearch = Elasticsearch(
    [{"host": environ["http.host"], "port": environ["http.port"]}]
)

# https://elasticsearch-dsl.readthedocs.io/en/latest/configuration.html#multiple-clusters
ELASTICSEARCH_CONN = {
    "default": ["{}:{}".format(environ["http.host"], environ["http.port"])],
}
