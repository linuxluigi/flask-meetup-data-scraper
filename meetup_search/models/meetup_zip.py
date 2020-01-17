from __future__ import annotations

from elasticsearch_dsl import Document, Text, Q
from typing import List
from elasticsearch_dsl.search import Search
from elasticsearch_dsl.response import Response


class MeetupZip(Document):
    """
    Meetup.com Zip Model with elasticsearch persistence

    Meetup Zip doc: https://www.meetup.com/de-DE/meetup_api/docs/find/locations/?uri=%2Fmeetup_api%2Fdocs%2Ffind%2Flocations%2F

    Elasticsearch persistence doc -> https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html#persistence

    Raises:
        GroupDoesNotExists: Raise when request a group wich does not exists on elasticsearch or on meetup
    """

    zip_code = Text(required=True)

    class Index:
        """
        Elasticsearch index of the model

        for override the default index -> https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html#document-life-cycle
        """

        name = "meetup_zip"

    @staticmethod
    def get_or_create_zip(zip_code: str) -> MeetupZip:
        """
        Get or create a new Zip

        Arguments:
            zip_code {str} -- meetup zip code

        Returns:
            MeetupZip -- load zip from elasticsearch or a new created zip model
        """

        # get MeetupZip from elasticsearch. if exists
        s: Search = MeetupZip.search()
        s = s.query("match", zip_code=zip_code)
        results: Response = s.execute()
        for meetup_zip in results:
            return meetup_zip

        # create a new MeetupZip and save it to elasticsearch
        new_meetup_zip: MeetupZip = MeetupZip(zip_code=zip_code)
        new_meetup_zip.save()

        # return saved MeetupZip object
        return new_meetup_zip

    @staticmethod
    def get_or_create_zips(zip_code_list: List[str]) -> List[MeetupZip]:
        """
        Get or create a list of MeetupZip objects

        Arguments:
            zip_code_list {List[str]} -- list of zip codes

        Returns:
            List[MeetupZip] -- get or created MeetupZip objects
        """

        # remove double entries from list
        zip_code_list = list(set(zip_code_list))

        # create return list
        meetup_zips: List[MeetupZip] = []

        for zip_code in zip_code_list:
            meetup_zips.append(
                MeetupZip.get_or_create_zip(zip_code=zip_code)
            )

        return meetup_zips

    @staticmethod
    def get_all_zips() -> List[MeetupZip]:
        """
        Get all MeetupZip from elasticsearch

        Returns:
            List[MeetupZip] -- List of all MeetupZip
        """
        # init search
        search: Search = MeetupZip.search()

        # create search query
        search_query: dict = {"match_all": {}}

        # execute search
        search = search.query(Q(search_query))

        # load response from elasticsearch
        results: Response = search.execute()

        # create return array
        meetup_zips: List[MeetupZip] = []

        for meetup_zip in results.hits:
            meetup_zips.append(meetup_zip)

        return meetup_zips
