from typing import List

import click
from flask.cli import with_appcontext
from meetup_search.meetup_api_client.meetup_api_client import MeetupApiClient
from meetup_search.models.group import Group


@click.command(name="update_groups")
@with_appcontext
def update_groups() -> None:
    """
    update for all groups new events
    """
    # get all groups
    groups: List[Group] = Group.get_all_groups()

    # init api client
    api_client: MeetupApiClient = MeetupApiClient()

    # update all groups
    for group in groups:
        api_client.update_all_group_events(group=group)
