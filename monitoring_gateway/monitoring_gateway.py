#!/usr/bin/python3
import pandas as pd
import requests
import time
from datetime import datetime
import os 
import mail

def log(gateway,port):
    if not os.path.exists("log"):
             os.makedirs("log")
    date = str(datetime.now())
    try :
        fichier = open("log/{}".format(date[0:10]),'r+')
    except:
        fichier = open("log/{}".format(date[0:10]),'a+')
    seen = 0
    for ligne in fichier :
        if ligne.find(gateway) != -1 :
                    seen = 1
    if seen == 0 :
        fichier.write("{} {} ## {}\n".format(gateway,port,str(datetime.now())))
        mail.email("la gateway {} ({}) ne fonctionne plus depuis {}".format(gateway,port,str(datetime.now())))



KEEPALIVE_TIMEOUT_S = 300
data = pd.read_csv('gateway.csv',names=['eui','port'])
gt = {}
for eui,port in zip(data.eui,data.port):
    gt.setdefault(eui,port)


while 1:
    for gateway in gt:
        resp = requests.get('http://noc.thethingsnetwork.org:8085/api/v2/gateways/'+gateway)
        if resp.status_code != 200:
            raise ApiError('GET gateways {}'.format(resp.status_code))
        delta=int(time.time()) - int(resp.json()['time'][:-9])
        if ( delta > KEEPALIVE_TIMEOUT_S ):
            log(gateway,gt[gateway])                
        time.sleep(5)
