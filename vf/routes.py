# import needed modules
from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import abort
from flask.blueprints import Blueprint

# import user created modules
import db.helpers as dbh

# define my Blueprint class that handles everything
blueprint = Blueprint('routes', __name__, static_folder='static', template_folder='/templates')


# site navigation stuff
@blueprint.route('/')
def home():
    return render_template('index.html', **locals())  # locals are the variables I pass


@blueprint.route('/index.html')
def index_return():
    return home()


@blueprint.route('/automate.html')
def automate():
    return render_template('automate.html', **locals())


@blueprint.route('/data.html')
def data_fetch():
    # Get the data from the database
    max_limit = 1000
    raw_data = dbh.sensors.get_data(0, max_limit)

    # assign data to variables
    labels = [row[2] for row in raw_data]
    temp1 = [row[0] for row in raw_data]
    humidity1 = [row[1] for row in raw_data]

    raw_data = dbh.sensors.get_data(1, max_limit)
    temp2 = [row[0] for row in raw_data]
    humidity2 = [row[1] for row in raw_data]

    raw_data = dbh.sensors.get_data(2, max_limit)
    temp3 = [row[0] for row in raw_data]
    humidity3 = [row[1] for row in raw_data]

    # Pass the data to the template
    return render_template('data.html',
                           labels=labels,
                           data1_1=temp1,
                           data1_2=temp2,
                           data1_3=temp3,
                           data2_1=humidity1,
                           data2_2=humidity2,
                           data2_3=humidity3)


@blueprint.route('/battery.html')
def battery():
    battery_data = dbh.battery.get_battery_data()

    # Pass the data to the template
    return render_template(
        'battery.html',
        voltage=battery_data['voltage'],
        current=battery_data['current'],
        power=battery_data['power'],
        state_of_charge=battery_data['state_of_charge'],
        timestamp=battery_data['timestamp']
    )


@blueprint.route('/control.html')
def control():
    return render_template('control.html', **locals())

# sensor stuff
# @blueprint.route('/readpH')
# def recordPH():
# 	pHString = str(sensorControl.readpH())
# 	return render_template('control.html', pH = pHString)

# # light stuff
# @blueprint.route('/lightOn')
# def lightOn():
# 	print("The light should be on")
# 	lightControl.lightOn()
# 	return render_template('control.html', **locals())
