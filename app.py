from typing import Optional

from envparse import env
from flask import Flask
from flask.app import Flask as FlaskApp
from flask_restful import Api

from flask_cors import CORS
from meetup_search.commands.get_group import get_group
from meetup_search.commands.get_groups import get_groups
from meetup_search.commands.load_groups import load_groups
from meetup_search.commands.load_zip_codes import load_zip_codes
from meetup_search.commands.migrate_models import migrate_models
from meetup_search.commands.update_groups import update_groups
from meetup_search.rest_api.api import MeetupSearchApi, MeetupSearchSuggestApi


def create_app(config_path: Optional[str] = None) -> FlaskApp:
    """
    Create a flask app and load a config file. 
    When no config_path is given it will try to load the config file from FLASK_CONFIGURATION enviroment var and when the
    FLASK_CONFIGURATION does not exists, it load the production config file.

    Keyword Arguments:
        config_path {Optional[str]} -- Path to a flask config file (default: None)

    Returns:
        FlaskApp -- flask app with loaded configs
    """

    if not config_path:
        config_path = env("FLASK_CONFIGURATION", "/app/config/production.py")

    # init flask app
    app = Flask(__name__)
    app.config.from_pyfile(config_path)
    CORS(app, resources={r"/*": {"origins": env("CORS_ORIGINS")}})

    # init flask api
    api: Api = Api(app)
    api.add_resource(MeetupSearchApi, "/")
    api.add_resource(MeetupSearchSuggestApi, "/suggest/")

    # add commands to flask app
    app.cli.add_command(get_group)
    app.cli.add_command(get_groups)
    app.cli.add_command(update_groups)
    app.cli.add_command(load_zip_codes)
    app.cli.add_command(load_groups)
    app.cli.add_command(migrate_models)

    return app


flask_app: FlaskApp = create_app()

if __name__ == "__main__":
    flask_app.run(host=env("FLASK_HOST", "127.0.0.1"))
