from datetime import datetime, timedelta
from meetup_search.models import Group, Event
from config.base import es
from elasticsearch_dsl import Search


def get_event_from_response(response: dict, group: Group) -> Event:
    """
    parse json response and return an Event

    Keyword arguments:
    response -- meetup api response in a dict

    return -> Event when not already exists
    """

    # if event page already exists, return None
    if group.event_exists(event_meetup_id=response["id"]):
        return

    date_in_series_pattern: bool = False
    if "date_in_series_pattern" in response:
        date_in_series_pattern = response["date_in_series_pattern"]

    event: Event = Event(
        meetup_id=response["id"],
        time=datetime.fromtimestamp(response["time"] / 1000),
        name=response["name"],
        link=response["link"],
        date_in_series_pattern=date_in_series_pattern,
    )

    # add optional fields
    if "attendance_count" in response:
        event.attendance_count = response["attendance_count"]
    if "attendance_sample" in response:
        event.attendance_sample = response["attendance_sample"]
    if "attendee_sample" in response:
        event.attendee_sample = response["attendee_sample"]
    if "created" in response:
        event.created = datetime.fromtimestamp(response["created"] / 1000)
    if "description" in response:
        event.description = response["description"]
    if "duration" in response:
        event.duration = response["duration"]
    # if "event_hosts" in response:
    #     event_hosts: [EventHost] = []
    #     for event_host in response["event_hosts"]:
    #         event_hosts.append(get_event_host_from_response(response=event_host))
    #     event.event_hosts = event_hosts
    # else:
    #     event.event_hosts = []
    if "fee" in response:
        event.fee_accepts = response["fee"]["accepts"]
        event.fee_amount = response["fee"]["amount"]
        event.fee_currency = response["fee"]["currency"]
        event.fee_description = response["fee"]["description"]
        event.fee_label = response["fee"]["label"]
    if "how_to_find_us" in response:
        event.how_to_find_us = response["how_to_find_us"]
    if "status" in response:
        event.status = response["status"]
    if "utc_offset" in response:
        event.utc_offset = response["utc_offset"] / 1000
    if "updated" in response:
        event.updated = datetime.fromtimestamp(response["updated"] / 1000)
    if "venue" in response:
        event = get_venue_from_response(response=response["venue"], event=event)
    if "venue_visibility" in response:
        event.venue_visibility = response["venue_visibility"]
    if "visibility" in response:
        event.visibility = response["visibility"]

    return event


def get_group_from_response(response: dict) -> Group:
    """
    parse json response and return an EventPage

    Keyword arguments:
    home_page -- HomePage parent of GroupPage

    return -> get or create Group based on urlname
    """

    group = Group.get_or_create_by_urlname(
        urlname=response["urlname"],
        meetup_id=response["id"],
        created=datetime.fromtimestamp(response["created"] / 1000),
        description=response["description"],
        name=response["name"],
        link=response["link"],
        lat=response["lat"],
        lon=response["lon"],
        members=response["members"],
        status=response["status"],
        timezone=response["timezone"],
        visibility=response["visibility"],
    )

    # add optional fields
    if "category" in response:
        group = get_category_from_response(response=response["category"], group=group)
    if "city" in response:
        group.city = response["city"]
    if "city_link" in response:
        group.city_link = response["city_link"]
    if "country" in response:
        group.country = response["country"]
    if "fee_options" in response:
        if "currencies" in response["fee_options"]:
            group.fee_options_currencies_code = response["fee_options"]["currencies"][
                "code"
            ]
            if "default" in response["fee_options"]["currencies"]:
                group.fee_options_currencies_default = response["fee_options"][
                    "currencies"
                ]["default"]
            else:
                group.fee_options_currencies_default = False
        if "type" in response["fee_options"]:
            group.fee_options_type = response["fee_options"]["type"]
    if "join_mode" in response:
        group.join_mode = response["join_mode"]
    if "join_mode" in response:
        group.join_mode = response["join_mode"]
    if "localized_country_name" in response:
        group.localized_country_name = response["localized_country_name"]
    if "localized_location" in response:
        group.localized_location = response["localized_location"]
    if "member_limit" in response:
        group.member_limit = response["member_limit"]
    # if "meta_category" in response:
    #     group.meta_category = get_meta_category_from_response(
    #         response=response["meta_category"]
    #     )
    # else:
    #     group.nominated_member = False
    if "nomination_acceptable" in response:
        group.nomination_acceptable = True
    else:
        group.nomination_acceptable = False
    if "organizer" in response:
        group = get_group_organizer_from_response(
            response=response["organizer"], group=group
        )
    if "short_link" in response:
        group.short_link = response["short_link"]
    if "state" in response:
        group.state = response["state"]
    if "status" in response:
        group.status = response["status"]
    # if "topics" in response:
    #     group.topics.clear()
    #     for topic in response["topics"]:
    #         group.topics.add(get_topic_from_response(response=topic))
    if "untranslated_city" in response:
        group.untranslated_city = response["untranslated_city"]
    if "welcome_message" in response:
        group.welcome_message = response["welcome_message"]
    if "who" in response:
        group.who = response["who"]

    group.save()
    return group


