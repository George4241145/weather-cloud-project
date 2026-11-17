import os
import json

from flask import Flask, request, jsonify
from pyowm.owm import OWM
from pyowm.commons.exceptions import NotFoundError
from prometheus_client import Gauge, generate_latest

app = Flask(__name__)
app.secret_key = '3c0716f88780d6d642330dfa3c96dbca' # md5 -s incremental-istio
owm = OWM(os.environ.get('OWM_API_KEY'))

city_metric = {
    'Austin, TX, US': Gauge('city_temp_austin_tx_us', 'Temperatures for Austin, TX, US')
}

if os.environ.get('ENABLE_TRACING', None) is not None:
    from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter
    from opencensus.ext.flask.flask_middleware import FlaskMiddleware
    from opencensus.trace import config_integration

    project = os.environ.get('PROJECT_ID')
    exporter = stackdriver_exporter.StackdriverExporter(project_id=project)
    middleware = FlaskMiddleware(app, exporter=exporter)
    config_integration.trace_integrations(["requests"])


@app.route('/api/weather', methods=['GET'])
def current_weather():
    ret = []
    mgr = owm.weather_manager()

    city_param = request.args.get('city', '').strip()[:60]
    if city_param:
        cities = {city_param: None}
    else:
        cities = city_metric

    for city, metric in cities.items():
        try:
            obs = mgr.weather_at_place(city)
        except NotFoundError:
            return jsonify({'error': 'City not found: {}'.format(city)}), 404
        w = obs.weather
        temp = w.temperature('fahrenheit')
        if metric is None:
            location = '{}, {}'.format(obs.location.name, obs.location.country)
        else:
            location = city
        conditions = {
            'location': location,
            'temp_cur': temp['temp'],
            'temp_min': temp['temp_min'],
            'temp_max': temp['temp_max'],
            'status': w.status,
            'clouds': w.clouds,
            'icon': 'https://openweathermap.org/img/w/{}.png'.format(w.weather_icon_name)
        }
        ret.append(conditions)
        if metric is not None:
            metric.set(temp['temp'])

    return jsonify(ret)


@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest()

@app.route('/version', methods=['GET'])
def version():
    return "weather-backend: single"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
