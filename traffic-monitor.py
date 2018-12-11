#!/usr/bin/env python3

import asyncio
import grovepi
import math
import json 

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

endpoint = "a2i9jv9wdklrfp-ats.iot.eu-west-2.amazonaws.com"
rootCAPath = "./root-CA.crt"
certificatePath = "./traffic-monitor.cert.pem"
privateKeyPath = "./traffic-monitor.private.key"
clientID = "traffic-monitor"

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientID)
myAWSIoTMQTTClient.configureEndpoint(endpoint, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

myAWSIoTMQTTClient.connect()

analogPins = {
    'airQuality': 0
}

digitalPins = {
    'tempAndHumidity': 4,
    'waterSensor': 2
}

grovepi.pinMode(analogPins.get('airQuality'), 'INPUT')
grovepi.pinMode(digitalPins.get('waterSensor'), 'INPUT')

def init():
    if myAWSIoTMQTTClient.publish('messages/status', json.loads('Traffic monitor started & connected!'), 1)
        print("published successfully")
    else:
        print("Couldn't publish message")
    
    print('started!')
    getEnvironmentData()

def getEnvironmentData():
    temperature, humidity = getTemperatureAndHumidity()
    data = {
        'airQuality': getAirQuality(),
        'temperature': temperature,
        'humidity': humidity,
        'water': getWater()
    }

    for key, value in data.items():
        if value == None:
            print('Error with ' + key + ' value. It equals none.')
            return
    
    sendDataOverMQTT(data)

def sendDataOverMQTT(data):
    for key, value in data.items():
        print('key: ' + key + ' is value: ' + str(value))
    print('send data here')

def getAirQuality():
    try:
        return grovepi.analogRead(analogPins.get('airQuality'))
    except IOError:
        print('IO Error')
        return None

def getTemperatureAndHumidity():
    try:
        [temp, humidity] = grovepi.dht(digitalPins.get('tempAndHumidity'), 0)

        if math.isnan(temp) == False and math.isnan(humidity) == False:
            return temp, humidity
        else:
            return None, None
    except IOError: 
        print('IO Error')
        return None, None

def getWater():
    try: 
        return grovepi.digitalRead(grovepi.digitalRead(digitalPins.get('waterSensor')))
    except IOError:
        print('IO Error')
        return None

init()