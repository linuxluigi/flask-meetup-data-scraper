import pytest
from click.testing import Result
from flask.app import Flask
from flask.testing import FlaskCliRunner
from meetup_search.commands.load_zip_codes import load_zip_codes
from meetup_search.models.meetup_zip import MeetupZip
from time import sleep


def test_load_zip_codes(app: Flask):
    runner: FlaskCliRunner = app.test_cli_runner()

    # load zip codes from berlin
    result_1: Result = runner.invoke(load_zip_codes, ["52.3570365", "52.6770365", "13.2288599", "13.5488599"])
    assert result_1.exit_code == 0

    sleep(2)

    assert len(MeetupZip.get_all_zips()) > 0

    # force http error
    result_2: Result = runner.invoke(load_zip_codes, ["10000", "10001", "10000", "10001"])
    assert result_2.exit_code == 1
