#!/usr/bin/python3
import paho.mqtt.client as mqtt
from tkinter import *
from tkinter import *
import tkinter as tk
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
global frame

def MyLabel(master,nbc,nbr,dev,txt):
        frame = Frame(master)
        frame.grid(column=nbc,row=nbr)
        label = Label(frame, text=dev,width=6,font=('Arial', 12), fg='#88F').grid(row=0,column = 0)
        if txt  > 0 :  button=Button(frame, text=str(int(txt)), fg='white', bg='#44F',width=1).grid(row=0,column=2)
        else :  button=Button(frame, text="", fg='white', bg='red',width=1).grid(row=0,column=2)




def all_children () :
    _list = rootWindow.winfo_children()
    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list





def newmessage():
    widget_list = all_children()
    ligne = -1
    i=0
    for item in device :
        ligne += 1 
        if device[item][1] == '1' :
            if device[item][3] == '1':
                device[item][3]='0'
                device[item][0] = datetime.now()
            time = abs((datetime.now()-device[item][0])).total_seconds()
            if time > device[item][2]  :
                device[item][2] = time
            MyLabel(rootWindow,i,ligne,item,device[item][2])
        else :
            MyLabel(rootWindow,i,ligne,item,0)

        if ligne > 25 :
             i += 1
             ligne = -1
    
    for item in widget_list:
        item.destroy()


def on_message(mqttsub, obj, msg):
    x = json.loads(msg.payload.decode('utf-8'))
    if x['dev_id'] in device :
        device[x['dev_id']][1] = '1'
        device[x['dev_id']][3] = '1'
        newmessage()


mqttsub = mqtt.Client()
mqttsub.on_message = on_message
mqttsub.username_pw_set(APPID,PSW)
mqttsub.connect("eu.thethings.network",1883,60)
mqttsub.subscribe("+/devices/+/up")   

rootWindow = Tk()
rootWindow.title('MQTT monitor')
frame = Frame(rootWindow)
newmessage()
mqttsub.loop_start() 
rootWindow.mainloop()
