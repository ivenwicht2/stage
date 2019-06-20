import mysql.connector
from datetime import datetime
from log_device import log
sql = mysql.connector.connect(host="localhost",
                               user="theo", password="root", 
                               database="test")
cursor = sql.cursor()
  
cursor.execute("SELECT * FROM `place` WHERE `device_id` is not null")
for (_,_,_,device,rcv) in cursor:
      time = (datetime.now()-rcv).total_seconds()
      print("{}, {},      {}".format(device,rcv,time))
      if time > 600 : log(device,rcv)
sql.close()
