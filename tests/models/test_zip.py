import pytest
from meetup_search.models.meetup_zip import MeetupZip
from time import sleep
from typing import List


def test_get_or_create_zip():
    zip_code: str = "12345"

    # create 2 MeetupZips with the same zip
    meetup_zip_1: MeetupZip = MeetupZip.get_or_create_zip(zip_code=zip_code)
    sleep(2)
    meetup_zip_2: MeetupZip = MeetupZip.get_or_create_zip(zip_code=zip_code)

    # # check if both MeetupZip has the same id
    assert meetup_zip_1.meta.id == meetup_zip_2.meta.id
    assert meetup_zip_1.zip_code == zip_code
    assert meetup_zip_2.zip_code == zip_code


def test_get_or_create_zips():
    # list with double entries; it contain 4 different zip_codes
    zip_list: List[str] = [
        "1",
        "2",
        "3",
        "1",
        "4",
        "2"
    ]

    # create new zip_codes
    meetup_zips_1: List[MeetupZip] = MeetupZip.get_or_create_zips(zip_code_list=zip_list)

    assert len(meetup_zips_1) == 4
    for meetup_zip in meetup_zips_1:
        assert isinstance(meetup_zip, MeetupZip)


def test_get_all_zips():
    # get all MeetupZip without add one to elasticsearch
    assert len(MeetupZip.get_all_zips()) == 0

    # create in a loop MeetupZips
    for i in range(0, 5):
        MeetupZip.get_or_create_zip(zip_code="{}".format(i))

        sleep(1)

        assert len(MeetupZip.get_all_zips()) == i + 1
        assert isinstance(MeetupZip.get_all_zips()[i], MeetupZip)
        assert MeetupZip.get_all_zips()[i].zip_code == "{}".format(i)
