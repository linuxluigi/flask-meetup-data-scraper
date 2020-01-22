Getting started
=====================================

.. note::
   These instructions assume familiarity with `Docker <https://www.docker.com/>`_ and
   `Docker Compose <https://docs.docker.com/compose/>`_.

Development & Production Version
--------------------------------

The Project comes with 2 different Docker-Compose files wich are for development ``local.yml`` and production ``production.yml``.

The development version start the website in debug mode and bind the local path ``./`` to the flask docker contaiers path ``/app``. 

For the production version, the docker container is build with the code inside of the container. Also the production version use redis 
as caching backend.

Quick install (Development Version)
-----------------------------------

Build the docker container.

.. code-block:: console

    $ docker-compose -f local.yml build

Load the Meetup Sandbox Group with all events.

.. code-block:: console

    $ docker-compose -f local.yml run flask flask get_group --sandbox True

Start the website.

.. code-block:: console

    $ docker-compose -f local.yml up

Now the server is listen on http://localhost:5000 for any REST API requests.

Quick install (Production Version)
----------------------------------

Settings
^^^^^^^^ 

At first create the directory ``./.envs/.production`` 

.. code-block:: console

    $ mkdir ./.envs/.production`

For flask container create a file ``./.envs/.production/.flask`` wich should look like:

.. code-block::

    # Flask
    # ------------------------------------------------------------------------------
    FLASK_CONFIGURATION=/app/config/production.py
    FLASK_ENV=production
    CORS_ORIGINS=frontend.example.com


For Elasticsearch container create a file ``./.envs/.production/.elasticsearch`` wich should look like below. For further
information how to setup Elasticsearch with enviroment vars got to https://www.elastic.co/guide/en/elasticsearch/reference/current/settings.html

.. code-block::

    # Elasticsearch
    # ------------------------------------------------------------------------------
    http.host=elasticsearch
    http.port=9200
    node.name=elasticsearch1
    cluster.name=meetup-data-scryper-cluster
    cluster.initial_master_nodes=elasticsearch1

Setup
^^^^^

Build the docker container.

.. code-block:: console

    $ docker-compose -f production.yml build

Create the elasticsearch indexes.

.. code-block:: console

    $ docker-compose -f production.yml run flask flask migrate_models

Load Meetuup zip codes for a country.

.. code-block:: console

    $ docker-compose -f production.yml run flask flask load_zip_codes 47.2701114 55.099161 5.8663153 15.0418087 # germany
    $ docker-compose -f production.yml run flask flask load_zip_codes 45.817995 47.8084648 5.9559113 10.4922941 # switzerland
    $ docker-compose -f production.yml run flask flask load_zip_codes 46.3722761 49.0205305 9.5307487 17.160776 # austria

Load Meetuup zip codes for a country.

.. code-block:: console

    $ docker-compose -f production.yml run flask flask load_zip_codes 47.2701114 55.099161 5.8663153 15.0418087 # germany
    $ docker-compose -f production.yml run flask flask load_zip_codes 45.817995 47.8084648 5.9559113 10.4922941 # switzerland
    $ docker-compose -f production.yml run flask flask load_zip_codes 46.3722761 49.0205305 9.5307487 17.160776 # austria

Start the website.

.. code-block:: console

    $ docker-compose -f production.yml up -d
