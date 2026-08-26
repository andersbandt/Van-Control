

# import needed modules
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler


# import user created modules
from vf import routes


def createApp():
    app = Flask(__name__)
    register_blueprints(app)

    # set up logging
    app.logger.setLevel(logging.DEBUG)

    # Create a file handler
    # Rotating, not a plain FileHandler: this file was growing unbounded
    # (DEBUG level, no cap) -- capped at 1MB x 3 backups so it can't quietly
    # eat the SD card over months of uptime.
    file_handler = RotatingFileHandler('app.log', maxBytes=1_000_000, backupCount=3)
    file_handler.setLevel(logging.DEBUG)  # Capture debug and above
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # add handlers
    app.logger.addHandler(file_handler)

    return app


def register_blueprints(app):
	app.register_blueprint(routes.blueprint)




