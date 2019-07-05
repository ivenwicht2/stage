#!/usr/bin/python3
import paho.mqtt.client as mqtt
from tkinter import *
import json


device = {'000262':'0','000448':'0','000251':'0'}


def newmessage():
    text = ''
    for key in device :
        if device[key] == '1':
            text = text + key + '    '  + device[key] + '\n'
        if device[key] == '0':
            text = key + '    ' + device[key] + '\n' + text
    return text


def on_message(mqttsub, obj, msg):
    x = json.loads(msg.payload.decode('utf-8'))
    if x['dev_id'] in device :
        device[x['dev_id']] = '1'
        message = newmessage()
        label.config(text=message)
mqttsub = mqtt.Client()
mqttsub.on_message = on_message
mqttsub.username_pw_set('ports_v2','ttn-account-v2.HYt-o3l0JrFpIl7IXtuAlIt8VHkZxbkPG34-OTeTC88')
mqttsub.connect("eu.thethings.network",1883,60)
mqttsub.subscribe("+/devices/+/up")  # CHANGE ME 

rootWindow = Tk()
rootWindow.title('MQTT monitor')
rootWindow.geometry("500x500")
message = newmessage()
label = Label(rootWindow, text=message)
label.place(x= 0,y=0)
mqttsub.loop_start() # Don't use loop_forever() as it blocks.
rootWindow.mainloop()
