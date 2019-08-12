import paho.mqtt.client as mqtt
import mysql.connector
import json
from datetime import date, datetime

mydb = mysql.connector.connect(
       host="localhost",
       user="theo",
       passwd="root",
       database="interface"
        )

def date_diff(data):
    return  ((datetime.utcnow()-data).total_seconds())
	 


def load_device():
        mycursor = mydb.cursor()
        mycursor.execute("SELECT numCapteur,port FROM device")
        myresult = mycursor.fetchall()
        dev = {}
        for item in myresult:
            i = ""
            for _ in range(6-len(item[0])) :
                i+="0"
            correction = i+item[0] 
            correction2 = item[1].replace(' ','_')
            correction2 = correction2.replace("'",'_')
            dev.setdefault(correction,correction2)
        return dev



def on_message(mqttsub, obj, msg):
    x = json.loads(msg.payload.decode('utf-8'))
    if x['port'] == 4  and x['dev_id'] in device : 
        msg = 13*[0]
        data = x['payload_fields']
        msg[0] = x['dev_id'] 
        msg[12] = x['counter']
        msg[1] = data.get('index1','None')
        msg[5] = data.get('value1','None')
        msg[2] = data.get('index2','None')
        msg[6] = data.get('value2','None')
        msg[3] = data.get('index3','None')
        msg[7] = data.get('value3','None')
        msg[4] = data.get('index4','None')
        msg[8] = data.get('value4','None')
        msg[9] = x['payload_fields']['presence']
        msg[10] = x["metadata"]["time"]
        gateways = x["metadata"]["gateways"]
        for gw in gateways: 
            msg[11] = gw["rssi"]
        write(msg,device[x['dev_id']].lower())
    elif x['dev_id'] in device : 
        write_HB(x)

def write(payload,table):
        mycursor = mydb.cursor()
        try:
            mycursor.execute('INSERT INTO {} (id,index1,index2,index3,index4,value1,value2,value3,value4,presence,time,rssi,counter) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(table,payload[0],payload[1],payload[2],payload[3],payload[4],payload[5],payload[6],payload[7],payload[8],payload[9],payload[10],payload[11],payload[12]))
        except Exception as e :
            print(e)
        mydb.commit()

def write_HB(x):
            mycursor = mydb.cursor()
            mycursor.execute("insert into {}_HB (id,pression,temp) values ({},{},{})".format(device[x['dev_id']].lower(),x['dev_id'],x['payload_fields']['pressure'],x['payload_fields']['temp']))
            mydb.commit()

def on_connect(mqttsub,userdata,flags,rc):
    print("Connected With Result Code " + str(rc))
    mqttsub.subscribe("+/devices/+/up",qos=1)   

def on_disconnect(mqttsub, userdata, rc):
	if rc != 0:
		print("Unexpected MQTT disconnection. Will auto-reconnect")



APPID = 'ports_v2'
PSW = 'ttn-account-v2.HYt-o3l0JrFpIl7IXtuAlIt8VHkZxbkPG34-OTeTC88'
device = load_device()
mqttsub = mqtt.Client()
mqttsub.on_connect = on_connect
mqttsub.on_message = on_message
mqttsub.on_disconnect = on_disconnect
mqttsub.username_pw_set(APPID,PSW)
mqttsub.connect("eu.thethings.network",1883,60)
mqttsub.subscribe("+/devices/+/up",qos=1)
maj = datetime.utcnow()
while True :
    mqttsub.loop_start() 
    if date_diff(maj) > 300 : 
        device = load_device()
        maj = datetime.now()
        
