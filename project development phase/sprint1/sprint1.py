import requests as req
import json
import os
import ibmiotf.application
import ibmiotf.device
from datetime import datetime as dt
import time
import sys

# Weather Details 
api_key = "fb12afe2efc8992de27da4156f22f05a"
city = "Chennai"
country = "IN"
url_w=f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric"

# Cloud Details for weather
org_id_w = "nbl97v"
device_type_w = "weather"
device_id_w = "weather_id_1"
auth_method_w = "token"
auth_token_w = "Kanish@2002"

# Cloud Details for speed limit
org_id_s = "bhan09"
device_type_s = "Speed"
device_id_s = "Speed_limit"
auth_method_s = "token"
auth_token_s = "Jegadees_001"

location_info = {
     "school" : {
        "school_zone" : True,
        "active_time" : ["7:00","17:30"]
        },
    "hospitals_near_by" : False,
    "usual_speed_limit" : 40
    }


def get_weather_details():    
    weather_req = req.get(url = url_w)
    weather_data = weather_req.json()

    climate = weather_data['weather'][0]['main']
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    temperature = weather_data['main']['temp']
    temperature_min = weather_data['main']['temp_min']
    temperature_max = weather_data['main']['temp_max']
    temperature_feel = weather_data['main']['feels_like']
    temperature_average = (temperature_max+ temperature_min)/2
    data = {"climate":climate,"humidity":humidity,"temperature_average":temperature_average}
    return data

def myonpublishcallback_w(data):
    print(f"Published Temperature  = { data['temperature_average'] }, Humidity = {data['humidity']}, Climate = {data['climate']}")

def myonpublishcallback_s(speed):
    print(f"Published Speed limit  = { speed['speed'] }")


def speed_process(climate):
    if climate is 'rain':
        return {"speed":location_info["usual_speed_limit"]*0.3}
    elif climate is 'snow':
        return {"speed":location_info["usual_speed_limit"]*0.6}
    else:
        return {"speed":location_info["usual_speed_limit"]}

# Connecting to weather cloud
try:
    deviceOptions_w = {"org" : org_id_w, 
                     "type" : device_type_w,
                     "id" : device_id_w,
                     "auth-method" : auth_method_w,
                     "auth-token" : auth_token_w
                    }
    deviceCli_w = ibmiotf.device.Client(deviceOptions_w)
except Exception as e:
    print(f"Caught exception connecting device {str(e)}")
    sys.exit()
deviceCli_w.connect()

#connecting to speed limit
try:
    deviceOptions_s = {"org" : org_id_s, 
                     "type" : device_type_s,
                     "id" : device_id_s,
                     "auth-method" : auth_method_s,
                     "auth-token" : auth_token_s
                    }
    deviceCli_s = ibmiotf.device.Client(deviceOptions_s)
except Exception as e:
    print(f"Caught exception connecting device {str(e)}")
    sys.exit()
deviceCli_s.connect()

# Processing
while True:
    data = get_weather_details()
    success_w = deviceCli_w.publishEvent("Current Weather","json",data,qos=1,on_publish = myonpublishcallback_w(data))
    speed = speed_process(data['climate'])
    success_s = deviceCli_s.publishEvent("Speed Limit","json",speed,qos=1,on_publish = myonpublishcallback_s(speed))
    if not success_w and not success_s:
        time.sleep(1)
