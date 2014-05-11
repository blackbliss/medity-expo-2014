#!flask/bin/python

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
#from flask.ext.sqlalchemy import SQLAlchemy

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC

from time import sleep

""" BeagleBone Black setup """
GPIO.setup("P8_11", GPIO.OUT)
GPIO.setup("P8_03", GPIO.OUT)
ADC.setup()

""" Enable MCP9700 """
GPIO.setup("P8_03", GPIO.HIGH)


 
app = Flask(__name__, static_url_path = "")

#app.run(host='192.168.1.107', port=5001)

auth = HTTPBasicAuth()
#db = SQLAlchemy(app)

@auth.get_password
def get_password(username):
    if username == 'medity':
        return 'appengine'
    return None
 
@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
 
devices = [
    {
        'id': 1,
        'title': u'Temperature',
        'type': u'Termometer',
        'value': '20.1',
        'description': u"Read temperature in Daniele's room", 
        'parameter1': u"Test",
        'value': 1,
        'temp_on': 10,
        'temp_off': 20,
        'active': True
    },
    {
        'id': 2,
        'type': u'led',
        'title': u'LED',
        'description': u'Turn a led on', 
        'value': 1,
        'active': True
    },
    
    {
        'id': 3,
        'type': u'dimmer',
        'title': u'Dimmer',
        'description': u'Dimmer using PWM', 
        'value': 100,
        'active': True
    },
    {
        'id': 4,
        'title': u'Generic Pin',
        'type': u'pin',
        'value': 1,
        'description': u"General purpose.", 
        'parameter1': u"Test",
        'value': 0,
        'active': True
    },
]


@app.route('/remote/api/v1.0/devices/<pin_to_change>/<action>')
#@auth.login_required
def do_something(pin_to_change, action):
    pin_to_change = int(pin_to_change) #cast to integer
    
    #get the device name
    deviceName = pins[changePin]['name']
    
    
    device = filter(lambda t: t['title'] == 'Temperature', devices)
    #device[0]['value'] = "15" #request.json.get('status', device[0]['status'])
    device[0]['value'] = '4' #update the temperature
    if len(device) == 0:
        abort(404)
    return jsonify( { 'device': make_public(device[0]) } )



""" Set value for termometer """
@app.route('/remote/api/v1.0/devices/temp')
#@auth.login_required
def get_temperature():
    device = filter(lambda t: t['title'] == 'Temperature', devices)
    #device[0]['value'] = "15" #request.json.get('status', device[0]['status'])
    
    """ Read ambient temperature """
    reading = ADC.read("P9_39")
    millivolts = reading * 1800
    temp_c = "{0:.1f}".format((millivolts - 500) / 10)
    
    device[0]['value'] = str(temp_c) #update the temperature
    if len(device) == 0:
        abort(404)
    return jsonify( { 'device': make_public(device[0]) } )

""" Termostato """
@app.route('/remote/api/v1.0/devices/term' , methods = ['PUT'])
#@auth.login_required
def set_temperature():
    device = filter(lambda t: t['title'] == 'Temperature', devices)
    #device[0]['value'] = "15" #request.json.get('status', device[0]['status'])
    device[0]['value'] = '4' #update the temperature
    if len(device) == 0:
        abort(404)
    device[0]['temp_on'] = request.json.get('temp_on', device[0]['temp_on'])
    device[0]['temp_off'] = request.json.get('temp_off', device[0]['temp_off'])
    return jsonify( { 'device': make_public(device[0]) } )


def make_public(device):
    new_device = {}
    for field in device:
        if field == 'id':
            new_device['uri'] = url_for('get_device', device_id = device['id'], _external = True)
        else:
            new_device[field] = device[field]
    return new_device
    
@app.route('/remote/api/v1.0/devices', methods = ['GET'])
#@auth.login_required
def get_devices():
    return jsonify( { 'devices': map(make_public, devices) } )
 
@app.route('/remote/api/v1.0/devices/<int:device_id>', methods = ['GET'])
#@auth.login_required
def get_device(device_id):
    device = filter(lambda t: t['id'] == device_id, devices)
    if len(device) == 0:
        abort(404)
    return jsonify( { 'device': make_public(device[0]) } )
 
@app.route('/remote/api/v1.0/devices', methods = ['POST'])
@auth.login_required
def create_device():
    if not request.json or not 'title' in request.json:
        abort(400)
    device = {
        'id': devices[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        #'parameter2': request.json.get('parameter2', ""),
        'status': False
    }
    devices.append(device)
    return jsonify( { 'device': make_public(device) } ), 201
 
@app.route('/remote/api/v1.0/devices/<int:device_id>', methods = ['PUT'])
#@auth.login_required
def update_device(device_id):
    device = filter(lambda t: t['id'] == device_id, devices)
    if len(device) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'active' in request.json and type(request.json['active']) is not bool:
        abort(400)
    device[0]['title'] = request.json.get('title', device[0]['title'])
    device[0]['description'] = request.json.get('description', device[0]['description'])
    device[0]['active'] = request.json.get('active', device[0]['active'])
    device[0]['value'] = request.json.get('value', device[0]['value'])
    
    """ update led status """
    if device[0]['value'] == 1:
        GPIO.output("P8_11", GPIO.HIGH)
    elif device[0]['value'] == 0:
        GPIO.output("P8_11", GPIO.LOW)
        
    #update_status(device[0]['value']) #update led status
    return jsonify( { 'device': make_public(device[0]) } )
    
@app.route('/remote/api/v1.0/devices/<int:device_id>', methods = ['DELETE'])
@auth.login_required
def delete_device(device_id):
    device = filter(lambda t: t['id'] == device_id, devices)
    if len(device) == 0:
        abort(404)
    devices.remove(device[0])
    return jsonify( { 'result': True } )
    
def update_status(status):
    device = filter(lambda t: t['title'] == 'LED', devices)
    device[0]['value'] = '1' #update the led status
    if len(device) == 0:
        abort(404)
    return jsonify( { 'device': make_public(device[0]) } )
    
    
if __name__ == '__main__':
    app.run(host='192.168.1.107', port = 5001, debug = True)
