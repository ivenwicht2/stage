import paho.mqtt.client as mqtt
import json
import base64
import sys 
from log_device import log_device
from datetime import datetime
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
         codrate = x["metadata"]["coding_rate"]
         data_r = x["metadata"]["data_rate"]
         freq = x["metadata"]["frequency"]
         payload_fields = x["payload_fields"]
         dtm = x["metadata"]["time"]
         gateways = x["metadata"]["gateways"]
         for gw in gateways:
                   gateway_id = gw["gtw_id"]
                   rssi = gw["rssi"]
                   channel = gw['channel']
                   timestamp = gw["timestamp"]
                   snr = gw["snr"]
                   rf_chain = gw["rf_chain"]
                   lat = gw["latitude"]
                   lon = gw["longitude"]
                   location_source = gw["location_source"]
                   dtm = dtm[0:10]+"'"+ dtm[11:19]
                   print(dtm +","+device + ","+ str(counter)  + ","+   str(base64.b64decode(payload_raw).hex())+","+str(codrate)+ ","+str(data_r)+ ","+str(freq)+ ','+str(gateway_id)+ ","+str(rssi)+','+str(channel)+','+str(timestamp)+','+str(snr)+','+str(rf_chain)+','+str(lat)+','+str(lon)+','+str(location_source)       )
                   
                    
                   

                   message = dtm + ',' + device + ","+ str(counter)  + ","+   str(base64.b64decode(payload_raw).hex())+","+str(codrate)+ ","+str(data_r)+ ","+str(freq)+','+str(gateway_id)+ ","+str(rssi)+','+str(channel)+','+str(timestamp)+','+str(snr)+','+str(rf_chain)+','+str(lat)+','+str(lon)+','+str(location_source)       
                   log_device(message,APPID)
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
