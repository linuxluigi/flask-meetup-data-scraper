from click.testing import Result
from flask.app import Flask
from flask.testing import FlaskCliRunner
from meetup_search.commands.get_group import get_group


def test_get_group(meetup_groups: dict, app: Flask):
    runner: FlaskCliRunner = app.test_cli_runner()

    # run command without params
    result_1: Result = runner.invoke(get_group)
    assert result_1.exit_code == 1

    # test with exiting group
    result_2: Result = runner.invoke(get_group, [meetup_groups["sandbox"]["urlname"]])
    assert result_2.exit_code == 0

    # test with not-exist group
    result_3: Result = runner.invoke(get_group, [meetup_groups["not-exist"]["urlname"]])
    assert result_3.exit_code == 2

    # test with gone group
    result_4: Result = runner.invoke(get_group, [meetup_groups["gone"]["urlname"]])
    assert result_4.exit_code == 2
