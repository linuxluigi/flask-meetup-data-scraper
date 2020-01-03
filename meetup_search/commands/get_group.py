from meetup_search.meetup_api_client.meetup_api_client import MeetupApiClient
from meetup_search.models import Group
from meetup_search.meetup_api_client.exceptions import (
    GroupDoesNotExistsOnMeetup,
    MeetupConnectionError,
)


def get_group(meetup_group_urlname: str) -> Group:
    """
    Load single Meetupgroup from Meetup REST API into elasticsearch

    Arguments:
        meetup_group_urlname {str} -- meetup group urlname to load the group from meetup

    Returns:
        Group -- updated group from meetup.com
    """
    api_client: MeetupApiClient = MeetupApiClient()

    try:
        group: Group = api_client.get_group(meetup_group_urlname)
    except (GroupDoesNotExistsOnMeetup, MeetupConnectionError) as e:
        print(e)
        exit(1)

    group_events: List[Event] = api_client.update_all_group_events(group=group)

    print("Group {} was updatet with {} events".format(group.name, len(group_events)))

    return group
