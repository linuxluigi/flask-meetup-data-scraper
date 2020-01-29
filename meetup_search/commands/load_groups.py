from time import sleep
from typing import List

import click
from flask.cli import with_appcontext

from environs import Env
from meetup_search.meetup_api_client.meetup_api_client import MeetupApiClient
from meetup_search.models.group import Group
from meetup_search.models.meetup_zip import MeetupZip


@click.command(name="load_groups")
@click.option("--load_events", nargs=1, type=bool, default=True)
@click.option("--country", nargs=1, type=str, default="DE")
@with_appcontext
def load_groups_command(load_events: bool, country: str):
    """
    Load all groups from a country of all meetup zips saved in elasticsearch

    Arguments:
        load_events {bool} -- Load all past events of every group and save them into elasticsearch
        country {str} -- Country code like DE for germany
    """

    load_groups(load_events=load_events, country=country)

def load_groups(load_events: bool, country: str):
    """
    Load all groups from a country of all meetup zips saved in elasticsearch

    Arguments:
        load_events {bool} -- Load all past events of every group and save them into elasticsearch
        country {str} -- Country code like DE for germany
    """
    env = Env()
    
    # meetup api client
    api_client: MeetupApiClient = MeetupApiClient(
        cookie=env("MEETUP_AUTH_COOKIE"), csrf_token=env("MEETUP_CSRF_TOKEN")
    )

    # get all zip codes from elasticsearch
    meetup_zips: List[MeetupZip] = MeetupZip.get_all_zips()

    print("Start fetching groups from meetup!")

    for meetup_zip in meetup_zips:
        groups: List[Group] = api_client.search_new_groups(
            zip_code=meetup_zip.zip_code, country_code=country
        )

        sleep(1)

        if load_events:
            for group in groups:
                print(group.urlname)

                try:
                    api_client.update_all_group_events(group=group)
                except Exception as e:
                    print(e)

        print(
            "{} groups was added to elasticsearch for zip {}!".format(
                len(groups), meetup_zip.zip_code
            )
        )
