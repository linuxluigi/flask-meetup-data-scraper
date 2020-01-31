from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from elasticsearch_dsl import Boolean, Date, Document, GeoPoint, InnerDoc, Integer, Long, Nested, Text
from elasticsearch_dsl.field import Completion
from elasticsearch_dsl.response import Response
from elasticsearch_dsl.search import Search
from meetup_search.meetup_api_client.exceptions import GroupDoesNotExists


class Topic(InnerDoc):
    """
    Meetup Group Topic
    """

    # required fields
    meetup_id = Text(required=True)
    lang = Text(required=True)
    name = Text(required=True)
    urlkey = Text(required=True)


class Event(InnerDoc):
    """
    Meetup Group Event
    """

    # required fields
    meetup_id = Text(required=True)
    time = Date(required=True)
    name = Text(required=True)
    link = Text(required=True)
    date_in_series_pattern = Boolean(required=True)

    # optional fields
    attendance_count = Integer()
    attendance_sample = Integer()
    attendee_sample = Integer()
    created = Date()
    description = Text()
    duration = Long()
    fee_accepts = Text()
    fee_amount = Integer()
    fee_currency = Text()
    fee_description = Text()
    fee_label = Text()
    how_to_find_us = Text()
    status = Text()
    updated = Date()
    utc_offset = Long()
    venue_visibility = Text()
    visibility = Text()

    # venue
    venue_address_1 = Text()
    venue_address_2 = Text()
    venue_address_3 = Text()
    venue_city = Text()
    venue_country = Text()
    venue_localized_country_name = Text()
    venue_name = Text()
    venue_phone = Text()
    venue_zip_code = Text()
    venue_location = GeoPoint()

    # event hosts
    event_host_host_count = Integer()
    event_host_id = Integer()
    event_host_intro = Text()
    event_host_join_date = Date()
    event_host_name = Text()


