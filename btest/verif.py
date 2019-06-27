import paho.mqtt.client as mqtt
import json
import base64
import sys 
from log_device import log_device
from datetime import datetime
#APPEUI = "70B3D57ED001DEAF"
#APPID  = "ports-v2"
#PSW    = 'ttn-account-v2.jFwbmUV-yqeQCW3q26YrW1K5T5OuPTd1HFPYLYwcRWE'

# distance de test
distance = 1500 
#tolerance de distance de test +/-
tolerance_d = 30 
#valeur min  de bat
bat = 250
#valeur pressure 
pressure = 1000
#valeur pressure +/-
tolerance_p = 50
#valeur max ratio
ratio = 50
#valeur temperature
temperature = 24
#tolerance de la temperature
tolerance_t = 3
#valeur min de value
value = 200

conf =[bat,distance,tolerance_d,pressure,tolerance_p,ratio,temperature,tolerance_t,value]

APPEUI  = sys.argv[2]
APPID   = sys.argv[1]
PSW     = sys.argv[3]



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
