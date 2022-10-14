import os

from application.flask.app import create_app

app = create_app(os.environ["FLASK_CONFIG"])
