#!/usr/bin/python3
import paho.mqtt.client as mqtt
from tkinter import *
import json
import configparser
import pandas as pd
from datetime import date, datetime
config = configparser.ConfigParser()
config.read('config.txt')

APPEUI  = config['DEFAULT']['APPEUI']
APPID   = config['DEFAULT']['APPID']
PSW     = config['DEFAULT']['PSW']

data = pd.read_csv('capteur.csv',names=['num','Ncapteur','Nplace','Port'])
df = data.dropna()
device = {}
for col in df.Ncapteur :
        device.setdefault(col,[datetime.now(),'0',0,'0'])


def newmessage():
    text = ''
    text2= ''
    i = 16
    i2= 16
    for key in device :
        arg = device[key][1]
        if arg ==  '1' :
            time = abs((datetime.now()-device[key][0])).total_seconds()
            print("time: " + str(time) + " real_time: " + str(device[key][2]))
            if int(time) >  int(device[key][2])  : 
                    device[key][2] = int(time)
            if device[key][3] == '1':
                device[key][3] == '0'
                device[key][0] = datetime.now()
            if i % 14 == 1 : text = text + '\n'
            text = text + "  " + key + " " + str(device[key][2])
            i+=1
        if arg == '0' :
            if i2 % 14 == 1 : text2 = text2 + '\n'
            text2 = text2 + "  " + key
            i2+=1
    label2.config(text=text2,bg="red")
    label.config(text=text,bg = "green")


def on_message(mqttsub, obj, msg):
    x = json.loads(msg.payload.decode('utf-8'))
    if x['dev_id'] in device :
        device[x['dev_id']][1] = '1'
        device[x['dev_id']][3] = '1'
        newmessage()

mqttsub = mqtt.Client()
mqttsub.on_message = on_message
mqttsub.username_pw_set('ports_v2','ttn-account-v2.HYt-o3l0JrFpIl7IXtuAlIt8VHkZxbkPG34-OTeTC88')
mqttsub.connect("eu.thethings.network",1883,60)
mqttsub.subscribe("+/devices/+/up")   

rootWindow = Tk()
rootWindow.title('MQTT monitor')
rootWindow.geometry("800x200")
label = Label(rootWindow)
label.grid(row=1)
label2 = Label(rootWindow)
label2.grid(row=2)
newmessage()

mqttsub.loop_start() 
rootWindow.mainloop()
