from meetup_search.commands.update_groups import update_groups
from typing import List
from time import sleep
from meetup_search.models import Group


def test_update_groups(group_1: Group):
    # init group to update
    group_1.urlname = "Meetup-API-Testing"
    group_1.save()
    sleep(2)

    # update all groups
    update_groups()
    sleep(2)

    # check if group was updated
    group_2: Group = Group.get_group(urlname=group_1.urlname)
    assert len(group_2.events) > 0
