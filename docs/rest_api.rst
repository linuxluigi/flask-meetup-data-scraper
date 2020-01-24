.. _rest_api:

Rest API Documentation
======================

About
-----

The REST API is based on `Flask RESTful <https://flask-restful.readthedocs.io/en/latest/>`_. To add or remove
Endpoints modify in ``app.py`` the method ``create_app``. Example how to add add suggestion & search::

    # init flask api
    api: Api = Api(app)
    # add api endpoints
    api.add_resource(MeetupSearchApi, "/")
    api.add_resource(MeetupSearchSuggestApi, "/suggest/")

The code for the REST API is in ``meetup_search/rest_api/api.py`` and the tests are in ``tests/rest_api/test_api.py``.

Also in ``tests/rest_api/utily.py`` are helper methods to tests the REST API!

Suggestion
----------

``PUT /suggest/`` 

Return up to 5 suggestion based on group names.

Example, when send a ``PUT /suggest/`` with follow data::

    {
        'query': 'jam',
    }

The output will be like::

    {"suggestions": [
        "Jam-Session Berlin",
        "Jam Time Amsterdam",
        "Jammy @ ROMA",
    ]}

Search
------

``PUT /``

Create a fulltext search on every group saved in Elasticsearch. 

Example of every possible PUT Data::

    {
        'query': 'my_query',
        'load_events': true,
        'page': 0,
        'limit': 10,
        'sort': ['urlname', '-meetup_id'],
        'geo_distance': '100km',
        'geo_lat': 52.13,
        'geo_lon': 13.12,
        'event_time_gte': '2019-11-01',
        'event_time_lte': '2020-01-01'
    }

And the result will be a list of Group models, go to 
`Meetup API Doc <https://www.meetup.com/de-DE/meetup_api/docs/:urlname/?uri=%2Fmeetup_api%2Fdocs%2F%3Aurlname%2F#get>`_
for fields description::

    {
        'results': [
            # required fields
            'meetup_id': int,
            'urlname': str,
            'created': str,
            'description': str,
            'name': str,
            'link': str,
            'location': {
                'lat': float,
                'lon': float,
            },
            'members': int,
            'status': str,
            'timezone': str,
            'visibility': str,

            # extra optional fields from the rest api (get every venue location from all events in the group)
            'venues': [
                'name': str,
                'location': {
                    'lat': float,
                    'lon': float,
                }
            ],
            'venue_location_average': {
                'lat': float,
                'lon': float,
            },

            # optional fields
            'score': float;
            'nomination_acceptable': bool,
            'city': str,
            'city_link': str,
            'country': str,
            'fee_options_currencies_code': str,
            'fee_options_currencies_default': bool,
            'fee_options_type': str,
            'join_mode': str,
            'localized_country_name': str,
            'localized_location': str,
            'member_limit': int,
            'short_link': str,
            'state': str,
            'untranslated_city': str,
            'welcome_message': str,
            'who': str,
            'category_id': long,
            'category_name': str,
            'category_shortname': str,
            'category_sort_name': str,
            'meta_category_id': long,
            'meta_category_shortname': str,
            'meta_category_name': str,
            'meta_category_sort_name': str,
            'topics': [
                'meetup_id': str,
                'lang': str,
                'name': str,
                'urlkey': str,
            ],
            'organizer_id': int,
            'organizer_name': str,
            'organizer_bio': str,
            'events': [
                # required fields
                'meetup_id': str,
                'time': str,
                'name': str,
                'link': str,
                'date_in_series_pattern': bool,

                # optional fields
                'attendance_count': int,
                'attendance_sample': int,
                'attendee_sample': int,
                'created': str,
                'description': str,
                'duration': long,
                'fee_accepts': str,
                'fee_amount': int,
                'fee_currency': str,
                'fee_description': str,
                'fee_label': str,
                'how_to_find_us': str,
                'status': str,
                'updated': str,
                'utc_offset': long,
                'venue_visibility': str,
                'visibility': str,
                'venue_address_1': str,
                'venue_address_2': str,
                'venue_address_3': str,
                'venue_city': str,
                'venue_country': str,
                'venue_localized_country_name': str,
                'venue_name': str,
                'venue_phone': str,
                'venue_zip_code': str,
                'venue_location': {
                    'lat': float,
                    'lon': float,
                },
                'event_host_host_count': int,
                'event_host_id': int,
                'event_host_intro': str,
                'event_host_join_date': str,
                'event_host_name': str,
            ]
        ],
        'hits': int,
        'map_center': {
            'lat': float,
            'lon': float,
        }
    }


PUT Data fields
^^^^^^^^^^^^^^^

query
.....

``query`` is the only ``required`` field for a search request. The query has to be a string and could also use
wildcards like ``*``. Example for a minimal search request::

    {
        'query': 'my_query',
    }

load_events
...........

By default events will not be send through a search request, only if ``load_events`` is set to ``True``::

    {
        'load_events': true,
    }

pagination
..........

For pagination use the fields ``limit`` (how many groups will load on a request) and ``page``.

When not set the default value for ``page`` is ``0`` and for ``limit`` is it ``10``.

``limit`` only accept ``5``, ``10``, ``25``, ``100`` as valid value!

It's possible to just use ``page`` or ``limit`` without the other, than the default values will be used!

Example for the secound page with 25 entries per page.::

    {
        'query': 'my_query',
        'page': 2,
        'limit': 55,
    }


sorting
.......

It's possible to sort the groups by field (only work on group fields, not an nested fields like ``events`` or ``topic``).

To costimize sorting read the `sort docs <https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#sorting>`_!

To sort a query by ``urlname`` in ``asc`` and ``meetup_id`` in ``desc`` use::

    {
        'query': 'my_query',
        'sort': ['urlname', '-meetup_id'],
    }

geo_distance
............

To filter groups by a geo_distance the fields ``geo_distance``, ``geo_lat`` & ``geo_lon`` have to be all set, there is no default value!

The distance filter check for events venue location, if a group has any event with a venue in the distance it will be return.

``geo_distance`` accept `elasticsearch distance units <https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#distance-units>`_

``geo_lat`` & ``geo_lon`` accecpt float values. To get geopoints of citys and points of intresst you can use `Nominatim <https://nominatim.openstreetmap.org/>`_.

For deeper explination go to 
`Geo-distance query doc <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-distance-query.html>`_

Example for a distance request on Berlin with 100km::

    {
        'query': 'my_query',
        'geo_distance': '100km',
        'geo_lat': 52.520008,
        'geo_lon': 13.404954,
    }

Filter by event time
....................

The fields ``event_time_gte`` and ``event_time_lte`` are used to filter events by the time when they was done.

Attation, when at leats one event of a group was hit, the hole group with all events will be returned!

To filter events with a date greater or equal date than ``2019-11-01`` use::

    {
        'query': 'my_query',
        'event_time_gte': '2019-11-01',
    }

To filter events with a date less or equal than ``2020-01-01`` use::

    {
        'query': 'my_query',
        'event_time_lte': '2020-01-01'
    }

It's alo possible to use both filter at once, so to filter a date greater or equal date than ``2019-11-01``
and less or equal than ``2020-01-01`` use::

    {
        'query': 'my_query',
        'event_time_gte': '2019-11-01',
        'event_time_lte': '2020-01-01'
    }