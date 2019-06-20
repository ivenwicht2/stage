#!/usr/bin/python3
import requests
import time
from datetime import datetime
import os 
import mail

def log(gateway):
    date = datetime.now()
    date = date.timetuple()
    name = str(date[0]) + str(date[1]) + str(date[2])
    file = open('{}'.format(name),'a+')
    now = datetime.now()
    now = now.timetuple()
    vide = os.path.getsize('{}'.format(name))  
    if vide == 0 :
        error = "{} ".format(gateway) + str(now[0]) + str(now[1]) + str(now[2]) + str(now[3]) + str(now[4]) + str(now[5]) + "\n"
        file.write(error)
        file.close()
        mail.email("la gateway {} ne fonctionne plus".format(gateway)) 
    else :
        for line in file :
            if line.find(gateway) == -1 :
                error = "{} ".format(gateway) + str(now[0]) + str(now[1]) + str(now[2]) + str(now[3]) + str(now[4]) + str(now[5]) + "\n"
                file.write(error)
                file.close()
                mail.email("la gateway {} ne fonctionne plus".format(gateway)) 



KEEPALIVE_TIMEOUT_S = 300
GATEWAY_ID = ""
refresh = 301
while 1:

    if refresh > 300:
        fichier = open('gateway')
        Gateway_ID = [line.rstrip('\n') for line in fichier]
        fichier.close()
        for gateway in Gateway_ID:
                resp = requests.get('http://noc.thethingsnetwork.org:8085/api/v2/gateways/'+gateway)
                if resp.status_code != 200:
                    raise ApiError('GET gateways {}'.format(resp.status_code))
 
                delta=int(time.time()) - int(resp.json()['time'][:-9])
 
                if ( delta > KEEPALIVE_TIMEOUT_S ):
                    log(gateway)
                    print(gateway)
                
    time.sleep(5)
    refresh += 5
