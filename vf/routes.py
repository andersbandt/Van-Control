
# import needed modules
from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
from flask import session
from flask import abort
from flask.blueprints import Blueprint

# import user created modules
import db.helpers as dbh
from analysis import data_helper as datah

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
    max_limit = request.args.get('max_limit', default=5000, type=int)

    # Retrieve aligned data using your new alignment function
    aligned_data = datah.retrieve_aligned_data(max_limit)

    # Process aligned data
    labels = [row["timestamp"] for row in aligned_data]
    temp1 = [row["temperatures"][0] for row in aligned_data]
    temp2 = [row["temperatures"][1] for row in aligned_data]
    temp3 = [row["temperatures"][2] for row in aligned_data]
    

    # NOTE: Assuming you want to extend this logic to include humidity or other datasets,
    # include those calculations here as required.

    # If the request is an AJAX call, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'labels': labels,
            'data1_1': temp1,
            'data1_2': temp2,
            'data1_3': temp3,
            'data2_1': temp1,
            'data2_2': temp2,
            'data2_3': temp3
        })

    # Otherwise, return the HTML page with data rendered in Jinja
    return render_template('data.html',
                           labels=labels,
                           data1_1=temp1,
                           data1_2=temp2,
                           data1_3=temp3,
                           data2_1=temp1,
                           data2_2=temp2,
                           data2_3=temp3)


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



###############################################
###########    API data stuff      ############
###############################################
@blueprint.route('/stats', methods=['GET'])
def get_stats():
    sensor_id = request.args.get('sensor_id', default=0, type=int)
    max_limit = request.args.get('max_limit', default=5000, type=int)
    
    result = dbh.sensors.get_stats(sensor_id, max_limit)

    def c_to_f(celsius):
        return celsius*1.8 + 32

    
    # Calculate statistics
    # TODO: pass in data in both Celsius and Fahrenheit here
    stats = {
        'high': c_to_f(result['high']),
        'low': c_to_f(result['low']),
        'mean': c_to_f(round(result['mean'], 2)),
        'earliest_time': result['earliest_time'],
        'latest_time': result['latest_time']
    }

    # Return stats as JSON for AJAX to consume
    return jsonify(stats)



