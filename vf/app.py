

# import needed modules
from flask import Flask
import logging


# import user created modules
from vf import routes


def createApp():
    app = Flask(__name__)
    register_blueprints(app)

    # set up logging
    app.logger.setLevel(logging.DEBUG)
        
    # Create a file handler
    # TODO: figure out 
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)  # Capture debug and above
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # add handlers
    app.logger.addHandler(file_handler)

    return app


def register_blueprints(app):
	app.register_blueprint(routes.blueprint)




