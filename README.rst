Meetup Data Scraper
======================

Dowload group & events from Meetup-API into a database to make a fulltext search on every event.

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style
.. image:: https://travis-ci.com/linuxluigi/flask-meetup-data-scraper.svg?branch=master
     :target: https://travis-ci.com/linuxluigi/flask-meetup-data-scraper
     :alt: Travis CI tests
.. image:: https://readthedocs.org/projects/flask-meetup-data-scraper/badge/?version=latest
     :target: https://flask-meetup-data-scraper.readthedocs.io/en/latest/?badge=latest
     :alt: Documentation Status
.. image:: https://api.codacy.com/project/badge/Grade/09b0518479d547d2a86c2a925e525160
     :target: https://www.codacy.com/manual/linuxluigi/flask-meetup-data-scraper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=linuxluigi/flask-meetup-data-scraper&amp;utm_campaign=Badge_Grade
     :alt: Codacy quality
.. image:: https://api.codacy.com/project/badge/Coverage/09b0518479d547d2a86c2a925e525160
     :target: https://www.codacy.com/manual/linuxluigi/flask-meetup-data-scraper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=linuxluigi/flask-meetup-data-scraper&amp;utm_campaign=Badge_Coverage
     :alt: Coverage
.. image:: https://static.deepsource.io/deepsource-badge-light.svg
     :target: https://deepsource.io/gh/linuxluigi/flask-meetup-data-scraper/?ref=repository-badge
     :alt: DeepSource

Basic Commands
--------------

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ docker-compose -f local.yml run flask coverage run -m mypy /app

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ docker-compose -f local.yml run flask coverage run -m pytest
    $ docker-compose -f local.yml run flask coverage run -m coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ docker-compose -f local.yml run flask coverage run -m pytest


Create Docs
^^^^^^^^^^^

For creating the docs use from sphinx the makefile::

    $ docker-compose -f local.yml run flask make --directory docs html

Than the docs will be generated into ``docs/_build/html``.

For more options check out the help::

    $ docker-compose -f local.yml run flask make --directory docs help


Deployment
----------

The following details how to deploy this application.



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html

