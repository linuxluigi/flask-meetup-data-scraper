import pytest
from meetup_search.commands.get_group import get_group
from meetup_search.models import Group


def test_get_group(meetup_groups: dict):
    # test with exiting group
    group_1: Group = get_group(meetup_group_urlname=meetup_groups["sandbox"]["urlname"])

    assert isinstance(group_1, Group)
    assert group_1.urlname == meetup_groups["sandbox"]["urlname"]
    assert len(group_1.events) > 0

    # test with not-exist group
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        get_group(meetup_group_urlname=meetup_groups["not-exist"]["urlname"])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    # test with gone group
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        get_group(meetup_group_urlname=meetup_groups["gone"]["urlname"])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
