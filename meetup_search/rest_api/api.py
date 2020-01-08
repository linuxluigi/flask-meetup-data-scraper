from flask_restful import Resource, Api, reqparse
from flask import request
from typing import List, Dict
from elasticsearch_dsl.search import Search
from elasticsearch_dsl.query import MultiMatch, Q
from meetup_search.models import Group
from elasticsearch_dsl.response import Response
from typing import List, Dict
import json
from .argument_validator import (
    string_list_validator,
    filter_validator,
    positive_int_validator,
    sort_validator,
)


class MeetupSearchApi(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()

        # query
        self.parser.add_argument(
            "query", type=str, required=True, help="Bad query: {error_msg}"
        )
        self.parser.add_argument(
            "query_fields",
            type=string_list_validator,
            action="append",
            help="Bad query fields: {error_msg}",
            default=["*"],
        )

        # filter
        self.parser.add_argument(
            "filter", type=filter_validator, help="Bad Filter: {error_msg}"
        )

        # pagination
        self.parser.add_argument(
            "page",
            type=positive_int_validator,
            help="Bad pagination page number: {error_msg}",
            default=0,
        )
        self.parser.add_argument(
            "limit",
            type=int,
            help="Bad pagination limit: {error_msg}",
            choices=(5, 25, 50, 100),
            default=25,
        )

        # sort
        self.parser.add_argument(
            "sort",
            type=sort_validator,
            action="append",
            help="Bad sorting: {error_msg}",
        )

        # todo add geo argument

    def put(self) -> dict:
        """
        search for a group in Elasticsearch

        Returns:
            dict -- search results
        """
        args = self.parser.parse_args()

        # init search
        search: Search = Group.search()

        # add search wildcard to query
        query: str = args["query"]

        # set query_fields
        query_fields: List[str] = args["query_fields"]

        # sort
        # todo fix to enable sorting & don't forget to add a test case!
        # if args["sort"]:
        #     for sort_item in args["sort"]:
        #         search = Search().sort(sort_item)

        search_query: Q = Q(
            {
                "bool": {
                    "should": [
                        {"query_string": {"query": query, "fields": query_fields}},
                        {
                            "nested": {
                                "path": "events",
                                "score_mode": "avg",
                                "query": {
                                    "query_string": {
                                        "query": query,
                                        "fields": query_fields,
                                    }
                                },
                            }
                        },
                        {
                            "nested": {
                                "path": "topics",
                                "score_mode": "avg",
                                "query": {
                                    "query_string": {
                                        "query": query,
                                        "fields": query_fields,
                                    }
                                },
                            }
                        },
                    ]
                }
            }
        )

        # pagination
        strat_entry: int = args["page"] * args["limit"]
        end_entry: int = strat_entry + args["limit"]
        search = search[strat_entry:end_entry]

        # filter
        if args["filter"]:
            search = search.filter("term", **args["filter"])

        # execute search
        search = search.query(search_query)

        # set highlight score
        search.highlight_options(order="score")

        # load response from elasticsearch
        results: Response = search.execute()

        # get response
        found_groups: List[dict] = []
        for group in results.hits:
            # add group dict to array
            found_groups.append(
                {
                    **{"score": group.meta.score},  # elasticsearch score
                    **group.to_json_dict(),  # group dict
                }
            )

        return {"results": found_groups, "hits": results.hits.total["value"]}


class MeetupSearchSuggestApi(Resource):
    def get(self, query: str) -> Dict[str, List[str]]:
        """
        Get Suggestion for query term in Group name

        Arguments:
            query {str} -- query name

        Returns:
            Dict[str, List[str]] -- a list to 5 suggestions
        """

        # run suggest query
        search: Search = Group.search()
        search = search.suggest("suggestion", query, completion={"field": "name"})
        response: Response = search.execute()

        # get suggestion
        suggestion: List[str] = []
        for result in response.suggest.suggestion:
            for option in result.options:
                suggestion.append(option.text)

        return {"suggestions": suggestion}
