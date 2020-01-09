from flask_restful import Resource, reqparse
from elasticsearch_dsl.search import Search
from elasticsearch_dsl.query import Q
from meetup_search.models import Group
from elasticsearch_dsl.response import Response
from typing import List, Dict, Tuple
from .argument_validator import (
    string_list_validator,
    filter_validator,
    positive_int_validator,
)
from elasticsearch_dsl.response.hit import Hit


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
            "sort", type=str, help="Bad sorting: {error_msg}",
        )

        # geo_distance
        self.parser.add_argument(
            "geo_lan", type=float, help="Bad geo latitute: {error_msg}",
        )
        self.parser.add_argument(
            "geo_lon", type=float, help="Bad geo longitute: {error_msg}",
        )
        self.parser.add_argument(
            "geo_distance", type=str, help="Bad distance (example: 100km): {error_msg}",
        )

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

        search_query: dict = {
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
                ]
            }
        }

        # set geo_distance filter
        if args["geo_distance"] and args["geo_lan"] and args["geo_lon"]:
            search = search.filter(
                "geo_distance",
                distance=args["geo_distance"],
                location={"lat": args["geo_lan"], "lon": args["geo_lon"]},
            )

        # pagination
        strat_entry: int = args["page"] * args["limit"]
        end_entry: int = strat_entry + args["limit"]
        search = search[strat_entry:end_entry]

        # filter
        if args["filter"]:
            search = search.filter("term", **args["filter"])

        # sort
        if args["sort"]:
            search = Search().sort(args["sort"])

        # execute search
        search = search.query(Q(search_query))

        # set highlight score
        search.highlight_options(order="score")

        # load response from elasticsearch
        results: Response = search.execute()

        # get response
        found_groups: List[dict] = []
        for group in results.hits:
            # add group dict to array
            if isinstance(group, Hit):
                found_groups.append(
                    {**group.to_dict(),}  # group dict
                )
            else:
                found_groups.append(
                    {
                        **{"score": group.meta.score},  # elasticsearch score
                        **group.to_json_dict(),  # group dict
                    }
                )

        return {"results": found_groups, "hits": results.hits.total["value"]}


class MeetupSearchSuggestApi(Resource):
    @staticmethod
    def get(query: str) -> Dict[str, List[str]]:
        """
        Get Suggestion for query term in Group name

        Arguments:
            query {str} -- query name

        Returns:
            Dict[str, List[str]] -- a list to 5 suggestions
        """

        # run suggest query
        search: Search = Group.search()
        search = search.suggest(
            "suggestion",
            query,
            completion={
                "field": "meetup_id_suggest",
                "field": "urlname_suggest",
                "field": "description_suggest",
                "field": "name_suggest",
            },
        )

        response: Response = search.execute()

        # get suggestion
        suggestion: List[str] = []
        for result in response.suggest.suggestion:
            for option in result.options:
                suggestion.append(option.text)

        return {"suggestions": suggestion}
