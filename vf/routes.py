
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
    start_date = request.args.get('start_date', default=None, type=str)
    end_date = request.args.get('end_date', default=None, type=str)
    scale = request.args.get('scale', default='f', type=str)

    # Check if date range is provided
    if start_date and end_date:
        # Use date-based retrieval
        aligned_data = datah.retrieve_aligned_data_by_date(start_date, end_date, scale=scale)
    else:
        # Use limit-based retrieval (original behavior)
        aligned_data = datah.retrieve_aligned_data(max_limit, scale=scale)

    # Process aligned data
    labels = [row["timestamp"] for row in aligned_data]
    temp1 = [row["temperature"][0] for row in aligned_data]
    temp2 = [row["temperature"][1] for row in aligned_data]
    temp3 = [row["temperature"][2] for row in aligned_data]

    hum1 = [row["humidity"][0] for row in aligned_data]
    hum2 = [row["humidity"][1] for row in aligned_data]
    hum3 = [row["humidity"][2] for row in aligned_data]

    # If the request is an AJAX call, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'labels': labels,
            'data1_1': temp1,
            'data1_2': temp2,
            'data1_3': temp3,
            'data2_1': hum1,
            'data2_2': hum2,
            'data2_3': hum3
        })

    # Otherwise, return the HTML page with data rendered in Jinja
    return render_template('data.html',
                           labels=labels,
                           data1_1=temp1,
                           data1_2=temp2,
                           data1_3=temp3,
                           data2_1=hum1,
                           data2_2=hum2,
                           data2_3=hum3,
                           max_limit=max_limit)


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
# TODO: pass in data in both Celsius and Fahrenheit here. Can have a drop down on the main page?
@blueprint.route('/stats', methods=['GET'])
def get_stats():
    def c_to_f(celsius):
        return celsius * 1.8 + 32

    sensor_id = request.args.get('sensor_id', default=0, type=int)
    max_limit = request.args.get('max_limit', default=5000, type=int)
    start_date = request.args.get('start_date', default=None, type=str)
    end_date = request.args.get('end_date', default=None, type=str)
    scale = request.args.get('scale', default='f', type=str)

    # Check if date range is provided
    if start_date and end_date:
        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"
        result = dbh.sensors.get_stats_by_date_range(sensor_id, start_datetime, end_datetime)
    else:
        result = dbh.sensors.get_stats(sensor_id, max_limit)

    # Apply temperature conversion based on scale
    if scale.lower() == 'f':
        stats = {
            'temp_high': round(c_to_f(result['temp_high']), 2) if result['temp_high'] is not None else 'N/A',
            'temp_low': round(c_to_f(result['temp_low']), 2) if result['temp_low'] is not None else 'N/A',
            'temp_mean': round(c_to_f(result['temp_mean']), 2) if result['temp_mean'] is not None else 'N/A',
            'temp_stddev': round(c_to_f(result['temp_stddev']) if result['temp_stddev'] else 0, 2) if result['temp_stddev'] is not None else 'N/A',
            'hum_high': round(result['hum_high'], 2) if result['hum_high'] is not None else 'N/A',
            'hum_low': round(result['hum_low'], 2) if result['hum_low'] is not None else 'N/A',
            'hum_mean': round(result['hum_mean'], 2) if result['hum_mean'] is not None else 'N/A',
            'hum_stddev': round(result['hum_stddev'], 2) if result['hum_stddev'] is not None else 'N/A',
            'count': result['count'],
            'earliest_time': result['earliest_time'],
            'latest_time': result['latest_time'],
        }
    else:  # Celsius
        stats = {
            'temp_high': round(result['temp_high'], 2) if result['temp_high'] is not None else 'N/A',
            'temp_low': round(result['temp_low'], 2) if result['temp_low'] is not None else 'N/A',
            'temp_mean': round(result['temp_mean'], 2) if result['temp_mean'] is not None else 'N/A',
            'temp_stddev': round(result['temp_stddev'], 2) if result['temp_stddev'] is not None else 'N/A',
            'hum_high': round(result['hum_high'], 2) if result['hum_high'] is not None else 'N/A',
            'hum_low': round(result['hum_low'], 2) if result['hum_low'] is not None else 'N/A',
            'hum_mean': round(result['hum_mean'], 2) if result['hum_mean'] is not None else 'N/A',
            'hum_stddev': round(result['hum_stddev'], 2) if result['hum_stddev'] is not None else 'N/A',
            'count': result['count'],
            'earliest_time': result['earliest_time'],
            'latest_time': result['latest_time'],
        }

    # Return stats as JSON for AJAX to consume
    return jsonify(stats)



