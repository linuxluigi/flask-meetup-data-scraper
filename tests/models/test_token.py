from time import sleep

import pytest
from pytest_httpserver import HTTPServer

from meetup_search.meetup_api_client.exceptions import HttpNoSuccess
from meetup_search.models.token import Token


def test_get_token(auth_token: Token):
    # test without any token exists
    assert Token.get_token() is None

    # add token to elasticsearch
    auth_token.save()
    sleep(1)

    # get token from elasticsearch
    auth_token_2: Token = Token.get_token()

    # assert if auth_token is auth_token_2
    assert auth_token.access_token == auth_token_2.access_token
    assert auth_token.refresh_token == auth_token_2.refresh_token

def test_delete_all_tokens(auth_token: Token):
    # add token to elasticsearch
    auth_token.save()
    sleep(1)

    # delete all tokens
    Token.delete_all_tokens()
    sleep(1)

    # assert if get_token get no token
    assert Token.get_token() is None

def test_get_refresh_token(httpserver: HTTPServer, auth_token: Token):
    response_json: dict = {
        "access_token":"ACCESS_TOKEN_TO_STORE",
        "token_type": "bearer",
        "expires_in":3600,
        "refresh_token":"TOKEN_USED_TO_REFRESH_AUTHORIZATION"
    }

    # create a invalid http request
    httpserver.expect_oneshot_request("/HttpNoSuccess")

    # refresh token with an error
    with pytest.raises(HttpNoSuccess):
        auth_token.get_refresh_token(post_url=httpserver.url_for("/refresh"))

    # set up the server to serve /refresh with the json
    httpserver.expect_request("/refresh").respond_with_json(response_json)

    # refresh token
    auth_token.get_refresh_token(post_url=httpserver.url_for("/refresh"))

    # assert if token was refreshed
    assert auth_token.access_token == response_json["access_token"]
    assert auth_token.refresh_token == response_json["refresh_token"]

    sleep(1)

    # assert if token was saved
    auth_token_2: Token = Token.get_token()
    assert isinstance(auth_token_2, Token)
    assert auth_token_2.access_token == auth_token.access_token
    assert auth_token_2.refresh_token == auth_token.refresh_token
