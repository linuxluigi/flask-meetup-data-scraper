from typing import Dict, List

from elasticsearch_dsl.query import Q
from elasticsearch_dsl.response import Response
from elasticsearch_dsl.response.hit import Hit
from elasticsearch_dsl.search import Search
from flask_restful import Resource, reqparse

from meetup_search.models.group import Group

from .argument_validator import date_validator, positive_int_validator


class MeetupSearchApi(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()

        # query
        self.parser.add_argument(
            "query", type=str, required=True, help="Bad query: {error_msg}"
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
            choices=(5, 10, 25, 100),
            default=10,
        )

        # sort
        self.parser.add_argument(
            "sort", type=str, help="Bad sorting: {error_msg}",
        )

        # load events
        self.parser.add_argument(
            "load_events", type=bool, help="Bad sorting: {error_msg}", default=False,
        )

        # event time filter
        self.parser.add_argument(
            "event_time_gte", type=date_validator, help="Bad date: {error_msg}",
        )
        self.parser.add_argument(
            "event_time_lte", type=date_validator, help="Bad date: {error_msg}",
        )

        # geo_distance
        self.parser.add_argument(
            "geo_lat", type=float, help="Bad geo latitute: {error_msg}",
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

        search_query: dict = {
            "bool": {
                "should": [
                    {"query_string": {"query": args["query"], "fields": ["*"]}},
                    {
                        "nested": {
                            "path": "topics",
                            "score_mode": "avg",
                            "query": {
                                "bool": {
                                    "must": [
                                        {
                                            "query_string": {
                                                "query": args["query"],
                                                "fields": ["*"],
                                            }
                                        }
                                    ]
                                }
                            },
                        }
                    },
                    {
                        "nested": {
                            "path": "events",
                            "score_mode": "avg",
                            "query": {
                                "bool": {
                                    "must": [
                                        {
                                            "query_string": {
                                                "query": args["query"],
                                                "fields": ["*"],
                                            }
                                        }
                                    ]
                                }
                            },
                        }
                    },
                ],
                "must": [],
            }
        }

        # set event time filter
        if args["event_time_gte"] or args["event_time_lte"]:
            range_query: dict = {}
            if args["event_time_gte"]:
                range_query["gte"] = args["event_time_gte"]
            if args["event_time_lte"]:
                range_query["lte"] = args["event_time_lte"]

            search_query["bool"]["must"].append(
                {
                    "nested": {
                        "path": "events",
                        "score_mode": "avg",
                        "query": {
                            "bool": {"must": [{"range": {"events.time": range_query}}]}
                        },
                    }
                }
            )

        # set geo_distance filter
        if args["geo_distance"] and args["geo_lat"] and args["geo_lon"]:
            search_query["bool"]["must"].append(
                {
                    "nested": {
                        "path": "events",
                        "score_mode": "avg",
                        "query": {
                            "bool": {
                                "must": [
                                    {
                                        "geo_distance": {
                                            "distance": args["geo_distance"],
                                            "events.venue_location": {
                                                "lat": args["geo_lat"],
                                                "lon": args["geo_lon"],
                                            },
                                        }
                                    }
                                ]
                            }
                        },
                    }
                }
            )

        # pagination
        strat_entry: int = args["page"] * args["limit"]
        end_entry: int = strat_entry + args["limit"]
        search = search[strat_entry:end_entry]

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
        map_center_lat: float = 0
        map_center_lon: float = 0
        for group in results.hits:

            group_dict: dict = {}
            if isinstance(group, Hit):
                group_object = Group.get_group(urlname=group.to_dict()["urlname"])
                group_dict = group_object.to_json_dict(load_events=args["load_events"])
            else:
                group_dict = group.to_json_dict(load_events=args["load_events"])

            if "venue_location_average" in group_dict:
                map_center_lat = (
                    map_center_lat + group_dict["venue_location_average"]["lat"]
                )
                map_center_lon = (
                    map_center_lon + group_dict["venue_location_average"]["lon"]
                )
            else:
                map_center_lat = map_center_lat + group_dict["location"]["lat"]
                map_center_lon = map_center_lon + group_dict["location"]["lon"]

            # add group dict to array
            found_groups.append(
                {**group_dict,}
            )

        if len(found_groups) > 0:
            map_center_lat = map_center_lat / len(found_groups)
            map_center_lon = map_center_lon / len(found_groups)

        return {
            "results": found_groups,
            "hits": results.hits.total["value"],
            "map_center": {"lat": map_center_lat, "lon": map_center_lon},
        }


class MeetupSearchSuggestApi(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()

        # query
        self.parser.add_argument(
            "query", type=str, required=True, help="Bad query: {error_msg}"
        )

    def put(self) -> Dict[str, List[str]]:
        """
        Get Suggestion for query term in Group name

        Returns:
            Dict[str, List[str]] -- a list to 5 suggestions
        """
        args = self.parser.parse_args()

        # run suggest query
        search: Search = Group.search()
        search = search.suggest(
            "suggestion", args["query"], completion={"field": "name_suggest"},
        )

        response: Response = search.execute()

        # get suggestion
        suggestion: List[str] = []
        for result in response.suggest.suggestion:
            for option in result.options:
                suggestion.append(option.text)

        return {"suggestions": suggestion}
