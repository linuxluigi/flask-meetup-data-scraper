from config.base import *
from envparse import env

# Flask
# ------------------------------------------------------------------------------
TESTING = False
DEBUG = False

# Server Name https://flask.palletsprojects.com/en/1.1.x/config/#SERVER_NAME
SERVER_NAME = env("SERVER_NAME", default="localhost")
