import paho.mqtt.client as mqtt
import json
import base64
import sys 
from log_device import log_device
#APPEUI = "70B3D57ED001DEAF"
#APPID  = "ports-v2"
#PSW    = 'ttn-account-v2.jFwbmUV-yqeQCW3q26YrW1K5T5OuPTd1HFPYLYwcRWE'

APPEUI  = sys.argv[2]
APPID   = sys.argv[1]
PSW     = sys.argv[3]


def on_connect(mqttc, mosq, obj,rc):
    print("Connected with result code:"+str(rc))
    mqttc.subscribe('+/devices/+/up')
def on_message(mqttc,obj,msg):
    try:
         x = json.loads(msg.payload.decode('utf-8'))
         device = x["dev_id"]
         counter = x["counter"]
         payload_raw = x["payload_raw"]
         payload_fields = x["payload_fields"]
         datetime = x["metadata"]["time"]
         gateways = x["metadata"]["gateways"]
         for gw in gateways:
                   gateway_id = gw["gtw_id"]
                   rssi = gw["rssi"]
                   print(datetime + ", " + device + ", " + str(counter) + ", "+ gateway_id + ", "+ str(rssi) + ", " + str(payload_fields)+", "+ str(base64.b64decode(payload_raw).hex()))
                   log_device(str(device),str(base64.b64decode(payload_raw).hex()),str(APPID))
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
