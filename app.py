from flask import Flask
from flask.app import Flask as FlaskApp
from flask.cli import with_appcontext
import click
import os
from meetup_search.commands.get_groups import get_groups as command_get_groups
from meetup_search.models import Group
from elasticsearch_dsl import connections
from typing import Optional
from envparse import env


# flask default setup
def create_app(config_path: Optional[str] = env("FLASK_CONFIGURATION")) -> FlaskApp:
    app = Flask(__name__)
    app.config.from_pyfile(config_path)
    return app


app: FlaskApp = create_app()


@app.route("/")
def hello_docker():
    return "Hello, I run in a docker container"


@click.command(name="get_groups")
@with_appcontext
@click.argument(
    "meetup_files_path",
    type=click.Path(exists=True),
    required=False,
    default="meetup_groups",
)
def get_groups(meetup_files_path: str):
    """
    import new meetup groups from JSON files and get all events from meetup.com
    """
    command_get_groups(meetup_files_path=meetup_files_path)


@click.command(name="migrate_models")
@with_appcontext
def migrate_models():
    """
    init elasticsearch models
    """
    Group.init()


app.cli.add_command(get_groups)
app.cli.add_command(migrate_models)

if __name__ == "__main__":
    app.run(host="127.0.0.1")
