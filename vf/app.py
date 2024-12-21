

# import needed modules
from flask import Flask


# import user created modules
from vf import routes


def createApp():
	app = Flask(__name__)
	register_blueprints(app)

	return app


def register_blueprints(app):
	app.register_blueprint(routes.blueprint)




