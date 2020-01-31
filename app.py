from typing import Optional

from environs import Env
from flask import Flask, redirect, request, session, url_for
from flask.app import Flask as FlaskApp
from flask.json import jsonify
from flask_cors import CORS
from flask_restful import Api
from meetup_search.commands.get_group import get_group
from meetup_search.commands.get_groups import get_groups
from meetup_search.commands.load_groups import load_groups_command as load_groups
from meetup_search.commands.load_zip_codes import load_zip_codes_command as load_zip_codes
from meetup_search.commands.migrate_models import migrate_models_command as migrate_models
from meetup_search.commands.reset_index import reset_index
from meetup_search.commands.update_groups import update_groups
from meetup_search.meetup_api_client.meetup_api_client import MeetupApiClient
from meetup_search.models.token import Token
from meetup_search.rest_api.api import MeetupSearchApi, MeetupSearchSuggestApi
from requests_oauthlib import OAuth2Session


def create_app(config_path: Optional[str] = None) -> FlaskApp:
    """
    Create a flask app and load a config file. 
    When no config_path is given it will try to load the config file from FLASK_CONFIGURATION
    enviroment var and when the FLASK_CONFIGURATION does not exists, it load the production config
    file.

    Keyword Arguments:
        config_path {Optional[str]} -- Path to a flask config file (default: None)

    Returns:
        FlaskApp -- flask app with loaded configs
    """

    env: Env = Env()

    if not config_path:
       config_path = env("FLASK_CONFIGURATION", "/app/config/production.py")

    # init flask app
    app = Flask(__name__)
    app.config.from_pyfile(config_path)
    CORS(app, resources={r"/*": {"origins": env("CORS_ORIGINS")}})

    @app.route("/login")
    def login():
        """
        Meetup.com oauth login page based on
        https://github.com/pferate/meetup-api/pull/17#issuecomment-516834900
        """
        scopes = ['ageless']
        meetup = OAuth2Session(
                env("MEETUP_CLIENT_ID"),
                redirect_uri='https://{}/callback'.format(env("DOMAIN")),
                scope=scopes
            )
        authorization_url, state = meetup.authorization_url(MeetupApiClient.AUTHORIZATION_BASE_URL)

        # State is used to prevent CSRF, keep this for later.
        session['oauth_state'] = state
        return redirect(authorization_url)

    @app.route("/callback")
    def callback():
        """
        Meetup.com oauth callback page based on
        https://github.com/pferate/meetup-api/pull/17#issuecomment-516834900
        """
        meetup = OAuth2Session(env("MEETUP_CLIENT_ID"), state=session['oauth_state'])
        meetup_token = meetup.fetch_token(
                MeetupApiClient.TOKEN_URL,
                client_secret=env("MEETUP_CLIENT_SECRET"),
                authorization_response=request.url
            )

        Token.delete_all_tokens()
        token: Token = Token(
            access_token=meetup_token['access_token'],
            refresh_token=meetup_token['refresh_token']
        )
        token.save()
        
        return jsonify(
                meetup.get('https://api.meetup.com/self/groups?&sign=true&photo-host=secure&page=20'
            ).json())

    # init flask api
    api: Api = Api(app)
    # add api endpoints
    api.add_resource(MeetupSearchApi, "/")
    api.add_resource(MeetupSearchSuggestApi, "/suggest/")

    # add commands to flask app
    app.cli.add_command(get_group)
    app.cli.add_command(get_groups)
    app.cli.add_command(update_groups)
    app.cli.add_command(load_zip_codes)
    app.cli.add_command(load_groups)
    app.cli.add_command(migrate_models)
    app.cli.add_command(reset_index)

    return app


flask_app: FlaskApp = create_app()

if __name__ == "__main__":
    env: Env = Env()
    flask_app.run(host=env("FLASK_HOST", "0.0.0.0"))
