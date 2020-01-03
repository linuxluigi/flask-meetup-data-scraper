import requests
import time
from requests.models import Response
import pytz
from .exceptions import (
    HttpNoSuccess,
    HttpNotFoundError,
    HttpNotAccessibleError,
    HttpNoXRateLimitHeader,
)
from meetup_search.models import Group, Event
from meetup_search.meetup_api_client.json_parser import (
    get_event_from_response,
    get_group_from_response,
)
from datetime import datetime
from meetup_search.meetup_api_client.exceptions import (
    EventAlreadyExists,
    GroupDoesNotExists,
    GroupDoesNotExistsOnMeetup,
    MeetupConnectionError,
)
from time import sleep
from typing import List, Optional


class RateLimit:
    """
    meetup api rate limit, wait for new request if needed
    
    Raises:
        HttpNoXRateLimitHeader: Raise when HTTP response has no XRateLimitHeader
    """
    

    def __init__(self):
        """
        init default values for meetup XRateLimitHeaders
        """

        # The maximum number of requests that can be made in a window of time
        self.limit: int = 0

        # The remaining number of requests allowed in the current rate limit window
        self.remaining: int = 0

        # The number of seconds until the current rate limit window resets
        self.reset: int = 0

        # unixtime when limits will be reseted
        self.reset_time: float = time.time()

    def wait_for_next_request(self) -> None:
        """
        wait for next request, if needed
        """
        if not self.reset_time:
            return

        if self.remaining < 1:
            while self.reset_time > time.time():
                time.sleep(1)

    def update_rate_limit(self, response: Response, reset_time: int):
        """
        Update rate limit information from response header
        
        Arguments:
            response {Response} -- http response
            reset_time {int} -- wait time in secounds
        
        Raises:
            HttpNoXRateLimitHeader: Raise when HTTP response has no XRateLimitHeader
        """
        self.limit = int(response.headers.get("X-RateLimit-Limit", -1))
        self.remaining = int(response.headers.get("X-RateLimit-Remaining", -1))
        self.reset = int(response.headers.get("X-RateLimit-Reset", -1))
        self.reset_time = time.time() + self.reset

        if self.limit < 0 or self.remaining < 0 or self.reset_time < 0:
            self.limit = 0
            self.remaining = 0
            self.reset = reset_time
            self.reset_time = time.time() + self.reset
            raise HttpNoXRateLimitHeader("There is no XRateLimit Header!")


