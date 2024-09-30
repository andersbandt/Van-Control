from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import abort

from van_flask import routes


def createApp():
	app = Flask(__name__)
	register_blueprints(app)

	return app


def register_blueprints(app):
	app.register_blueprint(routes.blueprint)




