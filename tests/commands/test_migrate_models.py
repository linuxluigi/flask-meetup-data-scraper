from time import sleep
from typing import List

import pytest
from click.testing import Result
from conftest import delte_index
from elasticsearch.exceptions import NotFoundError
from flask.app import Flask
from flask.testing import FlaskCliRunner
from meetup_search.commands.migrate_models import migrate_models
from meetup_search.models.group import Group
from meetup_search.models.meetup_zip import MeetupZip


def test_migrate_models(meetup_groups: dict, app: Flask):
    runner: FlaskCliRunner = app.test_cli_runner()

    # delete index
    delte_index()

    # check if index was deleted
    with pytest.raises(NotFoundError):
        Group.get_all_groups()
    with pytest.raises(NotFoundError):
        MeetupZip.get_all_zips()

    # migrate models
    result_1: Result = runner.invoke(migrate_models)
    assert result_1.exit_code == 0
    sleep(2)

    # check if indexes was created
    assert isinstance(Group.get_all_groups(), List)
    assert isinstance(MeetupZip.get_all_zips(), List)
