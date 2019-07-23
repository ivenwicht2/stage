
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox as mbox
import mysql.connector
import pandas as pd

def menu():
    window = Tk()
    window.title('register console')
    window.resizable(width=False, height=False)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0,weight=2)
    Button(window, text="Device",command=lambda:device(), fg='black', bg='white',width=20, height=5).grid(column=1,row=1)
    window.grid_rowconfigure(3, weight=1)
    window.grid_columnconfigure(2,weight=2)
    window.mainloop()

def device():
    file = filedialog.askopenfile(initialdir='.',filetypes=(("csv file","*.csv"),),title='Choose a file')
    if file != None:
        data= pd.read_csv(file,usecols=[1,2,3],names=['capteur','place','port'],header=None,skiprows=2)
        data =data.dropna()
        data = data[-data['place'].str.contains("Stock")]
    mycursor = mydb.cursor()
    mycursor.execute("SELECT nom FROM port")
    myresult = mycursor.fetchall()
    mydb.commit()
    
    register(data['port'].unique(),myresult)
    for capteur,place,port in zip(data['capteur'],data['place'],data['port']) :
        register_sensor(capteur,place,port)
    print("fini")

def register(port,myresult):
    for item in port :
        seen = 0
        item = item.replace(' ','_')
        item = item.replace("'","_")
        for result in myresult :
            res = result[0].replace(' ','_')
            res = res.replace("'","_")
            if res == item.lower() : seen = 1
        if seen != 1 : register_port(item.lower())
    

def register_port(port):
    mycursor = mydb.cursor()
    sql = "INSERT INTO port (nom) VALUES (%s)"
    val = ("{}".format(port),)
    mycursor.execute(sql, val)
    port = port.replace(' ','_')
    port = port.replace("'","_")
    mycursor.execute("""CREATE TABLE {} (id VARCHAR(255),
            index1 VARCHAR(255),
            index2 VARCHAR(255),
            index3 VARCHAR(255),
            index4 VARCHAR(255),
            value1 VARCHAR(255),
            value2 VARCHAR(255),
            value3 VARCHAR(255),
            value4 VARCHAR(255),
            presence VARCHAR(255),
            time VARCHAR(255),
            rssi VARCHAR(255))""".format(port))
    mydb.commit() 

def register_sensor(capteur,place,port):
    mycursor = mydb.cursor()
    mycursor.execute( 'select numCapteur from device where numCapteur = "{}"'.format(capteur))
    myresult = mycursor.fetchall() 
    if myresult : 
        mycursor.execute("delete from device where numCapteur = '{}'".format(capteur))
    mycursor.execute('INSERT INTO device (numCapteur,place,port) VALUES ("{}","{}","{}")'.format(str(capteur),place,port))
    mydb.commit()


mydb = mysql.connector.connect(
            host="localhost",
            user="theo",
            passwd="root",
            database="interface"
            )

menu()








