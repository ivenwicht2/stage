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
    text2= ''
    i = 9
    i2= 9
    for key in device :
        arg = device[key]
        if arg == '1' :
            if i % 7 == 1 : text = text + '\n'
            text = text + "  " + key
            i+=1
        if arg == '0' :
            if i2 % 7 == 1 : text2 = text2 + '\n'
            text2 = text2 + "  " + key 
            i2+=1
    print(text)
    print('\n')
    print(text2)
    label2.config(text=text2,bg="red")
    label.config(text=text,bg = "green")


def on_message(mqttsub, obj, msg):
    x = json.loads(msg.payload.decode('utf-8'))
    if x['dev_id'] in device :
        device[x['dev_id']] = '1'
        newmessage()

mqttsub = mqtt.Client()
mqttsub.on_message = on_message
mqttsub.username_pw_set('ports_v2','ttn-account-v2.HYt-o3l0JrFpIl7IXtuAlIt8VHkZxbkPG34-OTeTC88')
mqttsub.connect("eu.thethings.network",1883,60)
mqttsub.subscribe("+/devices/+/up")   

rootWindow = Tk()
rootWindow.title('MQTT monitor')
rootWindow.geometry("500x200")
label = Label(rootWindow)
label.grid(row=1)
label2 = Label(rootWindow)
label2.grid(row=2)
newmessage()

mqttsub.loop_start() 
rootWindow.mainloop()
