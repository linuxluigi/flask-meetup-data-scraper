from typing import List

import click
from flask.cli import with_appcontext
from meetup_search.meetup_api_client.exceptions import (
    HttpNoSuccess,
    HttpNotAccessibleError,
    HttpNotFoundError,
    HttpNoXRateLimitHeader,
)
from meetup_search.meetup_api_client.meetup_api_client import MeetupApiClient
from meetup_search.models.meetup_zip import MeetupZip


@click.command(name="load_zip_codes")
@click.argument("lat_min", type=float, required=True)
@click.argument("lat_max", type=float, required=True)
@click.argument("lon_min", type=float, required=True)
@click.argument("lon_max", type=float, required=True)
@with_appcontext
def load_zip_codes_command(lat_min: float, lat_max: float, lon_min: float, lon_max: float):
    """
    Load all meetup zip codes from a boundingbox [min_lat, max_lat, min_lon, max_lon]

    Arguments:
        lat_min {float} -- boundingbox lat min
        lat_max {float} -- boundingbox lat max
        lon_min {float} -- boundingbox lon min
        lon_max {float} -- boundingbox lon max
    """
    load_zip_codes(lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max)

def load_zip_codes(lat_min: float, lat_max: float, lon_min: float, lon_max: float):
    """
    Load all meetup zip codes from a boundingbox [min_lat, max_lat, min_lon, max_lon]

    Arguments:
        lat_min {float} -- boundingbox lat min
        lat_max {float} -- boundingbox lat max
        lon_min {float} -- boundingbox lon min
        lon_max {float} -- boundingbox lon max
    """
    # init api client
    api_client: MeetupApiClient = MeetupApiClient()

    try:
        # get all zip codes from Switzerland
        zip_code_list: List[str] = api_client.get_all_zip_from_meetup(
            min_lat=lat_min, max_lat=lat_max, min_lon=lon_min, max_lon=lon_max,
        )
    except (
        HttpNotFoundError,
        HttpNotAccessibleError,
        HttpNoSuccess,
        HttpNoXRateLimitHeader,
    ) as e:
        print(e)
        print("Network error, please try again later!")
        print("There was no zip code added to elasticsearch!")
        exit(1)

    meetup_zips: List[MeetupZip] = MeetupZip.get_or_create_zips(
        zip_code_list=zip_code_list
    )

    print("{} zip codes was updated!".format(len(meetup_zips)))
