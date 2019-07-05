#!/usr/bin/python3
import paho.mqtt.client as mqtt
from tkinter import *
import json
import configparser

config = configparser.ConfigParser()
config.read('config.txt')

APPEUI  = config['DEFAULT']['APPEUI']
APPID   = config['DEFAULT']['APPID']
PSW     = config['DEFAULT']['PSW']

device_0 = config['DEFAULT']['device'].split(',')
device = {}
for key in device_0 : device.setdefault(key,'0')


def newmessage():
    text = ''
    i = 8
    for key in device :
        if i % 7 == 1 : text = text + '\n'
        text = text + "  " + key + " " + device[key]
        i+=1
    return text


def on_message(mqttsub, obj, msg):
    x = json.loads(msg.payload.decode('utf-8'))
    if x['dev_id'] in device :
        device[x['dev_id']] = 'UP'
        message = newmessage()
        label.config(text=message)
        label.place(x= 0,y=0)

mqttsub = mqtt.Client()
mqttsub.on_message = on_message
mqttsub.username_pw_set('ports_v2','ttn-account-v2.HYt-o3l0JrFpIl7IXtuAlIt8VHkZxbkPG34-OTeTC88')
mqttsub.connect("eu.thethings.network",1883,60)
mqttsub.subscribe("+/devices/+/up")   

rootWindow = Tk()
rootWindow.title('MQTT monitor')
rootWindow.geometry("450x200")
message = newmessage()
label = Label(rootWindow, text=message)
label.place(x= 0,y=0)
mqttsub.loop_start() 
rootWindow.mainloop()
