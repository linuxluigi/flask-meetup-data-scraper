from typing import List, Optional

import click
from flask.cli import with_appcontext
from meetup_search.meetup_api_client.exceptions import (
    GroupDoesNotExistsOnMeetup,
    MeetupConnectionError,
)
from meetup_search.meetup_api_client.meetup_api_client import MeetupApiClient
from meetup_search.models.group import Event, Group


@click.command(name="get_group")
@with_appcontext
@click.option("--sandbox", nargs=1, type=bool)
@click.argument(
    "meetup_group_urlname", type=str, required=False,
)
def get_group(
    meetup_group_urlname: Optional[str] = None, sandbox: bool = False
) -> Group:
    """
    Load single Meetupgroup from Meetup REST API into elasticsearch

    Arguments:
        meetup_group_urlname {str} -- meetup group urlname to load the group from meetup

    Returns:
        Group -- updated group from meetup.com
    """
    if sandbox:
        meetup_group_urlname = "Meetup-API-Testing"

    if not meetup_group_urlname:
        print("No meetup_group_urlname was given!")
        exit(1)

    api_client: MeetupApiClient = MeetupApiClient()

    try:
        group: Group = api_client.get_group(meetup_group_urlname)
    except (GroupDoesNotExistsOnMeetup, MeetupConnectionError) as e:
        print(e)
        exit(2)

    group_events: List[Event] = api_client.update_all_group_events(group=group)

    print("Group {} was updatet with {} events".format(group.name, len(group_events)))

    return group