class Group(Document):
    """
    Meetup.com Group Model with elasticsearch persistence

    Meetup Group doc:
    https://meetup.com/de-DE/meetup_api/docs/:urlname/?uri=%2Fmeetup_api%2Fdocs%2F%3Aurlname%2F#get

    Elasticsearch persistence doc ->
    https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html#persistence

    Raises:
        GroupDoesNotExists: Raise when request a group wich does not exists on elasticsearch or on meetup
    """

    class Index:
        """
        Elasticsearch index of the model

        for override the default index ->
        https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html#document-life-cycle
        """

        name = "meetup_group"

    # required fields
    meetup_id = Long(required=True)
    urlname = Text(required=True)
    created = Date(default_timezone="UTC", required=True)
    description = Text(analyzer="snowball", required=True)
    name = Text(required=True)
    link = Text(required=True)
    location = GeoPoint(required=True)
    members = Integer(required=True)
    status = Text(required=True)
    timezone = Text(required=True)
    visibility = Text(required=True)

    # optional fields
    nomination_acceptable = Boolean()
    city = Text()
    city_link = Text()
    country = Text()
    fee_options_currencies_code = Text()
    fee_options_currencies_default = Boolean()
    fee_options_type = Text()
    join_mode = Text()
    localized_country_name = Text()
    localized_location = Text()
    member_limit = Integer()
    short_link = Text()
    state = Text()
    untranslated_city = Text()
    welcome_message = Text()
    who = Text()

    # category
    category_id = Long()
    category_name = Text()
    category_shortname = Text()
    category_sort_name = Text()

    # meta_category
    meta_category_id = Long()
    meta_category_shortname = Text()
    meta_category_name = Text()
    meta_category_sort_name = Text()

    # topics
    topics = Nested(Topic)

    # organizer
    organizer_id = Integer()
    organizer_name = Text()
    organizer_bio = Text()

    # events
    events = Nested(Event)

    # suggest fields (auto fill on save)
    name_suggest = Completion()

    def add_event(self, event: Event):
        """
        Add a single event object to the group.

        Arguments:
            event {Event} -- Event wich should be added
        """
        self.events.append(event)

    def add_topic(self, topic: Topic):
        """
        Add a single topic object to the group.

        Arguments:
            topic {Topic} -- Topic wich should be added
        """
        self.topics.append(topic)

    def add_events(self, events: List[Event]):
        """
        Add a mutiple event objects to the group.

        Arguments:
            events {List[Event]} -- Event list wich should be added
        """
        self.events.extend(events)

    def event_exists(self, event_meetup_id: str) -> bool:
        """
        Check if a event with the meetup_id exists in this group on elasticsearch

        Arguments:
            event_meetup_id {str} -- meetup_id of the requested event

        Returns:
            bool -- True -> Event exists; False -> Event does not exists
        """
        for event in self.events:
            if event.meetup_id == event_meetup_id:
                return True
        return False

    def save(self, **kwargs):
        """
        Overwrite save method to set suggest fields
        """
        self.name_suggest = self.name

        return super().save(**kwargs)

    @property
    def last_event_time(self) -> Optional[datetime]:
        """
        Get from the last event the event time, if any event exists

        Usage:
            group: Group = Group(...)

            group.last_event_time

        Returns:
            Optional[datetime] -- Last event time, when any event exists in this group else return
                                  None
        """
        last_event_time: Optional[datetime] = None
        for event in self.events:
            if last_event_time:
                if event.time > last_event_time:
                    last_event_time = event.time
            else:
                last_event_time = event.time
        return last_event_time

    @staticmethod
    def delete_if_exists(urlname: str) -> bool:
        """
        Delete a group based on the urlname if exists.

        Usage:
            Group.delete_if_exists(urlname="MyGroupToDelete)

        Arguments:
            urlname {str} -- The Group URL name

        Returns:
            bool -- True -> Group was deletet; False -> Group doesn't exists on elasticsearch
        """
        try:
            group: Group = Group.get_group(urlname)
            group.delete()
            return True
        except GroupDoesNotExists:
            return False

    @staticmethod
    def get_group(urlname: str) -> Group:
        """
        Get Group from elasticseach based on urlname

        Arguments:
            urlname {str} -- Group urlname

        Raises:
            GroupDoesNotExists: When a Group does not exists on elasticsearch

        Returns:
            Group -- the request Group object from elasticsearch
        """
        s: Search = Group.search()
        s = s.query("match", urlname=urlname)
        results: Response = s.execute()
        for group in results:
            return group
        raise GroupDoesNotExists("{} does not exists in elasticsearch!".format(urlname))

    @staticmethod
    def get_or_create_by_urlname(
        urlname: str,
        meetup_id: int,
        created: datetime,
        description: str,
        name: str,
        link: str,
        lat: float,
        lon: float,
        members: int,
        status: str,
        timezone: str,
        visibility: str,
    ) -> Group:
        """
        Get a Group Object from elasticsearch based on the urlname and update the Group Object
        with all arguments.

        When the Group does not exists on elasticsearch, create a new Group Object with all
        arguments.

        Arguments:
            urlname {str} -- Meetup Group urlname
            meetup_id {int} -- Meetup Group id 
            created {datetime} -- create time of the Meetup Group
            description {str} -- Meetup Group description
            name {str} -- Meetup Group name
            link {str} -- link to the Group Meetup URL
            lat {float} -- Meetup Group location lat
            lon {float} -- Meetup Group location lon
            members {int} -- Meetup Group members amount
            status {str} -- Meetup Group status
            timezone {str} -- Meetup Group timezone
            visibility {str} -- Meetup Group visibility

        Returns:
            Group -- Updated or new Group Object from elasticsearch
        """

        s: Search = Group.search()
        s = s.query("match", urlname=urlname)
        results: Response = s.execute()

        for group in results:
            group.description = description
            group.name = name
            group.location = {"lat": lat, "lon": lon}
            group.members = members
            group.status = status
            group.timezone = timezone
            group.visibility = visibility
            group.save()
            return group

        return Group(
            urlname=urlname,
            meetup_id=meetup_id,
            created=created,
            description=description,
            name=name,
            link=link,
            location={"lat": lat, "lon": lon},
            members=members,
            status=status,
            timezone=timezone,
            visibility=visibility,
        )

    @staticmethod
    def get_all_groups() -> List[Group]:
        """
        Get all groups from Elasticsearch

        Raises:
            GroupDoesNotExists: When a Group does not exists on elasticsearch

        Returns:
            List[Group] -- all groups from elasticsearch
        """
        s: Search = Group.search()
        s = s.query("match_all")
        results: Response = s.execute()

        groups: List[Group] = []
        for group in results:
            groups.append(group)

        return groups

    @staticmethod
    def add_event_venue_to_list(venue_list: List[dict], event: Event) -> List[dict]:
        """
        add venue to dict, if it wasn't already included

        Arguments:
            venue_list: List[dict] -- list of venue dicts
            event {Event} -- event to add

        Returns:
            List[dict] -- input venue_list with added event venue
        """

        # check if there is no venue information in event
        if not event.venue_location or not event.venue_name:
            return venue_list

        # exit method if venue already exists
        for venue in venue_list:
            if venue["location"] == event.venue_location:
                return venue_list

        event_dict: dict = event.to_dict()

        # append venue if it does not exists
        venue_list.append(
            {
                "name": event_dict["venue_name"],
                "location": event_dict["venue_location"],
            }
        )

        return venue_list

    @staticmethod
    def get_venue_location_average(venue_list: List[dict]) -> dict:
        """
        Calc the average location of all venues

        Arguments:
            venue_list {List[dict]} -- venue list for calc the average

        Returns:
            dict -- {'lat': float, 'lon': float}
        """

        if len(venue_list) == 0:
            raise ValueError("The size of venue_list need to be larger than 0!")

        lat_average: float = 0
        lon_average: float = 0

        for venue in venue_list:
            lat_average = lat_average + venue["location"]["lat"]
            lon_average = lon_average + venue["location"]["lon"]

        lat_average = lat_average / len(venue_list)
        lon_average = lon_average / len(venue_list)

        return {"lat": lat_average, "lon": lon_average}

    def to_json_dict(self, load_events: bool) -> dict:
        """
        Convert to_dict into a JSON serializable dict object.
        Also add a venue dict to the group, for each venue that was used by that group in any event.

        Arguments:
            load_events {bool} -- load events into dict

        Returns:
            dict -- JSON serializable dict object
        """

        group_dict: dict = self.to_dict()

        # set group venue
        group_dict["venues"] = []
        for event in self.events:
            group_dict["venues"] = self.add_event_venue_to_list(
                group_dict["venues"], event
            )

        if len(group_dict["venues"]) > 0:
            group_dict["venue_location_average"] = self.get_venue_location_average(
                group_dict["venues"]
            )

        for field in group_dict:

            if "events" in group_dict:
                for event_dict in group_dict["events"]:

                    # load events into dict
                    if load_events:
                        for event_field in event_dict:
                            # todo remove double events to reduce bandwith
                            if isinstance(event_dict[event_field], datetime):
                                event_dict[event_field] = event_dict[
                                    event_field
                                ].strftime("%Y-%m-%dT%H:%M:%S%z")
                    else:
                        group_dict["events"] = []

            if isinstance(group_dict[field], datetime):
                group_dict[field] = group_dict[field].strftime("%Y-%m-%dT%H:%M:%S%z")

        return group_dict