class MeetupApiClient:
    """
    meetup api client only for groups & events
    """

    def __init__(self):
        """
        set rate limits & meetup api url
        """
        self.rate_limit = RateLimit()

        # meetup apir url
        self.base_url: str = "https://api.meetup.com/"

    def get(
        self, url_path: str, retry: int = 0, max_retry=3, reset_time: int = 60
    ) -> dict:
        """
        meetup http request on the url_path
        
        Arguments:
            url_path {str} -- url path without domain example for url https://api.meetup.com/find/groups is the url_path find/groups
        
        Keyword Arguments:
            retry {int} -- how many times try to get the same url (default: {0})
            max_retry {int} -- max retries bevor raise an error (default: {3})
            reset_time {int} -- wait time in secounds (default: {60})
        
        Raises:
            HttpNotFoundError: When get a 404 or 400 Error on the Meetup API
            HttpNotAccessibleError: When get a 410 (gone) Error on the Meetup API
            HttpNoSuccess: When get a HTTP Error (every error without 400, 404 & 410) on the Meetup API 
            HttpNoXRateLimitHeader: Raise when HTTP response has no XRateLimitHeader
        
        Returns:
            dict -- json as python dict
        """
        self.rate_limit.wait_for_next_request()

        url: str = "{}{}".format(self.base_url, url_path)
        response: Response = requests.get(url)

        if response.status_code == 404:
            raise HttpNotFoundError
        if response.status_code == 410:
            raise HttpNotAccessibleError
        if response.status_code != 200:
            if retry >= max_retry:
                raise HttpNoSuccess
            else:
                return self.get(url_path=url_path, retry=retry + 1)

        try:
            self.rate_limit.update_rate_limit(response=response, reset_time=reset_time)
        except HttpNoXRateLimitHeader:
            if retry >= max_retry:
                raise HttpNoXRateLimitHeader("There is no XRateLimit Header!")
            else:
                return self.get(url_path=url_path, retry=retry + 1)

        return response.json()

    def get_group(self, group_urlname: str) -> Group:
        """
        get or create a Group based on the group_urlname and fill / update the object from meetup rest api
        
        Arguments:
            group_urlname {str} -- Meetup group the urlname as string
        
        Raises:
            GroupDoesNotExistsOnMeetup: Group does not exists on Meetup.com
            MeetupConnectionError: Some network error to meetup.com
        
        Returns:
            Group -- Group based on the group_urlname
        """
        try:
            response: dict = self.get("{}".format(group_urlname))
        except (HttpNotAccessibleError, HttpNotFoundError) as e:
            # delete group if exists
            Group.delete_if_exists(urlname=group_urlname)
            raise GroupDoesNotExistsOnMeetup(
                "{} group does not exists on meetup.com!".format(group_urlname)
            )

        except (HttpNoXRateLimitHeader) as e:
            raise MeetupConnectionError(
                "Could not connect to meetup -> Rate Limits reached for {}!".format(
                    group_urlname
                )
            )
        except (HttpNoSuccess) as e:
            raise MeetupConnectionError(
                "Could not connect to meetup -> network problems for {}".format(
                    group_urlname
                )
            )

        group: Group = get_group_from_response(response=response)
        group.save()

        return group

    def update_all_group_events(
        self, group: Group, max_entries_per_page: int = 200
    ) -> List[Event]:
        """
        get all past events from meetup rest api & add it as child pages to the group
        
        Arguments:
            group {Group} -- Group to update
        
        Keyword Arguments:
            max_entries_per_page {int} -- How many events should be requestst at once on meetup (between 1 to 200) (default: {200})
        
        Returns:
            List[Event] -- List[Event] every new Events wich wasn't already in elasticsearch
        """

        # return [Event], init empty
        events: List[Event] = []

        # fetch all events
        while True:
            group_events: List[Event] = self.update_group_events(
                group=group, max_entries=max_entries_per_page
            )
            group.add_events(events=group_events)
            group.save()
            # todo replace sleep with wait for save done
            sleep(1)
            events.extend(group_events)
            if len(group_events) == 0:
                break

        return events

    def update_group_events(self, group: Group, max_entries: int = 200) -> List[Event]:
        """
        get new past events from meetup rest api & add it as child pages to the group

        Keyword arguments:
        group -- GroupPage
        max_entries_per_page -- how much events get from the meetup rest api per request (default 200, min 1, max 200)

        return -> [Event] new Events wich are not the database from the request
        """

        # get last event time from group
        last_event_time: Optional[datetime] = group.last_event_time

        # return [Event], init empty
        events: List[Event] = []

        # when there is a last_event_time -> set on meetup that only events fetch wich are no ealier than this event

        try:
            response: dict = {}
            if last_event_time:
                response = self.get(
                    "{}/events?status=past&no_earlier_than={}&page={}".format(
                        group.urlname,
                        last_event_time.strftime("%Y-%m-%d"),
                        self.get_max_entries(max_entries=max_entries),
                    )
                )
            else:
                response = self.get(
                    "{}/events?status=past&page={}".format(
                        group.urlname, self.get_max_entries(max_entries=max_entries)
                    )
                )
        except (
            HttpNotFoundError,
            HttpNotAccessibleError,
            HttpNoSuccess,
            HttpNoXRateLimitHeader,
        ) as e:
            print(e)
            return events

        # go through every event from response and at them to the database
        for event_response in response:
            try:
                event: Event = get_event_from_response(
                    response=event_response, group=group
                )
                events.append(event)
            except EventAlreadyExists:
                pass

        return events

    def get_max_entries(self, max_entries: int) -> int:
        """
        Set the max entries from a meetup request between 1 and 200
        
        Arguments:
            max_entries {int} -- max_entries wich should be limit between 1 to 200
        
        Returns:
            int -- valid value for max_entries
        """
        if max_entries < 1:
            return 1
        if max_entries > 200:
            return 200
        return max_entries
