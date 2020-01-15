from meetup_search.commands.get_groups import get_groups
from typing import List, Dict
from meetup_search.models import Group
from time import sleep


def test_get_groups_with_events():
    # load all groups from JSON test file
    groups_dict: Dict[str, List[str]] = get_groups(
        meetup_files_path="/app/compose/local/flask/meetup_groups",
        load_events=True
    )

    assert len(groups_dict["valid"]) == 1
    assert len(groups_dict["invalid"]) == 2

    sleep(1)

    # load group
    group: Group = Group.get_group(urlname=groups_dict["valid"][0])

    # check if group has events
    assert len(group.events) > 0


def test_get_groups_without_events():
    # load all groups from JSON test file
    groups_dict: Dict[str, List[str]] = get_groups(
        meetup_files_path="/app/compose/local/flask/meetup_groups",
        load_events=False
    )

    assert len(groups_dict["valid"]) == 1
    assert len(groups_dict["invalid"]) == 2

    sleep(1)

    # load group
    group: Group = Group.get_group(urlname=groups_dict["valid"][0])

    # check if group has no events
    assert len(group.events) == 0