def get_group_organizer_from_response(response: dict, group: Group):
    """
    parse json response and return an Member

    Keyword arguments:
    response -- meetup api response in a dict

    return -> get or create Member
    """
    group.organizer_id = response["id"]

    # add optional fields
    if "name" in response:
        group.organizer_name = response["name"]
    if "bio" in response:
        group.organizer_bio = response["bio"]

    return group


def get_event_host_from_response(response: dict, event: Event) -> Event:
    """
    parse json response and return an EventHost

    Keyword arguments:
    response -- meetup api response in a dict

    return -> get unsaved EventHost
    """

    # add optional fields
    if "host_count" in response:
        event.event_host_host_count = response["host_count"]
    if "id" in response:
        event.event_host_id = response["id"]
    if "intro" in response:
        event.event_host_intro = response["intro"]
    if "join_date" in response:
        event.event_host_join_date = datetime.fromtimestamp(
            response["join_date"] / 1000
        )
    if "name" in response:
        event.event_host_name = response["name"]

    return event


def get_category_from_response(response: dict, group: Group) -> Group:
    """
    parse json response and return an Category

    Keyword arguments:
    response -- meetup api response in a dict

    return -> get or create Category
    """

    group.category_id = response["id"]

    if "name" in response:
        group.category_name = response["name"]
    if "shortname" in response:
        group.category_shortname = response["shortname"]
    if "sort_name" in response:
        group.category_sort_name = response["sort_name"]

    return group


# def get_topic_from_response(response: dict):
#     """
#     parse json response and return an Topic

#     Keyword arguments:
#     response -- meetup api response in a dict

#     return -> get or create Topic
#     """

#     try:
#         topic: Topic = Topic.objects.get(meetup_id=response["id"])
#     except Topic.DoesNotExist:
#         topic: Topic = Topic(
#             meetup_id=response["id"],
#             lang=response["lang"],
#             name=response["name"],
#             urlkey=response["urlkey"],
#         )

#     # update required fields
#     topic.lang = response["lang"]
#     topic.name = response["name"]
#     topic.urlkey = response["urlkey"]

#     topic.save()
#     return topic


def get_meta_category_from_response(response: dict, group: Group) -> Group:
    """
    parse json response and return an MetaCategory

    Keyword arguments:
    response -- meetup api response in a dict

    return -> get or create MetaCategory
    """

    # update required fields
    group.meta_category_id = response["id"]
    group.meta_category_name = response["name"]
    group.meta_category_shortname = response["shortname"]
    group.meta_category_sort_name = response["sort_name"]

    return group


def get_venue_from_response(response: dict, event: Event) -> Event:
    """
    parse json response and return an Venue

    Keyword arguments:
    response -- meetup api response in a dict

    return -> get or create Venue
    """

    if "address_1" in response:
        event.venue_address_1 = response["address_1"]
    if "address_2" in response:
        event.venue_address_2 = response["address_2"]
    if "address_3" in response:
        event.venue_address_3 = response["address_3"]
    if "city" in response:
        event.venue_city = response["city"]
    if "country" in response:
        event.venue_country = response["country"]
    if "lat" in response and "lon" in response:
        event.venue_location = [response["lat"], response["lon"]]
    if "localized_country_name" in response:
        event.venue_localized_country_name = response["localized_country_name"]
    if "name" in response:
        event.venue_name = response["name"]
    if "phone" in response:
        event.venue_phone = response["phone"]
    if "zip_code" in response:
        event.venue_zip_code = response["zip_code"]

    return event
