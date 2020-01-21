C/I
===

.. index:: CI

About
-----

Flask Meetup Data Scraper use Github.com Marketplace Apps to maintain the project. Every App is for free for Open Source projects!

Code Style
----------

Black
^^^^^

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

`Black <https://github.com/ambv/black>`_ is not integrated as a C/I, it's just a python code auto formater for the project. So if you like
to contribute your code use black by ``python black ./``!

Tests
-----

Travis
^^^^^^

.. image:: https://travis-ci.com/linuxluigi/flask-meetup-data-scraper.svg?branch=master
     :target: https://travis-ci.com/linuxluigi/flask-meetup-data-scraper
     :alt: Travis CI tests

This project use for testing `unit test <https://docs.pytest.org/en/latest/>`_, `flask commands <https://flask.palletsprojects.com/en/1.1.x/cli/>`_ & 
Docker-Compose builds `Travis <https://travis-ci.com/>`_

Travis config is ``.travis.yml`` 

Documentation
-------------

Readthedocs.org
^^^^^^^^^^^^^^^

.. image:: https://readthedocs.org/projects/flask-meetup-data-scraper/badge/?version=latest
     :target: https://flask-meetup-data-scraper.readthedocs.io/en/latest/?badge=latest
     :alt: Documentation Status

Documentation is written in `Sphinx <https://www.sphinx-doc.org/en/master/ >`_ in ``.rst`` file format.
The sourcecode of the docs is in ``docs/`` 

Travis config is ``.readthedocs.yml``

Code Review
-----------

Codacy.com
^^^^^^^^^^

.. image:: https://api.codacy.com/project/badge/Grade/09b0518479d547d2a86c2a925e525160
     :target: https://www.codacy.com/manual/linuxluigi/flask-meetup-data-scraper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=linuxluigi/flask-meetup-data-scraper&amp;utm_campaign=Badge_Grade
     :alt: Codacy quality
.. image:: https://api.codacy.com/project/badge/Coverage/09b0518479d547d2a86c2a925e525160
     :target: https://www.codacy.com/manual/linuxluigi/flask-meetup-data-scraper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=linuxluigi/flask-meetup-data-scraper&amp;utm_campaign=Badge_Coverage
     :alt: Coverage

`Codacy.com <https://www.codacy.com>`_ is an automated code analysis/quality tool. Codacy analyze only python for this project, 
also the coverage of the test are uploaded to `Codacy.com <https://www.codacy.com>`_ via `Travis <https://travis-ci.com/>`_.

DeepSource.io
^^^^^^^^^^^^^

.. image:: https://static.deepsource.io/deepsource-badge-light-mini.svg
     :target: https://deepsource.io/gh/linuxluigi/flask-meetup-data-scraper/?ref=repository-badge
     :alt: DeepSource

`DeepSource.io <https://www.deepsource.io>`_ is like `Codacy.com <https://www.codacy.com>`_ but it also analyze Dockerfiles.

DeepSource config is ``.deepsource.toml``

Dependencies
------------

Pyup.io
^^^^^^^

.. image:: https://pyup.io/repos/github/linuxluigi/flask-meetup-data-scraper/shield.svg
     :target: https://pyup.io/repos/github/linuxluigi/flask-meetup-data-scraper/
     :alt: Updates

.. image:: https://pyup.io/repos/github/linuxluigi/flask-meetup-data-scraper/python-3-shield.svg
     :target: https://pyup.io/repos/github/linuxluigi/flask-meetup-data-scraper/
     :alt: Python 3

`Pyup.io <https://pyup.io>`_ update Python packages once a week. It push every update to an extra banch & create a pull request.

Pyup config is ``.pyup.yml``

Dependabot.com
^^^^^^^^^^^^^^

`Dependabot.com <https://dependabot.com/>`_ update Dockerfiles once a week. It push every update to an extra banch & create a pull request.

Dependabot config is ``.dependabot/config.yml``