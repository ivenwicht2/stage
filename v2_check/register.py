from tkinter import *
from tkinter import filedialog
import pandas as pd
from tkinter import messagebox as mbox
import mysql.connector

window = Tk()
window.title('register console')
window.resizable(width=False, height=False)

def menu() :
     reset()
     window.grid_rowconfigure(0, weight=1)
     window.grid_columnconfigure(0,weight=2)
     Button(window, text="Device",command=lambda:device(), fg='black', bg='white',width=20, height=5).grid(column=1,row=1)
     Button(window, text="Port",command=lambda:port(), fg='black', bg='white',width=20, height=5).grid(column=1,row=2)
     window.grid_rowconfigure(3, weight=1)
     window.grid_columnconfigure(2,weight=2)


def device():
    file = filedialog.askopenfile(initialdir='.',filetypes=(("csv file","*.csv"),),title='Choose a file')
    if file != None:
        data= pd.read_csv(file)

def port():
    reset()
    Button(window,text='home',command=lambda:menu()).grid(column=1,row=0)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0,weight=1)
   
   
    Label(window,text='Nom de gateway').grid(column=1,row=1)
    Label(window,text='ID port').grid(column=1,row=3)
    Label(window,text='PWD').grid(column=1,row=5)
    name = StringVar()
    eui = StringVar()
    pwd = StringVar()
    Entry(window, textvariable=name).grid(column=2,row=1)
    Entry(window, textvariable=eui).grid(column=2,row=3)
    Entry(window, textvariable=pwd).grid(column=2,row=5)
    window.grid_rowconfigure(6, weight=1)
    Button(window,text="save",command=lambda:register(str(name.get()),str(eui.get()),str(pwd.get()))).grid(column=1,row=7)
    
    
    window.grid_rowconfigure(9, weight=1)
    window.grid_columnconfigure(3,weight=1)

def register(name,eui,pwd):
    print(name+' '+eui+' '+pwd)
    mydb = mysql.connector.connect(
        host="localhost",
        user="theo",
        passwd="root",
        database="interface"
        )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT eui,nom FROM port")
    myresult = mycursor.fetchall()
    seen = 0;
    for item in myresult:
        if eui.find(item[0]) > -1 or nom.find(item[1]) >-1: seen = 1
    if seen == 0 :
        sql = "INSERT INTO port (nom,eui,pwd) VALUES (%s, %s, %s)"
        val = (name,eui,pwd)
        mycursor.execute(sql, val)
    else :
        mbox.showerror("Error", "eui ou nom de gateway déjà utilisé")
    mycursor.execute("CREATE TABLE {} (index1 VARCHAR(255), index2 VARCHAR(255), index3 VARCHAR(255),index4 VARCHAR(255),value1 VARCHAR(255),value2 VARCHAR(255),value3 VARCHAR(255),value4 VARCHAR(255),presence VARCHAR(255),time VARCHAR(255),rssi VARCHAR(255))".format(name))
    mydb.commit()

def reset():
    _list = window.winfo_children()
    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())
    for item in _list:
        item.destroy()

menu()
window.geometry("500x500")
window.mainloop()

