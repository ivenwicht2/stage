import os
from datetime import datetime

if not os.path.exists("log"):
     os.makedirs("log")

def log(device,timestamp):
    date = str(datetime.now())
    try :
       fichier = open("log/{}".format(date[0:10]),'r+')
    except:
       fichier = open("log/{}".format(date[0:10]),'a+')
    
    ok = 1

    for ligne in fichier : 
        if ligne.find(device) != -1 :
            ok = 0
    if ok == 1 :
        fichier.write("{} :: {}",device,timestamp)

