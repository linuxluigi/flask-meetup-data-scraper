from __future__ import annotations

from typing import List, Optional

import requests
from elasticsearch_dsl import Document, Q, Text
from elasticsearch_dsl.response import Response
from elasticsearch_dsl.search import Search
from environs import Env
from meetup_search.meetup_api_client.exceptions import HttpNoSuccess
from requests.models import Response


class Token(Document):
    """
    Meetup OAuth token
    """

    access_token = Text(required=True)
    refresh_token = Text(required=True)

    class Index:
        name = "token"

    @staticmethod
    def get_token() -> Optional[Token]:
        """
        get current auth token
        
        Returns:
            Token -- [description]
        """
        s: Search = Token.search()
        s = s.query("match_all")
        results: Response = s.execute()

        for token in results:
            return token

        return None

    @staticmethod
    def delete_all_tokens():
        """
        delete all tokens
        """
        s: Search = Token.search()
        s = s.query("match_all")
        results: Response = s.execute()

        for token in results:
            token.delete()


    def get_refresh_token(self, post_url: str = "https://secure.meetup.com/oauth2/access"):
        """
        refresh auth token
        """
        env: Env = Env()
        data = {
            'client_id': env("MEETUP_CLIENT_ID"),
            'client_secret': env("MEETUP_CLIENT_SECRET"),
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            }
        response: Response = requests.post(post_url, data=data)

        if response.status_code != 200:
            raise HttpNoSuccess(
                "There is something wrong on {} to refresh the auth token!".format(
                    data
                )
            )

        json_response: dict = response.json()

        self.access_token = json_response["access_token"]
        self.refresh_token = json_response["refresh_token"]
        self.save()
