import json
import logging
from botocore.vendored import requests
from datetime import date, datetime
from chalice import Chalice, CORSConfig

#####
# VARS
#####
cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Accept'],
    max_age=600
    )

apiEndpoint = 'https://owner-api.teslamotors.com/api/1/'
res = {}


#####
# HELPERS
#####
def json_serial(obj):
    logger.debug('in json_serial()...')
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def return_json(statusCode, body, headers={}):
    logger.debug('in return_json()......')
    headers['Content-Type'] = 'application/json'
    headers['Access-Control-Allow-Headers'] = 'Content-Type,X-Amz-Date,Authorization,X-Api-Key'
    headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
    headers['Access-Control-Allow-Origin'] = '*'
    return {
        'statusCode': statusCode,
        'body': json.loads(json.dumps(body, default=json_serial)),
        'headers': headers}


#####
# LOGGING
#####
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


#####
# CHALICE
#####
app = Chalice(app_name="root")


#####
# ROUTES
#####
@app.route('/command/{vehicleId}/sentry_mode_off', methods=['POST'], cors=cors_config)
def vehicles_command_sentry_mode_off(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/sentry_mode_off POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'set_sentry_mode', {'on': False})
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = f'Failed to turn off sentry mode.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/sentry_mode_on', methods=['POST'], cors=cors_config)
def vehicles_command_sentry_mode_on(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/sentry_mode_on POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'set_sentry_mode', {'on': 'on'})
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = f'Failed to turn on sentry mode.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/remote_steering_wheel_heater_off', methods=['POST'], cors=cors_config)
def vehicles_command_remote_steering_wheel_heater_off(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/remote_steering_wheel_heater_off POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'remote_steering_wheel_heater_request', {'on': False})
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = f'Failed to turn off steering wheel heater.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/remote_steering_wheel_heater_on', methods=['POST'], cors=cors_config)
def vehicles_command_remote_steering_wheel_heater_on(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/remote_steering_wheel_heater_on POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'remote_steering_wheel_heater_request', {'on': True})
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = f'Failed to turn on steering wheel heater.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/remote_seat_heater_request/{seats}/{level}', methods=['POST'], cors=cors_config)
def vehicles_seat_heater_request(vehicleId, seats, level):
    global res
    seatsDict = {
        'driver': 0,
        'passenger': 1,
        'left': 2,
        'center': 4,
        'right': 5}
    levelDict = {
        'off': 0,
        'low': 1,
        'medium': 2,
        'high': 3}
    logger.info('in /command/{vehicleId}/remote_seat_heater_request/{seats}/{level} POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'remote_seat_heater_request', {'heater': seatsDict[seats], 'level': levelDict[level]})
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = f'Failed to set seat heat temperature.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/set_temps/passenger/{temp}', methods=['POST'], cors=cors_config)
def vehicles_command_set_temp_passenger(vehicleId, temp):
    global res
    logger.info('in /command/{vehicleId}/set_temps/passenger/{temp} POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'set_temps', {'driver_temp': 22.2, 'passenger_temp': temp})
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = f'Failed to set passenger temprature for HVAC.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/set_temps/driver/{temp}', methods=['POST'], cors=cors_config)
def vehicles_command_set_temp_driver(vehicleId, temp):
    global res
    logger.info('in /command/{vehicleId}/set_temps/driver/{temp} POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'set_temps', {'driver_temp': temp, 'passenger_temp': 22.2})
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = f'Failed to set driver temprature for HVAC.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/set_temps/{temp}', methods=['POST'], cors=cors_config)
def vehicles_command_set_temp(vehicleId, temp):
    global res
    logger.info('in /command/{vehicleId}/set_temps/{temp} POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'set_temps', {'driver_temp': temp, 'passenger_temp': temp})
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = f'Failed to set temprature for HVAC.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/auto_conditioning_start', methods=['POST'], cors=cors_config)
def vehicles_command_auto_conditioning_start(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/auto_conditioning_start POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'auto_conditioning_start')
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = f'Failed to turn on HVAC.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/auto_conditioning_stop', methods=['POST'], cors=cors_config)
def vehicles_command_auto_conditioning_stop(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/auto_conditioning_stop POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'auto_conditioning_stop')
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = f'Failed to turn off HVAC.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/set_charge_limit/{chargeLimit}', methods=['POST'], cors=cors_config)
def vehicles_command_set_charge_limit(vehicleId, chargeLimit):
    global res
    logger.info('in /command/{vehicleId}/set_charge_limit/{chargeLimit} POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'set_charge_limit', {'percent': chargeLimit})
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = f'Failed to set charge limit to {chargeLimit}.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/charge_max_range', methods=['POST'], cors=cors_config)
def vehicles_command_charge_max_range(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/charge_max_range POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'charge_max_range')
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to set charge standard to max.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/charge_standard', methods=['POST'], cors=cors_config)
def vehicles_command_charge_standard(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/charge_standard POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'charge_standard')
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to set charge standard.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/charge_stop', methods=['POST'], cors=cors_config)
def vehicles_command_charge_stop(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/charge_stop POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'charge_stop')
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to stop charging.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/charge_start', methods=['POST'], cors=cors_config)
def vehicles_command_charge_start(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/charge_start POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'charge_start')
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to start charging.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/charge_port_door_open', methods=['POST'], cors=cors_config)
def vehicles_command_charge_port_door_open(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/charge_port_door_open POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'charge_port_door_open')
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to open charge port door.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/charge_port_door_close', methods=['POST'], cors=cors_config)
def vehicles_command_charge_port_door_close(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/charge_port_door_close POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'charge_port_door_close')
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to close charge port door.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/open_frunk', methods=['POST'], cors=cors_config)
def vehicles_command_open_frunk(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/open_frunk POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'actuate_trunk', {"which_trunk": 'front'})
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to open frunk.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/open_trunk', methods=['POST'], cors=cors_config)
def vehicles_command_open_trunk(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/open_trunk POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'actuate_trunk', {"which_trunk": 'rear'})
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to open trunk.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/honk_horn', methods=['POST'], cors=cors_config)
def vehicles_command_honk_horn(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/honk_horn POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'honk_horn')
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to honk horn.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/flash_lights', methods=['POST'], cors=cors_config)
def vehicles_command_flash_lights(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/flash_lights POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'flash_lights')
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to flash lights.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/door_lock', methods=['POST'], cors=cors_config)
def vehicles_command_door_lock(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/door_lock POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'door_lock')
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to lock door.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/door_unlock', methods=['POST'], cors=cors_config)
def vehicles_command_door_unlock(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/door_unlock POST')
    try:
        res = command(vehicleId, app.current_request.json_body, 'door_unlock')
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to unlock door.'
        return return_json(500, res)


@app.route('/command/{vehicleId}/wake_up', methods=['POST'], cors=cors_config)
def vehicles_command_wake_up(vehicleId):
    global res
    logger.info('in /command/{vehicleId}/wake_up POST')
    try:
        res = wake(vehicleId, app.current_request.json_body)
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to wake up car.'
        return return_json(500, res)


@app.route('/vehicles', methods=['POST'], cors=cors_config)
def vehicles_list():
    global res
    logger.info('in /vehicles POST')
    try:
        res = postVehicles(app.current_request.json_body)
        return return_json(200, res)
    except Exception as e:
        logger.error(str(e))
        res['error'] = 'Failed to list vehicles'
        return return_json(500, res)


def wake(vehicleId, Params):
    bearerToken = Params['bearer_token']
    ret = requests.post(
        f'{apiEndpoint}vehicles/{vehicleId}/wake_up',
        headers={
            'Authorization': f'bearer {bearerToken}'})
    if ret.status_code == 200:
        return f'wake_up on {vehicleId} successful.'
    else:
        raise Exception(f'vehicle_id:{vehicleId}, problem with command:wake_up')


def command(vehicleId, Params, command, data={}):
    bearerToken = Params['bearer_token']
    ret = requests.post(
        f'{apiEndpoint}vehicles/{vehicleId}/command/{command}',
        data=data,
        headers={
            'Authorization': f'bearer {bearerToken}'})
    if ret.status_code == 200:
        return f'{command} on {vehicleId} successful.'
    else:
        raise Exception(f'vehicle_id:{vehicleId} problem with command:{command}')


def postVehicles(Params):
    bearerToken = Params['bearer_token']
    response = requests.get(
        f'{apiEndpoint}vehicles',
        headers={
            'Authorization': f'bearer {bearerToken}'})
    vehicles_json = response.json()
    vehicles = []
    for vehicle in vehicles_json['response']:
        vehicles.append(str(vehicle['id']))
    return vehicles
