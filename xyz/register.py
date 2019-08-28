import paho.mqtt.client as mqtt
import json
import mysql.connector

def on_connect(mqttc,userdata,flags,rc):
    print("connection with code " + str(rc)) 
    mqttc.subscribe("+/devices/+/up",qos=1)

def on_disconnect(mqttc, userdata, rc):
    print("disconnection with code " + str(rc))

def on_message(mqttc, obj, msg):
        payload = json.loads(msg.payload.decode('utf-8'))
        if payload['dev_id'] == "000208" or payload['dev_id'] == "000209":
                print(['dev_id'])
                x = payload['payload_fields']['xmean']
                y = payload['payload_fields']['ymean']
                z = payload['payload_fields']['zmean']
                print(payload['dev_id']+ ' ' + str(x) + ' ' + str(y) + ' ' + str(z))
                mycursor = mydb.cursor()
                mycursor.execute('INSERT INTO data3 (id,vx,vy,vz) values ({},{},{},{})'.format(payload['dev_id'],x,y,z))
                mydb.commit()
                count +=1

mydb = mysql.connector.connect(
       host="localhost",
       user="theo",
       passwd="root",
       database="xyz"
        )



APPID = 'ports-v2'
PSW = 'ttn-account-v2.jFwbmUV-yqeQCW3q26YrW1K5T5OuPTd1HFPYLYwcRWE'



mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_disconnect = on_disconnect
mqttc.username_pw_set(APPID,PSW)
mqttc.connect("eu.thethings.network",1883,60)
mqttc.loop_forever() 

