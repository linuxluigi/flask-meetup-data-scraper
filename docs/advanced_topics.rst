Advanced topics
=====================================

Changing Models
---------------

The elasticsearch models are stored in ``meetup_search/models`` and the tests are in ``tests/models``. To edit the
models read the `Elasticsearch-DSL Docs <https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html>`_.

Docs
----

The docs are stored in ``./docs`` and written with `Sphinx <https://www.sphinx-doc.org/en/master/>`_. The recommend
way to host sphinx docs are with `readthedocs.org <https://readthedocs.org/>`_.

To compile the docs as HTML use::

    $ docker-compose -f local.yml run flask make --directory docs html

The html output goes to ``docs/_build/html``