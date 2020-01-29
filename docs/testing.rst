Testing
=====================================

.. index:: test

.. warning::
   **Do not run Tests on Production Systems!!!** Tests will destroy your Elasticsearch Index!!!

Pytest
------

.. index:: pytest

The unit test are stored in the ``tests`` folder and written with the `Pytest Framework
<https://docs.pytest.org/en/latest/>`_.

Conftest
--------

.. index:: conftest

When executing a test like.

.. code-block:: console

    $ docker-compose -f local.yml run flask coverage run -m pytest

Pytest will at first go to the file ``conftest.py`` and execute the method ``pytest_runtest_setup``
bevor each test and after each test the method ``pytest_runtest_teardown`` will be executed.

.. index:: fixture
.. index:: pytest

Every method witch is an annotation ``@pytest.fixture`` can be used in any test method as a 
param, for deteaild explination go to https://docs.pytest.org/en/latest/fixture.html

Create new test
---------------

To create a new test just create a python file with the prefix ``test_`` in the folder ``/tests``.
It also possible to bundle test in a python package, for that create a folder in ``/tests`` and
add a empty file ``__init__.py`` in the new folder, so that python recognize the folder as a
python package.

In the new test file with the prefix ``tests_`` (example: ``/tests/test_user.py``) add method
also with the prefix ``test_``. An example for the ``/tests/test_user.py`` test file would look
like::

    def test_user():
        assert get_user(username="Hugo").username == "Hugo" 

Execute tests
-------------

To execute all tests run::

    $ docker-compose -f local.yml run flask coverage run -m pytest

To run all tests in a specific module add the path like, in the example run all test in the
path ``tests/api_client``::

    $ docker-compose -f local.yml run flask coverage run -m pytest tests/api_client

For running all test in a file, just add the full path of the file::

    $ docker-compose -f local.yml run flask coverage run -m pytest tests/api_client/test_json_parser.py

To run a single method add 2 colons to the file path with a method name.::

    $ docker-compose -f local.yml run flask coverage run -m pytest tests/api_client/test_json_parser.py::test_get_group_from_response

.. note::
   If you add ``-s`` as param when executing a tests, you can see the terminal output from the test.
   ``docker-compose -f local.yml run flask coverage run -m pytest -s``