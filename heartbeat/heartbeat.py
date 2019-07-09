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
        if int(x['port']) == 190 : 
            log_device(x,APPID)               
            print(x)
    except Exception as e:
         print(e)
         pass


mqttc= mqtt.Client()
mqttc.on_connect=on_connect
mqttc.on_message=on_message
mqttc.username_pw_set(APPID, PSW)
mqttc.connect("eu.thethings.network",1883,60)
mqttc.loop_forever() 
