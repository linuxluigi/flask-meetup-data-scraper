.. _rest_api:

Rest API Documentation
======================

Suggestion
----------

``GET /suggest/query/`` 

Return up to 5 suggestion based on group names.

Example Output for ``GET /suggest/jam/`` ::

    {"suggestions": [
        "Jam-Session Berlin",
        "Jam Time Amsterdam",
        "Jammy @ ROMA",
    ]}

Search
------

``PUT /``

PUT Data::

    {
        "query": query,
        "query_fields": query_fields,
        "filter": filters,
        "exclude": excludes
    }

