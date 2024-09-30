from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import abort
from flask.blueprints import Blueprint

import db.helpers as dbh

blueprint = Blueprint('routes', __name__, static_folder='static', template_folder='/templates')


# site navigation stuff
@blueprint.route('/')
def home():
	return render_template('index.html',**locals()) # locals are the variables I pass

@blueprint.route('/index.html')
def index_return():
	return home()

@blueprint.route('/data.html')
def data_fetch():
        max_limit = 100
        # Get the data from the database
        raw_data = dbh.sensors.get_data(0, max_limit)
        labels = [row[2] for row in raw_data]
        temp1 = [row[0] for row in raw_data]
#        humidity1 = [row[1] for row in raw_data]

        raw_data = dbh.sensors.get_data(1, max_limit)
        temp2 = [row[0] for row in raw_data]

        raw_data = dbh.sensors.get_data(2, max_limit)
        temp3 = [row[0] for row in raw_data]

        # Pass the data to the template
        return render_template('data.html',
                               labels=labels,
                               data1=temp1,
                               data2=temp2,
                               data3=temp3)


# @blueprint.route('/chart-data')
# def chart_data():
#         # Get the data from the database
#         def generate_random_data():
#                 while True:
#                         json_data = json.dumps(
#                                 {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
#                         yield f"data:{json_data}\n\n"
#                         time.sleep(1)

#         response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
#         response.headers["Cache-Control"] = "no-cache"
#         response.headers["X-Accel-Buffering"] = "no"
#         return response
        

@blueprint.route('/automate.html')
def automate():
	return render_template('automate.html')

@blueprint.route('/control.html')
def control():
	return render_template('control.html', **locals())

# sensor stuff
# @blueprint.route('/readpH')
# def recordPH():
# 	pHString = str(sensorControl.readpH())
# 	return render_template('control.html', pH = pHString)

# @blueprint.route('/readEC')
# def recordEC():
# 	ECVal = sensorControl.readEC()
# 	return render_template('control.html', EC = ECVal)

# # light stuff
# @blueprint.route('/lightOn')
# def lightOn():
# 	print("The light should be on")
# 	lightControl.lightOn()
# 	return render_template('control.html', **locals())

# @blueprint.route('/lightOff')
# def lightOff():
# 	print("The light should be off")
# 	lightControl.lightOff()
# 	return render_template('control.html', **locals())

# # air and water stuff
# @blueprint.route('/airOn')
# def airOn():
# 	print("The air pump should be on!")
# 	airControl.airOn()
# 	return render_template('control.html', **locals())

# @blueprint.route('/airOff')
# def airOff():
# 	print("The air pump should be off!")
# 	airControl.airOff()
# 	return render_template('control.html', **locals())

# @blueprint.route('/waterOn')
# def waterOn():
# 	waterControl.waterOn()
# 	print("The main water pump should be on")
# 	return "Water status: on"
# 	return render_template('control.html', **locals())

# @blueprint.route('/waterOff')
# def waterOff():
# 	print("The water pump should be off!")
# 	waterControl.waterOff()
# 	return "water status: off"
# 	return render_template('control.html', **locals())

# # fan stuff
# @blueprint.route('/intakeOn')
# def intakeOn():
# 	fanControl.intakeOn()
# 	print("The intake fan should be on")
# 	return "Intake status: on"
# 	return render_template('control.html', **locals())

# @blueprint.route('/intakeOff')
# def intakeOff():
# 	fanControl.intakeOff()
# 	print("The intake fan should be off")
# 	return render_template('control.html', **locals())

# @blueprint.route('/outtakeOn')
# def outtakeOn():
# 	fanControl.outtakeOn()
# 	print("The outtake fan should be on")
# 	return render_template('control.html', **locals())

# @blueprint.route('/outtakeOff')
# def outtakeOff():
# 	fanControl.outtakeOff()
# 	print("The outtake fan should be off")
# 	return render_template('control.html', **locals())


