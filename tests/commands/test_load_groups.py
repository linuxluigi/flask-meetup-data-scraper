from time import sleep

from click.testing import Result
from flask.app import Flask
from flask.testing import FlaskCliRunner
from meetup_search.models.group import Group
from meetup_search.models.meetup_zip import MeetupZip
from meetup_search.commands.load_groups import load_groups


def test_load_groups_without_events(app: Flask):
    # enable as soon as api account is integrated
    pass

    # runner: FlaskCliRunner = app.test_cli_runner()

    # # add zip code to elasticsearch
    # meetup_zip: MeetupZip = MeetupZip(zip_code="meetup12")
    # meetup_zip.save()

    # sleep(1)

    # # load all groups without events
    # result: Result = runner.invoke(load_groups, ['--load_events', 'False'])
    # assert result.exit_code == 0

    # sleep(1)

    # # load groups from elasticsearch
    # groups: [Group] = Group.get_all_groups()

    # # check if groups was added to elasticsearch
    # assert len(groups) > 0

    # # check if there is no event for all groups
    # for group in groups:
    #     assert len(group.events) == 0


def test_load_groups_with_events(app: Flask):
    # enable as soon as api account is integrated
    pass

    # runner: FlaskCliRunner = app.test_cli_runner()

    # # add zip code to elasticsearch
    # meetup_zip: MeetupZip = MeetupZip(zip_code="meetup12")
    # meetup_zip.save()

    # sleep(1)

    # # load all groups without events
    # result: Result = runner.invoke(load_groups, ['--load_events', 'True'])
    # assert result.exit_code == 0

    # sleep(1)

    # # load groups from elasticsearch
    # groups: [Group] = Group.get_all_groups()

    # # check if groups was added to elasticsearch
    # assert len(groups) > 0

    # # check if there are events for at least one group
    # events_added: bool = False
    # for group in groups:
    #     if len(group.events) > 0:
    #         events_added = True
    #         break
    # assert events_added is True
