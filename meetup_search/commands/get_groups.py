from meetup_search.models import Group, Event
import json
import glob
from meetup_search.meetup_api_client.meetup_api_client import MeetupApiClient
from typing import List
from meetup_search.meetup_api_client.exceptions import (
    GroupDoesNotExistsOnMeetup,
    MeetupConnectionError,
)


def get_groups(meetup_files_path: str):
    """
    parse all JSON files in meetup_files_path, get the group name and index every group into elasticsearch
    
    Arguments:
        meetup_files_path {str} -- path of the JSON files
    """
    
    api_client: MeetupApiClient = MeetupApiClient()

    mettup_groups_files: List[str] = glob.glob("{}/*.json".format(meetup_files_path))

    group_counter: int = 0
    group_not_exists_counter: int = 0
    event_counter: int = 0

    for mettup_groups_file in mettup_groups_files:
        with open(mettup_groups_file) as json_file:
            data = json.load(json_file)

            for group_data in data:
                try:
                    group: Group = api_client.get_group(data[group_data]["urlname"])
                except (GroupDoesNotExistsOnMeetup, MeetupConnectionError) as e:
                    print(e)
                    group_not_exists_counter = group_not_exists_counter + 1
                    break

                group_counter = group_counter + 1

                group_events: List[Event] = api_client.update_all_group_events(
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
