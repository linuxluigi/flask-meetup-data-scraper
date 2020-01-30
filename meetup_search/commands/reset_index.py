import time
from time import sleep
from typing import List, Optional

import click
from elasticsearch import Elasticsearch
from environs import Env
from flask.cli import with_appcontext
from flask.config import Config

from meetup_search.commands.load_groups import load_groups
from meetup_search.commands.load_zip_codes import load_zip_codes
from meetup_search.commands.migrate_models import migrate_models
from meetup_search.models.group import Group
from meetup_search.models.meetup_zip import MeetupZip


@click.command(name="reset_index")
@click.option("--waring_time", type=int, default=30)
@click.option("--reset_periode", type=int)
@with_appcontext
def reset_index(waring_time: int, reset_periode: Optional[int]):
    """
    Reset elasticsearch index & reload every new group from meetup.com
    
    Arguments:
        waring_time {int} -- Delay time for stop command
        reset_periode {Optional[int]} -- run this command in a weekly periode like every 4 weeks
    """

    # check if it's time to reset elasticsearch index
    if reset_periode:
        unixtime_secounds: int = int(time.time())
        unixtime_minutes: int = int(unixtime_secounds / 60)
        unixtime_hours: int = int(unixtime_minutes / 60)
        unixtime_days: int = int(unixtime_hours / 24)
        unixtime_weeks: int = int(unixtime_days / 7)
        print(unixtime_weeks)
        if unixtime_weeks % reset_periode != 0:
            print("Skip reset elasticsearch index, because it's not on schedule!")
            exit(0)

    print("You try to drop the current elasticsearch index & to reload them again!")
    print("You have 30 secounds to stop this operation, you can't undo this action!")
    print("To stop this action press 'crtl + c'")

    try:
        for secounds in range(waring_time, 0, -1):
            sleep(1)
            print("{} secounds left ...".format(secounds))
    except KeyboardInterrupt:
        print("You stop this action, nothing changed...")
        return

    print("The Elasticsearch index will now be delted ...")

    # delete group & meetup zip index
    # fixme load es from flask base config!
    env: Env = Env()
    elasticsearch: Elasticsearch = Elasticsearch(
        [{"host": env("http.host"), "port": env("http.port")}]
    )
    elasticsearch.indices.delete(index=Group.Index.name, ignore=[400, 404])
    elasticsearch.indices.delete(index=MeetupZip.Index.name, ignore=[400, 404])

    sleep(2)

    print("The Elasticsearch index are now deletet!")

    # migrate models
    migrate_models()

    sleep(1)

    env: Env = Env()

    boundingboxes: dict = env.dict("LOCATION_BOUNDINGBOX", subcast=str)
    for boundingbox in boundingboxes:
        print("Load meetup.com zip codes for {}".format(boundingbox))
        boundingbox_list: List[str] = boundingboxes[boundingbox].split(" ")
        load_zip_codes(
            lat_min=float(boundingbox_list[0]),
            lat_max=float(boundingbox_list[1]),
            lon_min=float(boundingbox_list[2]),
            lon_max=float(boundingbox_list[3]),
        )

    sleep(2)

    for country in env.list("LOCATION_COUNTRIES"):
        print("Load groups with all events from {}!".format(country))
        load_groups(load_events=True, country=country)

    print("All done :)")
