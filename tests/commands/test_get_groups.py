from meetup_search.commands.get_groups import get_groups
from meetup_search.models.group import Group
from time import sleep
from flask.app import Flask
from flask.testing import FlaskCliRunner
from click.testing import Result


def test_get_groups_with_events(meetup_groups: dict, app: Flask):
    runner: FlaskCliRunner = app.test_cli_runner()

    # load all groups from JSON test file
    result_1: Result = runner.invoke(
        get_groups, ["/app/compose/local/flask/meetup_groups"]
    )
    assert result_1.exit_code == 0

    sleep(1)

    # load group
    group_1: Group = Group.get_group(urlname=meetup_groups["sandbox"]["urlname"])

    # check if group has events
    assert len(group_1.events) > 0


def test_get_groups_without_events(meetup_groups: dict, app: Flask):
    runner: FlaskCliRunner = app.test_cli_runner()

    # load all groups from JSON test file
    result_1: Result = runner.invoke(
        get_groups, ["/app/compose/local/flask/meetup_groups", "--load_events", "False"]
    )
    assert result_1.exit_code == 0

    sleep(1)

    # load group
    group_1: Group = Group.get_group(urlname=meetup_groups["sandbox"]["urlname"])

    # check if group has events
    assert len(group_1.events) == 0
