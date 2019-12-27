from __future__ import annotations

from datetime import datetime
from elasticsearch_dsl import (
    Nested,
    Document,
    Date,
    Integer,
    Long,
    Keyword,
    Text,
    connections,
    GeoPoint,
    Boolean,
    InnerDoc,
)
from elasticsearch_dsl.search import Search
from elasticsearch_dsl.response import Response


class Topic(InnerDoc):
    # required fields
    meetup_id = Text(required=True)
    lang = Text(required=True)
    name = Text(required=True)
    urlkey = Text(required=True)


class Event(InnerDoc):
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
    class Index:
        name = "meetup_group"

    # required fields
    meetup_id = Long(required=True)
    urlname = Text(required=True)
    created = Date(default_timezone="UTC", required=True)
    description = Text(analyzer="snowball", required=True)
    name = Text(required=True)
    link = Text(required=True)
    # https://stackoverflow.com/questions/37099899/geopoint-field-type-in-elasticsearch-dsl-py
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

    def add_event(self, event: Event):
        self.events.append(event)

    def add_topic(self, topic: Topic):
        self.topics.append(topic)

    def add_events(self, events: [Event]):
        self.events.extend(events)

    def event_exists(self, event_meetup_id: str) -> bool:
        for event in self.events:
            if event.meetup_id == event_meetup_id:
                return True
        return False

    @property
    def last_event_time(self) -> datetime:
        last_event_time: datetime = None
        for event in self.events:
            if last_event_time:
                if event.time > last_event_time:
                    last_event_time = event.time
            else:
                last_event_time = event.time
        return last_event_time

    @staticmethod
    def delete_if_exists(urlname: str) -> bool:
        group: Group = Group.get_group(urlname)
        if group:
            group.delete()
            return True
        return False

    @staticmethod
    def get_group(urlname: str) -> Group:
        s: Search = Group.search()
        s = s.query("match", urlname=urlname)
        results: Response = s.execute()
        for group in results:
            return group

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

        s: Search = Group.search()
        s = s.query("match", urlname=urlname)
        results: Response = s.execute()

        for group in results:
            group.description = description
            group.name = name
            group.name = name
            group.location = [lat, lon]
            group.members = members
            group.status = status
            group.timezone = timezone
            group.visibility = visibility
            return group

        return Group(
            urlname=urlname,
            meetup_id=meetup_id,
            created=created,
            description=description,
            name=name,
            link=link,
            location=[lat, lon],
            members=members,
            status=status,
            timezone=timezone,
            visibility=visibility,
        )
