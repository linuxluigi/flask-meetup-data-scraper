import glob
import json
from typing import Dict, List

import click
from flask.cli import with_appcontext
from meetup_search.meetup_api_client.exceptions import GroupDoesNotExistsOnMeetup, MeetupConnectionError
from meetup_search.meetup_api_client.meetup_api_client import MeetupApiClient
from meetup_search.models.group import Event, Group


@click.command(name="get_groups")
@click.option("--load_events", nargs=1, type=bool, default=True)
@with_appcontext
@click.argument(
    "meetup_files_path",
    type=click.Path(exists=True),
    required=False,
    default="meetup_groups",
)
def get_groups(meetup_files_path: str, load_events: bool) -> Dict[str, List[str]]:
    """
    parse all JSON files in meetup_files_path, get the group name and index every group into elasticsearch

    Arguments:
        meetup_files_path {str} -- path of the JSON files
        load_events {bool} -- load all events from groups

    Returns:
        Dict[str, List[str]] -- dict with valid & invalid group lists
    """

    api_client: MeetupApiClient = MeetupApiClient()

    mettup_groups_files: List[str] = glob.glob("{}/*.json".format(meetup_files_path))

    groups_dict: Dict[str, List[str]] = {"valid": [], "invalid": []}
    event_counter: int = 0

    for mettup_groups_file in mettup_groups_files:
        with open(mettup_groups_file) as json_file:
            data = json.load(json_file)

            for group_data in data:
                try:
                    group: Group = api_client.get_group(data[group_data]["urlname"])
                except (GroupDoesNotExistsOnMeetup, MeetupConnectionError) as e:
                    print(e)
                    groups_dict["invalid"].append(data[group_data]["urlname"])
                    continue

                groups_dict["valid"].append(data[group_data]["urlname"])

                if load_events:
                    group_events: List[Event] = api_client.update_all_group_events(
                        group=group
                    )

                    event_counter = event_counter + len(group_events)

                    print(
                        "Group {} was updatet with {} events".format(
                            group.name, len(group_events)
                        )
                    )

                else:
                    print(
                        "Group {} was updatet without events".format(
                            group.name,
                        )
                    )

    print(
        "{} groups was updatet with {} new events & {} do not exists anymore".format(
            len(groups_dict["valid"]), event_counter, len(groups_dict["invalid"])
        )
    )

    return groups_dict
