from tkinter import *
import tkinter as tk
from bdd import *
from datetime import datetime
import log
class Port():
    def __init__(self,window,port,colonne,ligne):
        self.port = port
        self.mydb = Dtb()
        #Supprime toutes les trames de plus de 10 jours
        self.mydb.execute("select * from {} WHERE DATE(time) < DATE(NOW() - INTERVAL 10 DAY)".format(port))
        self.frame = Frame(window)
        self.frame.grid(column=colonne,row=ligne)
        #button du port dans le menu 
        self.button = Button(self.frame,text=port, fg='black',command=lambda : self.fen(), bg='white',width=20,height=5,font='lucida').grid(row = 0 ,column = 0) 
        self.photo = PhotoImage(file='refresh.png')
    def fen (self):
        try:
            #création des fenêtres 
            self.top=Toplevel(self.frame,bg='white')
            self.top.resizable(width=False, height=False)
            self.top.title("{}".format(self.port))
            self.top.geometry("950x570")
            self.info = Frame(self.top,bg='white')
            self.info.grid(column=0,row=0,sticky="nsew")
            self.fen_frame()
        except Exception as e :
            print(e)
    def fen_frame(self):
        self.device = Frame(self.top,width=1000,height=810)
        self.device.grid(column=0,row=1,sticky="nsew")
        self.dev()

    def refresh(self):
        #refresh la page
        self.device.destroy()
        self.fen_frame()

    def myfunction(self,event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=920,height=540)
   
    def dev(self):
        #Affichage des titres
        Label(self.info,text="Device",width=10,bg='white').grid(column=0,row=0)
        Label(self.info,text="Ind1",width=10,bg='white').grid(column=1,row=0)
        Label(self.info,text="Ind2",width=5,bg='white').grid(column=2,row=0)
        Label(self.info,text="Ind3",bg='white',width=5).grid(column=3,row=0)
        Label(self.info,text="Ind4",bg='white',width=5).grid(column=4,row=0)
        Label(self.info,text="Val1",bg='white',width=5).grid(column=5,row=0)
        Label(self.info,text="Val2",bg='white',width=5).grid(column=6,row=0)
        Label(self.info,text="Val3",bg='white',width=5).grid(column=7,row=0)
        Label(self.info,text="Val4",bg='white',width=5).grid(column=8,row=0)
        Label(self.info,text="P",bg='white',width=5).grid(column=9,row=0)
        Label(self.info,text="Date",bg='white',width=30).grid(column=10,row=0)
        Label(self.info,text="RSSI",bg='white',width=5).grid(column=11,row=0)
        Button(self.info,image=self.photo,command=lambda:self.refresh(),anchor="center").grid(column=12,row=0)
        #requete pour avoir la liste des capteurs
        alldevice = self.mydb.execute('select numCapteur from device where port = "{}"'.format(self.port))
        #scrollbar
        self.canvas=Canvas(self.device)
        frame=Frame(self.canvas)
        myscrollbar=Scrollbar(self.device,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=frame,anchor='nw')
        frame.bind("<Configure>",self.myfunction)
        

        ligne = 1
        for item in alldevice:
            #affichage et colorisation en fonction du temps des label capteurs
            info = self.payload(item[0])
            if info :
                time=self.date_diff(info[10])
                if time <= 6 : Label(frame,text="{}".format(item[0]), fg='black',bg='white',width=10,height=2).grid(column=0,row=ligne) 
                elif time < 60 : Label(frame,text="{}".format(item[0]), fg='white',bg='green',width=10,height=2).grid(column=0,row=ligne) 
                else :  Label(frame,text="{}".format(item[0]), fg='white',bg='blue',width=10,height=2).grid(column=0,row=ligne) 
            else : Label(frame,text="{}".format(item[0]), fg='white',bg='red',width=10,height=2).grid(column=0,row=ligne) 

                    
            if info :
                try :
                    #trame de chaque capteurs
                    Label(frame,text="{}".format(info[1]),fg='black',bg='orange',width=10,height=2).grid(column=1,row=ligne)
                    Label(frame,text="{}".format(info[2]),fg='black',bg='orange',width=5,height=2).grid(column=2,row=ligne)
                    Label(frame,text="{}".format(info[3]),fg='black',bg='orange',width=5,height=2).grid(column=3,row=ligne)
                    Label(frame,text="{}".format(info[4]),fg='black',bg='orange',width=5,height=2).grid(column=4,row=ligne)
                    Label(frame,text="{}".format(info[5]),fg='black',bg='yellow',width=5,height=2).grid(column=5,row=ligne)
                    Label(frame,text="{}".format(info[6]),fg='black',bg='yellow',width=5,height=2).grid(column=6,row=ligne)
                    Label(frame,text="{}".format(info[7]),fg='black',bg='yellow',width=5,height=2).grid(column=7,row=ligne)
                    Label(frame,text="{}".format(info[8]),fg='black',bg='yellow',width=5,height=2).grid(column=8,row=ligne)
                    Label(frame,text="{}".format(info[9]),fg='black',bg='brown',width=5,height=2).grid(column=9,row=ligne)
                    Label(frame,text="{}".format(info[10]),fg='black',bg='green',width=30,height=2).grid(column=10,row=ligne)
                    Label(frame,text="{}".format(info[11]),fg='black',bg='purple',width=5,height=2).grid(column=11,row=ligne)
                    #bouton index log_index HB renvoie vers le fichier log.py
                    log.graphe(ligne,info[0],self.port,frame)
                except Exception as e:
                     print(e)
            ligne +=1


    def payload(self,item):
        info = []
        #requête dernière trame du capteur
        item = self.mydb.execute('select  * from {} where id = {} order by time DESC limit 1'.format(self.port,item) )
        if item :
            for i in item[0] :
                info.append(i)
            return info
        else : return item 

        

    def date_diff(self,data):
        #différence de date pour colorisation
        data=data[:-4]
        datetime_object = datetime.strptime(data,"%Y-%m-%dT%H:%M:%S.%f")
        time = ((datetime.utcnow()-datetime_object).total_seconds())/60
        return time
    





    


