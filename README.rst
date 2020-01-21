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
.. image:: https://static.deepsource.io/deepsource-badge-light-mini.svg
     :target: https://deepsource.io/gh/linuxluigi/flask-meetup-data-scraper/?ref=repository-badge
     :alt: DeepSource
.. image:: https://pyup.io/repos/github/linuxluigi/flask-meetup-data-scraper/shield.svg
     :target: https://pyup.io/repos/github/linuxluigi/flask-meetup-data-scraper/
     :alt: Updates
.. image:: https://pyup.io/repos/github/linuxluigi/flask-meetup-data-scraper/python-3-shield.svg
     :target: https://pyup.io/repos/github/linuxluigi/flask-meetup-data-scraper/
     :alt: Python 3

Basic Commands
--------------

Flask Commands
^^^^^^^^^^^^^^

Show help::

  $ docker-compose -f local.yml run flask flask

Migrate all models into Elasticsearch::

  $ docker-compose -f local.yml run flask flask migrate_models

Load a single Meetup Group::

  $ docker-compose -f local.yml run flask flask get_group MeetupGoupUrlName
  $ docker-compose -f local.yml run flask flask get_group --sandbox True # load sandbox group

Load all groups from JSON files from a path, default path is ``/app/meetup_groups``::

  $ docker-compose -f local.yml run flask flask get_groups # use default path
  $ docker-compose -f local.yml run flask flask get_groups /app/meetup_groups # use custom path
  $ docker-compose -f local.yml run flask flask get_groups --load_events False # don't load events from groups

Load new meetup zip codes from meetup.com within a boundingbox::

  $ docker-compose -f local.yml run flask flask load_zip_codes 47.2701114 55.099161 5.8663153 15.0418087 # germany
  $ docker-compose -f local.yml run flask flask load_zip_codes 45.817995 47.8084648 5.9559113 10.4922941 # switzerland
  $ docker-compose -f local.yml run flask flask load_zip_codes 46.3722761 49.0205305 9.5307487 17.160776 # austria

Get all new past events from all groups in Elasticsearch::

  $ docker-compose -f local.yml run flask flask update_groups

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

