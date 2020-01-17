from time import sleep

from click.testing import Result
from flask.app import Flask
from flask.testing import FlaskCliRunner
from meetup_search.commands.update_groups import update_groups
from meetup_search.models.group import Group


def test_update_groups(group_1: Group,  meetup_groups: dict, app: Flask):
    runner: FlaskCliRunner = app.test_cli_runner()

    # init group to update
    group_1.urlname = meetup_groups["sandbox"]["urlname"]
    group_1.save()
    sleep(2)

    # update all groups
    result_1: Result = runner.invoke(update_groups)
    assert result_1.exit_code == 0
    sleep(2)

    # check if group was updated
    group_2: Group = Group.get_group(urlname=group_1.urlname)
    assert len(group_2.events) > 0
