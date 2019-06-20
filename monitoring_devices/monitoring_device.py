import mysql.connector
from datetime import datetime
from log_device import log 
sql = mysql.connector.connect(host="localhost",
                               user="theo", password="root", 
                               database="test")
cursor = sql.cursor()
  
cursor.execute("show tables")
tables = []
for rcv in cursor:
      print("{}".format(rcv[0]))
      if rcv[0].find("harbour") == -1 :
          tables.append(rcv)
for el in tables :
      
    cursor.execute("SELECT * FROM `{}` WHERE `device_id` is not null".format(el[0]))
    for (_,_,_,device,rcv) in cursor:
              time = (datetime.now()-rcv).total_seconds()
              print("{}, {},      {}".format(device,rcv,time))
              if time > 600 : log(device,rcv)
                          

sql.close()
