Getting started
=====================================

.. note::
   These instructions assume familiarity with `Docker <https://www.docker.com/>`_ and
   `Docker Compose <https://docs.docker.com/compose/>`_.

Development & Production Version
--------------------------------

The Project comes with 2 different Docker-Compose files wich are for development ``local.yml`` and
production ``production.yml``.

The development version start the website in debug mode and bind the local path ``./`` to the flask
docker contaiers path ``/app``. 

For the production version, the docker container is build with the code inside of the container.
Also the production version use redis as caching backend.

Quick install (Development Version)
-----------------------------------

.. index:: Quickstart development

Build the docker container.

.. code-block:: console

    $ docker-compose -f local.yml build

Migrate all models into Elasticsearch

.. code-block:: console

    $ docker-compose -f local.yml run flask flask migrate_models

Load the Meetup Sandbox Group with all events.

.. code-block:: console

    $ docker-compose -f local.yml run flask flask get_group --sandbox True

Start the website.

.. code-block:: console

    $ docker-compose -f local.yml up

Now the server is listen on http://localhost:5000 for any REST API requests.

Quick install (Production Version)
----------------------------------

.. index:: Quickstart production

Settings
^^^^^^^^ 

At first create the directory ``./.envs/.production`` 

.. code-block:: console

    $ mkdir ./.envs/.production`

For flask container create a file ``./.envs/.production/.flask`` wich should look like:

.. code-block::

    # Flask
    # ------------------------------------------------------------------------------
    SECRET_KEY=very_long_unique_random_string!!
    FLASK_CONFIGURATION=/app/config/production.py
    FLASK_ENV=production
    CORS_ORIGINS=frontend.example.com
    DOMAIN=meetup-search.de
 
    # Meetup.com OAuth
    # ------------------------------------------------------------------------------
    MEETUP_CLIENT_ID=your_meetup_oauth_client_id
    MEETUP_CLIENT_SECRET=your_meetup_oauth_client_secret
    OAUTHLIB_INSECURE_TRANSPORT=1

    # Meetup.com groups region
    # ------------------------------------------------------------------------------
    # set the boundingbox for downloading all meetup zip codes in the area
    LOCATION_BOUNDINGBOX=germany=47.2701114 55.099161 5.8663153 15.0418087,switzerland=45.817995 47.8084648 5.9559113 10.4922941,austria=46.3722761 49.0205305 9.5307487 17.160776
    # set the countrys, from where you want to download meetup group & events
    LOCATION_COUNTRIES=DE,CH,AT

To fill the section ``# Meetup.com OAuth`` you need an API account from `Meetup.com 
<https://www.meetup.com/start/description?couponcode=winback-discount-50>`_.
When setting up the meetup oauth account add ``https://you-domain.com/callback`` as your
callback url & with ``https://you-domain.com/login`` you can log in with your meetup account.

To read how to handle a boundingbox in the section ``# Meetup.com groups region`` go to
:ref:`load_zip_codes_command`.

For Elasticsearch container create a file ``./.envs/.production/.elasticsearch`` wich should look
like below. For further information how to setup Elasticsearch with enviroment vars got to
https://www.elastic.co/guide/en/elasticsearch/reference/current/settings.html

.. code-block::

    # Elasticsearch
    # ------------------------------------------------------------------------------
    http.host=elasticsearch
    http.port=9200
    node.name=elasticsearch1
    cluster.name=meetup-data-scryper-cluster
    cluster.initial_master_nodes=elasticsearch1

Add Users
^^^^^^^^^

Frontend & backend has the same endpoint for user authentification. Both use Basic Auth from  
`traefik <https://docs.traefik.io/v2.0/middlewares/basicauth/>`_. To add a user, use ``htpasswd``
and store the user data into ``compose/production/traefik/basic-auth-usersfile``. Example use in
Linux:

.. code-block:: console

    $ sudo apt install apache2-utils # install htpasswd
    $ htpasswd -c compose/production/traefik/basic-auth-usersfile username

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

Conjob
^^^^^^

Add a cronjob to run every week. So that every ``4`` weeks the elasticsearch index should be
resetet. If you want a another periode change the ``4`` with your periode time. But don't use a
persiod over 30 days! It is forbidden by meetup.com!!::

    0	3	*	*	6	docker-compose -f production.yml run flask flask reset_index --reset_periode 4

Description what does this command do, is under :ref:`reset_index_command`.