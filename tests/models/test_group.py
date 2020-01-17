import pytest
from meetup_search.models.group import Event, Group, Topic
from time import sleep
from datetime import datetime
from typing import List
from meetup_search.meetup_api_client.exceptions import GroupDoesNotExists


def test_group_get_or_create_by_urlname(group_2: Group):
    # test with non exiting Group
    group_1: Group = Group.get_or_create_by_urlname(
        urlname=group_2.urlname,
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
    group_2.save()
    sleep(1)

    # assert if request does exist
    group_3: Group = Group.get_or_create_by_urlname(
        urlname=group_2.urlname,
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
    assert group_3.urlname == group_2.urlname
    assert group_3.meetup_id == group_2.meetup_id


def test_group_add_event(group_1: Group):
    # init group model
    group_1.save()

    # add 10 events & check if there was added
    for i in range(0, 10):
        event: Event = Event(
            meetup_id=str(i),
            created=datetime.now(),
            time=datetime.now(),
            name="",
            link="",
            date_in_series_pattern=False,
        )

        group_1.add_event(event=event)
        group_1.save()
        sleep(1)

        group_2: Group = Group.get_group(urlname=group_1.urlname)
        group_events: List[Event] = group_2.events
        assert len(group_events) == i + 1
        assert isinstance(group_events[i], Event)
        assert group_events[i].meetup_id == str(i)


def test_group_add_events(group_1: Group):
    # init group model
    group_1.save()

    # create 10 events
    events: List[Event] = []
    for i in range(0, 10):
        event: Event = Event(
            meetup_id=str(i),
            created=datetime.now(),
            time=datetime.now(),
            name="",
            link="",
            date_in_series_pattern=False,
        )

        events.append(event)

    # add events to group
    group_1.add_events(events)
    group_1.save()
    sleep(1)

    # check if events was added
    group_2: Group = Group.get_group(urlname=group_1.urlname)
    group_events: List[Event] = group_2.events
    assert len(group_events) == 10
    for event in group_events:
        assert isinstance(group_events[i], Event)
        assert group_events[i].meetup_id == str(i)


def test_group_event_exists(group_1: Group, group_2: Group):
    # init group models
    group_1.save()
    group_2.save()

    # init event
    search_event: Event = Event(
        meetup_id=0,
        created=datetime.now(),
        time=datetime.now(),
        name="",
        link="",
        date_in_series_pattern=False,
    )

    # test when event does not exists
    assert group_1.event_exists(event_meetup_id=search_event.meetup_id) is False

    # test with existing event
    group_1.add_event(search_event)
    group_1.save()
    assert group_1.event_exists(event_meetup_id=search_event.meetup_id) is True

    # test with saved event in wrong group
    assert group_2.event_exists(event_meetup_id=search_event.meetup_id) is False


def test_group_get_group(group_1: Group):
    # check when there is no group
    with pytest.raises(GroupDoesNotExists):
        Group.get_group(urlname=group_1.urlname)

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


def test_group_last_event_time(group_1: Group):
    events: dict = {
        "first": {"meetup_id": "first", "time": datetime(year=2000, month=1, day=1), },
        "middle": {"meetup_id": "middle", "time": datetime(year=2010, month=1, day=1), },
        "last": {"meetup_id": "last", "time": datetime(year=2020, month=1, day=1), },
    }

    # init group models
    group_1.save()

    # test with no event
    assert group_1.last_event_time is None

    # test with one event
    event_first: Event = Event(
        meetup_id=events["first"]["meetup_id"],
        time=events["first"]["time"],
        name="",
        link="",
        date_in_series_pattern=False,
    )
    group_1.add_event(event_first)
    group_1.save()
    assert group_1.last_event_time == events["first"]["time"]

    # test with 2 events
    event_last: Event = Event(
        meetup_id=events["last"]["meetup_id"],
        time=events["last"]["time"],
        name="",
        link="",
        date_in_series_pattern=False,
    )
    group_1.add_event(event_last)
    group_1.save()
    assert group_1.last_event_time == events["last"]["time"]

    # test with 3 events
    event_middle: Event = Event(
        meetup_id=events["middle"]["meetup_id"],
        time=events["middle"]["time"],
        name="",
        link="",
        date_in_series_pattern=False,
    )
    group_1.add_event(event_middle)
    group_1.save()
    assert group_1.last_event_time == events["last"]["time"]


def test_group_delete_if_exists(group_1: Group):
    # check when there is no group
    assert Group.delete_if_exists(urlname=group_1.urlname) is False

    # save group
    group_1.save()
    sleep(1)

    # delete group
    assert Group.delete_if_exists(urlname=group_1.urlname) is True
    sleep(1)

    # check if group is really deleted
    with pytest.raises(GroupDoesNotExists):
        Group.get_group(urlname=group_1.urlname)


def test_group_add_topic(group_1: Group):
    # init group model
    group_1.save()

    # add 10 topics & check if there was added
    for i in range(0, 10):
        topic: Topic = Topic(meetup_id=str(i), lang=str(i), name=str(i), urlkey=str(i))

        group_1.add_topic(topic=topic)
        group_1.save()
        sleep(1)

        group_2: Group = Group.get_group(urlname=group_1.urlname)
        group_topics: List[Topic] = group_2.topics
        assert len(group_topics) == i + 1
        assert isinstance(group_topics[i], Topic)
        assert group_topics[i].meetup_id == str(i)


def test_get_all_groups(group_1: Group, group_2: Group):
    # test with no group in es
    groups_1: List[Group] = Group.get_all_groups()
    assert len(groups_1) == 0

    # init groups
    group_1.save()
    group_2.save()
    sleep(1)

    # test with 2 group in es
    groups_2: List[Group] = Group.get_all_groups()
    assert len(groups_2) == 2
    assert isinstance(groups_2[0], Group)


def test_add_event_venue_to_list():
    event: Event = Event(
        meetup_id=0,
        created=datetime.now(),
        time=datetime.now(),
        name="",
        link="",
        date_in_series_pattern=False,
    )

    # check with event without venue
    venue_list_1: List[dict] = Group.add_event_venue_to_list(venue_list=[], event=event)
    assert len(venue_list_1) == 0

    # add venue to event
    event.venue_name = 'Café'
    event.venue_location = [52.520008, 13.404954]

    # check with any previous event
    venue_list_2: List[dict] = Group.add_event_venue_to_list(venue_list=venue_list_1, event=event)
    assert len(venue_list_2) == 1

    # add again the same event
    venue_list_3: List[dict] = Group.add_event_venue_to_list(venue_list=venue_list_2, event=event)
    assert len(venue_list_3) == 1

    # add a different event
    event.venue_location = [51.050407, 13.737262]
    venue_list_4: List[dict] = Group.add_event_venue_to_list(venue_list=venue_list_3, event=event)
    assert len(venue_list_4) == 2


def test_get_venue_location_average():
    # test with empty venue arry
    with pytest.raises(ValueError):
        Group.get_venue_location_average(venue_list=[])

    # test average with a single event
    venue_list: List[dict] = [{'location': {'lat': 10, 'lon': 10}}]

    venue_average_1: dict = Group.get_venue_location_average(venue_list=venue_list)
    assert venue_average_1['lat'] == 10
    assert venue_average_1['lon'] == 10

    # test with mmutiple venues
    venue_list.append({'location': {'lat': 20, 'lon': 20}})
    venue_list.append({'location': {'lat': 30, 'lon': 30}})
    venue_list.append({'location': {'lat': 40, 'lon': 40}})
    venue_list.append({'location': {'lat': 50, 'lon': 50}})

    venue_average_2: dict = Group.get_venue_location_average(venue_list=venue_list)
    assert venue_average_2['lat'] == 30
    assert venue_average_2['lon'] == 30


def test_to_json_dict(group_1: Group):
    # add datetime element
    group_1.created = datetime.now()

    # test with no event
    assert isinstance(group_1.to_json_dict(load_events=True), dict)

    # check if an empty venue array was added
    assert len(group_1.to_json_dict(load_events=True)['venues']) == 0

    # check if venue_location_average is not set
    assert "venue_location_average" not in group_1.to_json_dict(load_events=True)

    # add event to group
    event: Event = Event(
        meetup_id=0,
        created=datetime.now(),
        time=datetime.now(),
        name="",
        link="",
        date_in_series_pattern=False,
        venue_name='Café',
        venue_location={'lat': 52.520008, 'lon': 13.404954},
    )
    group_1.add_event(event=event)

    # test with event
    assert isinstance(group_1.to_json_dict(load_events=True), dict)

    # check if the venue array was added with loaded groups
    assert len(group_1.to_json_dict(load_events=True)['venues']) == 1

    # check if events are in dict
    assert len(group_1.to_json_dict(load_events=True)['events']) == 1

    # check if events not included in dict
    assert len(group_1.to_json_dict(load_events=False)['events']) == 0

    # check if the venue array was added without loaded groups
    assert len(group_1.to_json_dict(load_events=True)['venues']) == 1

    # check if venue_location_average is set
    assert group_1.to_json_dict(load_events=True)['venue_location_average']['lat'] == event.venue_location['lat']
    assert group_1.to_json_dict(load_events=True)['venue_location_average']['lon'] == event.venue_location['lon']
