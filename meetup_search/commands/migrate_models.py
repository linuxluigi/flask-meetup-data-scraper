import click
from flask.cli import with_appcontext

from meetup_search.models.group import Group
from meetup_search.models.meetup_zip import MeetupZip


@click.command(name="migrate_models")
@with_appcontext
def migrate_models_command():
    """
    init elasticsearch models
    """
    migrate_models()

def migrate_models():
    """
    init elasticsearch models
    """
    Group.init()
    MeetupZip.init()
