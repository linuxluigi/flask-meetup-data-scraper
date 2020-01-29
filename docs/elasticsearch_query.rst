Elasticsearch Queries
=====================

.. index:: Elasticsearch

The main Elasticsearch Query is written in ``meetup_search/rest_api/api.py`` and the tests are in 
``tests/rest_api/test_api.py``. This project use https://github.com/elastic/elasticsearch-dsl-py 
to handle Elasticsearch, if you want to modify the query, go to
https://elasticsearch-dsl.readthedocs.io/en/latest/ for help.

To run the tests for the ``api`` run::

  $ docker-compose -f local.yml run flask coverage run -m pytest -s tests/rest_api/test_api.py

To run a single test use::

  $ docker-compose -f local.yml run flask coverage run -m pytest -s tests/rest_api/test_api.py::test_search_query

