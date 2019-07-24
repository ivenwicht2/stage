from tkinter import *
import tkinter as tk
from bdd import *
class Port():
    def __init__(self,window,txt,colonne,ligne):
        self.txt = txt
        self.frame = Frame(window)
        self.frame.grid(column=colonne,row=ligne)
        self.button = Button(self.frame,text=txt, fg='black',command=lambda : self.fen(), bg='white',width=20,height=5).grid(row = 0 ,column = 0)
    
    def fen (self):
        try:
            self.top=Toplevel(self.frame)
            self.top.resizable(width=False, height=False)
            self.top.title("{}".format(self.txt))
            self.top.geometry("670x500")
            self.device = Frame(self.top)
            self.device.grid(column=0,row=0)
            etat = Frame(self.top).grid(column=1)
            self.dev()
        except Exception as e :
            print(e)


    def dev(self):
        self.mydb = Dtb()
        alldevice = self.mydb.execute('select numCapteur from device where port = "{}"'.format(self.txt))
        scrollbar = Scrollbar(self.device)
        scrollbar.pack( side = RIGHT,fill = Y )
        canva = tk.Canvas(self.device, yscrollcommand=scrollbar.set,width=645,height=500)
        canva.pack()
        frame = tk.Frame(canva,width=700,height=50)
        ligne = 0
        for item in alldevice:
            info = self.payload(item[0])
            Label(frame,text="{}".format(item[0]), fg='white',bg='blue',width=5,height=2).grid(column=0,row=ligne) 
            if info :
                try :
                    Label(frame,text="{}".format(info[1]),fg='black',bg='white',width=5,height=2).grid(column=1,row=ligne)
                    Label(frame,text="{}".format(info[2]),fg='black',bg='white',width=5,height=2).grid(column=2,row=ligne)
                    Label(frame,text="{}".format(info[3]),fg='black',bg='white',width=5,height=2).grid(column=3,row=ligne)
                    Label(frame,text="{}".format(info[4]),fg='black',bg='white',width=5,height=2).grid(column=4,row=ligne)
                    Label(frame,text="{}".format(info[5]),fg='black',bg='white',width=5,height=2).grid(column=5,row=ligne)
                    Label(frame,text="{}".format(info[6]),fg='black',bg='white',width=5,height=2).grid(column=6,row=ligne)
                    Label(frame,text="{}".format(info[7]),fg='black',bg='white',width=5,height=2).grid(column=7,row=ligne)
                    Label(frame,text="{}".format(info[8]),fg='black',bg='white',width=5,height=2).grid(column=8,row=ligne)
                    Label(frame,text="{}".format(info[9]),fg='black',bg='white',width=5,height=2).grid(column=9,row=ligne)
                    Label(frame,text="{}".format(info[10]),fg='black',bg='white',width=30,height=2).grid(column=10,row=ligne)
                    Label(frame,text="{}".format(info[11]),fg='black',bg='white',width=5,height=2).grid(column=11,row=ligne)
                except Exception as e:
                     print(e)
            ligne +=1


        scrollbar.config(command=canva.yview)
        canva_window = canva.create_window( 0, 0, anchor=tk.NW, window=frame)

    def payload(self,item):
        info = []
        item = self.mydb.execute('select  * from {} where id = {} order by time limit 1'.format(self.txt,item) )
        if item :
            for i in item[0] :
                info.append(i)
            return info
        else : return item 











    


