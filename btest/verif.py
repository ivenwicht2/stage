import paho.mqtt.client as mqtt
import json
import base64
import sys 
import configparser
from datetime import datetime
from log_device import log_device


config = configparser.ConfigParser()
config.read('config.txt')

print("prise en compte de la configuration")
bat = int(config['DEFAULT']['bat'])
distance = int(config['DEFAULT']['distance'])
tolerance_d =int(config['DEFAULT']['tolerance_d'])
pressure = int(config['DEFAULT']['pressure'])
tolerance_p = int(config['DEFAULT']['tolerance_p'])
ratio = int(config['DEFAULT']['ratio'])
temperature = int(config['DEFAULT']['temperature'])
tolerance_t =  int(config['DEFAULT']['tolerance_t'])
value = int(config['DEFAULT']['value'])

conf =[bat,distance,tolerance_d,pressure,tolerance_p,ratio,temperature,tolerance_t,value]

APPEUI  = config['DEFAULT']['APPEUI']
APPID   = config['DEFAULT']['APPID']
PSW     = config['DEFAULT']['PSW']

print("configuration prise en compte..")

def on_connect(mqttc, mosq, obj,rc):
    print("Connected with result code:"+str(rc))
    mqttc.subscribe('+/devices/+/up')
def on_message(mqttc,obj,msg):
    try:
         x = json.loads(msg.payload.decode('utf-8'))
         #if int(x['port']) == 128 : print(x)
         log_device(x,APPID,conf)               

    except Exception as e:
         print(e)
         pass
def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc,obj,level,buf):
    print("message:" + str(buf))
    print("userdata:" + str(obj))

mqttc= mqtt.Client()
mqttc.on_connect=on_connect
mqttc.on_message=on_message
mqttc.username_pw_set(APPID, PSW)
mqttc.connect("eu.thethings.network",1883,60)
while True:
      mqttc.loop()
