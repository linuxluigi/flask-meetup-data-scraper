import pytest
from meetup_search.models import Group, Event
from time import sleep
from datetime import datetime

meetup_groups: dict = {
    "sandbox": {"meetup_id": 1556336, "urlname": "Meetup-API-Testing"},
    "not-exist": {"meetup_id": 123456, "urlname": "None"},
    "gone": {"meetup_id": 654321, "urlname": "connectedawareness-berlin"},
}


def test_group_get_or_create_by_urlname():
    # group content
    group_content: dict = {
        "urlname": "test_get_or_create_by_urlname",
        "meetup_id": 1234567,
    }

    # test with non exiting Group
    group_1: Group = Group.get_or_create_by_urlname(
        urlname=group_content["urlname"],
        meetup_id=0,
        created=datetime.now(),
        description="",
        name="",
        link="",
        lat=0,
        lon=0,
        members=0,
        status="",
        timezone="",
        visibility="",
    )
    sleep(1)

    # assert if request does not exist
    assert isinstance(group_1, Group)
    assert group_1.meetup_id == 0

    # test with exiting Group
    group_2 = Group(
        meetup_id=group_content["meetup_id"],
        urlname=group_content["urlname"],
        created=datetime.now(),
        description="",
        name="",
        link="",
        location=[0, 0],
        members=0,
        status="",
        timezone="",
        visibility="",
    )
    group_2.save()
    sleep(1)

    # assert if request does exist
    group_3: Group = Group.get_or_create_by_urlname(
        urlname=group_content["urlname"],
        meetup_id=0,
        created=datetime.now(),
        description="",
        name="",
        link="",
        lat=0,
        lon=0,
        members=0,
        status="",
        timezone="",
        visibility="",
    )
    assert isinstance(group_3, Group)
    assert group_3.urlname == group_content["urlname"]
    assert group_3.meetup_id == group_content["meetup_id"]


def test_group_add_event():
    # init group model
    group_1 = Group(
        meetup_id=0,
        urlname="group_add_event",
        created=datetime.now(),
        description="",
        name="",
        link="",
        location=[0, 0],
        members=0,
        status="",
        timezone="",
        visibility="",
    )
    group_1.save()

    # add 10 events & check if there was added
    for i in range(0, 10):
        event: Event = Event(
            meetup_id=str(i),
            created=datetime.now(),
            time=datetime.now(),
            name="",
            link="",
        )

        group_1.add_event(event=event)
        group_1.save()
        sleep(1)

        group_2: Group = Group.get_group(urlname=group_1.urlname)
        group_events: [Event] = group_2.events
        assert len(group_events) == i + 1
        assert isinstance(group_events[i], Event)
        assert group_events[i].meetup_id == str(i)


def test_group_add_events():
    # init group model
    group_1 = Group(
        meetup_id=0,
        urlname="group_add_events",
        created=datetime.now(),
        description="",
        name="",
        link="",
        location=[0, 0],
        members=0,
        status="",
        timezone="",
        visibility="",
    )
    group_1.save()

    # create 10 events
    events: [Event] = []
    for i in range(0, 10):
        event: Event = Event(
            meetup_id=str(i),
            created=datetime.now(),
            time=datetime.now(),
            name="",
            link="",
        )

        events.append(event)

    # add events to group
    group_1.add_events(events)
    group_1.save()
    sleep(1)

    # check if events was added
    group_2: Group = Group.get_group(urlname=group_1.urlname)
    group_events: [Event] = group_2.events
    assert len(group_events) == 10
    for event in group_events:
        assert isinstance(group_events[i], Event)
        assert group_events[i].meetup_id == str(i)


def test_group_event_exists():
    event_meetup_id: int = 1

    # init group models
    group_1 = Group(
        meetup_id=0,
        urlname="group_event_1",
        created=datetime.now(),
        description="",
        name="",
        link="",
        location=[0, 0],
        members=0,
        status="",
        timezone="",
        visibility="",
    )
    group_1.save()
    group_2 = Group(
        meetup_id=1,
        urlname="group_event_2",
        created=datetime.now(),
        description="",
        name="",
        link="",
        location=[0, 0],
        members=0,
        status="",
        timezone="",
        visibility="",
    )
    group_1.save()

    # init event
    search_event: Event = Event(
        meetup_id=0, created=datetime.now(), time=datetime.now(), name="", link=""
    )

    # test when event does not exists
    assert group_1.event_exists(event_meetup_id=search_event.meetup_id) is False

    # test with existing event
    group_1.add_event(search_event)
    group_1.save()
    assert group_1.event_exists(event_meetup_id=search_event.meetup_id) is True

    # test with saved event in wrong group
    assert group_2.event_exists(event_meetup_id=search_event.meetup_id) is False


def test_group_get_group():
    # init group model
    group_1 = Group(
        meetup_id=0,
        urlname="group_get",
        created=datetime.now(),
        description="",
        name="",
        link="",
        location=[0, 0],
        members=0,
        status="",
        timezone="",
        visibility="",
    )

    # check when there is no group
    assert Group.get_group(urlname=group_1.urlname) is None

    # save group
    group_1.save()
    sleep(1)

    # get group
    group_2: Group = Group.get_group(urlname=group_1.urlname)

    # check when there is a group
    assert isinstance(group_2, Group)
    assert group_2.urlname == group_1.urlname
    assert group_2.meetup_id == group_1.meetup_id
    assert group_2.created == group_1.created


def test_group_last_event_time():
    events: dict = {
        "first": {"meetup_id": "first", "time": datetime(year=2000, month=1, day=1),},
        "middle": {"meetup_id": "middle", "time": datetime(year=2010, month=1, day=1),},
        "last": {"meetup_id": "last", "time": datetime(year=2020, month=1, day=1),},
    }

    # init group models
    group = Group(
        meetup_id=10,
        urlname="group_event_2",
        created=datetime.now(),
        description="",
        name="",
        link="",
        location=[0, 0],
        members=0,
        status="",
        timezone="",
        visibility="",
    )
    group.save()

    # test with no event
    assert group.last_event_time is None

    # test with one event
    event_first: Event = Event(
        meetup_id=events["first"]["meetup_id"],
        time=events["first"]["time"],
        name="",
        link="",
    )
    group.add_event(event_first)
    group.save()
    assert group.last_event_time == events["first"]["time"]

    # test with 2 events
    event_last: Event = Event(
        meetup_id=events["last"]["meetup_id"],
        time=events["last"]["time"],
        name="",
        link="",
    )
    group.add_event(event_last)
    group.save()
    assert group.last_event_time == events["last"]["time"]

    # test with 3 events
    event_middle: Event = Event(
        meetup_id=events["middle"]["meetup_id"],
        time=events["middle"]["time"],
        name="",
        link="",
    )
    group.add_event(event_middle)
    group.save()
    assert group.last_event_time == events["last"]["time"]


def test_group_delete_if_exists():
    group = Group(
        meetup_id=20,
        urlname="group_delete_1",
        created=datetime.now(),
        description="",
        name="",
        link="",
        location=[0, 0],
        members=0,
        status="",
        timezone="",
        visibility="",
    )

    # check when there is no group
    assert Group.delete_if_exists(urlname=group.urlname) == False

    # save group
    group.save()
    sleep(1)

    # delete group
    assert Group.delete_if_exists(urlname=group.urlname) == True
    sleep(1)

    # check if group is really deleted
    assert Group.get_group(urlname=group.urlname) is None
