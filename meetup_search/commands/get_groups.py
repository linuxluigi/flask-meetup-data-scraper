from config.base import es
from datetime import datetime
from meetup_search.models import Group, Event
from tests.meetup_api_demo_response import get_group_response
import json
import glob
from meetup_search.meetup_api_client.meetup_api_client import MeetupApiClient
from elasticsearch_dsl import connections
from config.base import ELASTICSEARCH_CONN


class GetGroups:
    def __init__(self, *args, **options):
        super().__init__()
        api_client: MeetupApiClient = MeetupApiClient()

        options["json_path"] = "/app/meetup_groups"
        # if not options["json_path"]:
        #     options["json_path"] = "/app/meetup_groups"

        mettup_groups_files: [] = glob.glob("{}/*.json".format(options["json_path"]))

        group_counter: int = 0
        group_not_exists_counter: int = 0
        event_counter: int = 0

        # todo remove double code
        connections.create_connection(hosts=ELASTICSEARCH_CONN["default"], timeout=20)

        for mettup_groups_file in mettup_groups_files:
            with open(mettup_groups_file) as json_file:
                data = json.load(json_file)

                for group_data in data:
                    group: Group = api_client.get_group(data[group_data]["urlname"])

                    #  break if group not exists
                    if not group:
                        group_not_exists_counter = group_not_exists_counter + 1
                        break
                    group_counter = group_counter + 1

                    group_events: [Event] = api_client.update_all_group_events(
                        group=group
                    )

                    event_counter = event_counter + len(group_events)

                    print(
                        "Group {} was updatet with {} events".format(
                            group.name, len(group_events)
                        )
                    )

        print(
            "{} groups was updatet with {} new events & {} do not exists anymore".format(
                group_counter, event_counter, group_not_exists_counter
            )
        )
