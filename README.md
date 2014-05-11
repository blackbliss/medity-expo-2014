Medity Expò 2014 DEMO
=====================

#### Example ####

	curl -i http://localhost:5000/remote/api/v1.0/devices

	{
		"devices": [
		{
			"active": true,
			"description": "Read temperature in Daniele's room",
			"parameter1": "Test",
			"status": false,
			"title": "Temperature",
			"type": "Termometer",
			"uri": "http://localhost:5000/remote/api/v1.0/devices/1",
			"value": "20.1"
		},
		{
			"active": true,
			"description": "Turn a led on",
			"status": false,
			"title": "LED ON",
			"type": "led",
			"uri": "http://localhost:5000/remote/api/v1.0/devices/2"
		},
		{
			"active": true,
			"description": "Dimmer using PWM",
			"status": false,
			"title": "Dimmer",
			"type": "dimmer",
			"uri": "http://localhost:5000/remote/api/v1.0/devices/3",
			"value": 100
		},
		{
			"active": true,
			"description": "General purpose.",
			"parameter1": "Test",
			"status": false,
			"title": "Generic Pin",
			"type": "pin",
			"uri": "http://localhost:5000/remote/api/v1.0/devices/4",
			"value": 1
		}
		]
	}
  



#### Luce ambientale (possibilità di spegnere/accendere e prendere lo stato corrente) ####

**GET**
	
	curl -i http://localhost:5000/remote/api/v1.0/devices/2

**PUT** *(value = 1 | value = 0)*
	
	curl -i -H "Content-Type: application/json" -X PUT -d '{"value":1}' 	http://localhost:5000/remote/api/v1.0/devices/2


#### Un termostato con sensore di temperature (possibilità di ottenere la temperatura e di settare la temperatura di accensione del termostato) ####

**GET**
	
	curl -i http://localhost:5000/remote/api/v1.0/devices/1

**PUT** *(temp_on and temp_off)*

	curl -i -H "Content-Type: application/json" -X PUT -d '{"temp_on":1, "temp_off":10}' http://localhost:5000/remote/api/v1.0/devices/term


#### [Generico] Ottenere lo stato di una presa comandata ####

**GET**
	
	curl -i http://localhost:5000/remote/api/v1.0/devices/4

**PUT** *(value = 1 | value = 0)*

	curl -i -H "Content-Type: application/json" -X PUT -d '{"value":1}' 	http://localhost:5000/remote/api/v1.0/devices/4


#### [Generico] Dimmer ####

**GET**
	
	curl -i http://localhost:5000/remote/api/v1.0/devices/3

**PUT** *(values from 1 up to 256)*
	
	curl -i -H "Content-Type: application/json" -X PUT -d '{"value":1}' http://localhost:5000/remote/api/v1.0/devices/3


