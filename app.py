import os
import time
from flask import Flask, request, jsonify, render_template
from CO2Monitor import CO2Monitor
from apscheduler.schedulers.background import BackgroundScheduler
import redis
import atexit
from flask_cors import CORS, cross_origin



app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
aqm = CO2Monitor()

scheduler = BackgroundScheduler()
scheduler.add_job(func=aqm.save_measurement_to_redis, trigger="interval", seconds=60)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


def reconfigure_data(measurement):
    """Reconfigures data for chart.js"""
    current = int(time.time())
    measurement = measurement[:1200]
    measurement.reverse()
    return {
        'labels': [x['measurement']['timestamp'] for x in measurement],
        #'labels': [x['time'] for x in measurement],
        'temp_f': {
            'label': 'Temperature (F)',
            'data': [(x['measurement']['temp_f']) for x in measurement],
            'backgroundColor': '#cc0000',
            'borderColor': '#cc0000',
            'borderWidth': 3,
        },
        'humid_perc': {
            'label': 'Humidity (%)',
            'data': [x['measurement']['humid_perc'] for x in measurement],
            'backgroundColor': '#42C0FB',
            'borderColor': '#42C0FB',
            'borderWidth': 3,
        },
        'co2_ppm': {
            'label': 'CO2 (ppm)',
            'data': [x['measurement']['co2_ppm'] for x in measurement],
            'backgroundColor': '#42C0FB',
            'borderColor': '#42C0FB',
            'borderWidth': 3,
        },
    }

@app.route('/')
def index():
    """Index page for the application"""
    context = {
        'historical': reconfigure_data(aqm.get_last_n_measurements()),
    }
    return render_template('index.html', context=context)


@app.route('/api/')
@cross_origin()

def api():
    """Returns historical data from the sensor"""
    context = {
        'historical': reconfigure_data(aqm.get_last_n_measurements()),
    }
    return jsonify(context)


@app.route('/api/now/')
def api_now():
    """Returns latest data from the sensor"""
    context = {
        'current': aqm.get_measurement(),
    }
    return jsonify(context)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
