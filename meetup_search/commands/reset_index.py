from time import sleep
from typing import List

import click
from environs import Env
from flask.cli import with_appcontext
from flask.config import Config

import app
from meetup_search.commands.load_groups import load_groups
from meetup_search.commands.load_zip_codes import load_zip_codes
from meetup_search.commands.migrate_models import migrate_models
from meetup_search.models.group import Group
from meetup_search.models.meetup_zip import MeetupZip


@click.command(name="reset_index")
@click.option("--waring_time", type=int, default=30)
@with_appcontext
def reset_index(waring_time: int):
    """
    Reset elasticsearch index & reload every new group from meetup.com
    """

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

    # load app config
    app_config: Config = app.create_app().config

    print("The Elasticsearch index will now be delted ...")

    # delete group & meetup zip index
    app_config["ES"].indices.delete(index=Group.Index.name, ignore=[400, 404])
    app_config["ES"].indices.delete(index=MeetupZip.Index.name, ignore=[400, 404])

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
