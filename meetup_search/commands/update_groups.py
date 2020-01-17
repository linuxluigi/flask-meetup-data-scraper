from meetup_search.models.group import Group
from typing import List
from meetup_search.meetup_api_client.meetup_api_client import MeetupApiClient


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
