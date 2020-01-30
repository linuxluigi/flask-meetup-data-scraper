from flask.helpers import url_for
from flask.testing import FlaskClient
from pytest_flask.plugin import JSONResponse

from environs import Env

from .utily import generate_search_dict


def test_cors_headers(client: FlaskClient):
    """
    check if cors headers are set

    Arguments:
        client {FlaskClient} -- client to access flask web ressource
    """
    env: Env = Env()

    # set search request to get a response header
    response_1: JSONResponse = client.put(
        url_for("meetupsearchapi"), data=generate_search_dict(query="v")
    )

    # check if cors header are the same as in the enviroment var
    assert response_1.headers["Access-Control-Allow-Origin"] == env("CORS_ORIGINS")
