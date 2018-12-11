#!/usr/bin/env python

import asyncio
import grovepi
import math

analogPins = {
    'airQuality': 0
}

digitalPins = {
    'tempAndHumidity': 4,
    'waterSensor': 2
}

grovepi.pinMode(analogPins.get('airQuality'), 'INPUT')
grovepi.pinMode(digitalPins.get('waterSensor'), 'INPUT')

init()

def init():
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
        else 
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

