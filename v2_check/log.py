import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib
import pandas as pd
from bdd import *
from tkinter import *
import numpy as np

class graphe :
    def __init__(self,ligne,device,port,frame):
        self.mydb = Dtb()
        self.port = port
        self.device = device
        self.frame = frame
        Button(frame,text="index",command = lambda:self.graphic_data()).grid(column=12,row=ligne)
        Button(frame,text="HB",command = lambda:self.graphic_hb()).grid(column=13,row=ligne)
        Button(frame,text='log_index',command=lambda:self.log_index()).grid(column=14,row=ligne)
   
    def graphic_data(self):
        self.data = self.mydb.execute('select id,index1,index2,index3,index4,value1,value2,value3,value4,counter from {} where id = {} limit 240 '.format(self.port,self.device))
        index1=[]
        index2=[]
        index3=[]
        index4=[]
        counter=[] 
        N = 0
        r=[]
        for item in self.data :
            id1 = 0
            id2 = 0
            id3 = 0
            id4 = 0
            if str(item[1]) != 'None' : id1 = item[1] 
            if str(item[2]) != 'None' : id2 = item[2] 
            if str(item[3]) != 'None' : id3 = item[3] 
            if str(item[4]) != 'None' : id4 = item[4] 
            index1.append(int(id1))
            index2.append(int(id2))
            index3.append(int(id3))
            index4.append(int(id4))
            counter.append(int(item[9]))
            r.append(N)
            N += 1

        rc('font', weight='bold')
        barWidth = 1
        b1 = plt.bar(r, index4, color='red', edgecolor='white', width=barWidth)
        b2 = plt.bar(r, index3, color='orange', edgecolor='white', width=barWidth)
        b3 = plt.bar(r, index2, color='blue', edgecolor='white', width=barWidth)
        b4 = plt.bar(r, index1, color='green', edgecolor='white', width=barWidth)

        plt.xticks(r, counter, fontweight='bold',rotation='vertical')
        plt.legend([b4, b3, b2, b1], ['index1','index2','index3','index4'])
        plt.xlabel("counter")
        plt.ylabel("index")
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()

    def log_index(self):
        data_index = self.mydb.execute('select * from {} where id = {} limit 20 '.format(self.port,self.device))
        top = Toplevel(self.frame,bg='white')
        Label(top,text='id',bg='white').grid(column=0,row=0)
        Label(top,text='index1',bg='white').grid(column=1,row=0)
        Label(top,text='index2',bg='white').grid(column=2,row=0)
        Label(top,text='index3',bg='white').grid(column=3,row=0)
        Label(top,text='index4',bg='white').grid(column=4,row=0)
        Label(top,text='value1',bg='white').grid(column=5,row=0)
        Label(top,text='value2',bg='white').grid(column=6,row=0)
        Label(top,text='value3',bg='white').grid(column=7,row=0)
        Label(top,text='value4',bg='white').grid(column=8,row=0)
        Label(top,text='presence',bg='white').grid(column=9,row=0)
        Label(top,text='time',bg='white').grid(column=10,row=0)
        Label(top,text='rssi',bg='white').grid(column=11,row=0)
        Label(top,text='counter',bg='white').grid(column=12,row=0)
        ligne = 1
        for item in data_index : 
            colone = 0
            for i in item : 
                Label(top,text = i).grid(row=ligne,column = colone)
                colone += 1
            ligne += 1

    


   
    def graphic_hb(self):
            data_hb = self.mydb.execute('select * from {}_HB where id = {} limit 40 '.format(self.port,self.device))
            pressure = []
            temp = []
            for item in data_hb:
                pressure.append(int(item[1]))
                temp.append(float(item[2]))
                rt = int(item[1])/float(item[2])
            iterable =  np.arange(len(pressure))
            """fig, ax1 = plt.subplots()
            x1 = plt.subplots()
            color = 'tab:red'
            ax1.set_xlabel('température')
            ax1.set_ylabel('', color=color)
            ax1.plot(iterable, temp, color=color)
            ax1.tick_params(axis='y', labelcolor=color)

            ax2 = ax1.twinx()
            color = 'tab:blue'
            ax2.set_ylabel('pression', color=color)  
            ax2.plot(iterable,pressure,color=color)
            ax2.tick_params(axis='y', labelcolor=color)
            fig.tight_layout()  
            plt.show()"""

            fig = plt.figure(figsize=(8, 5))
            line_weight = 3
            alpha = .5
            ax1 = fig.add_axes([0, 0, 1, 1])
            ax2 = fig.add_axes()
            # This is the magic that joins the x-axis
            ax2 = ax1.twinx()
            lns1 = ax1.plot(iterable,temp, color='blue', lw=line_weight, alpha=alpha, label='température')
            lns2 = ax2.plot(iterable,pressure, color='orange', lw=line_weight, alpha=alpha, label='pression')
            # Solution for having two legends
            leg = lns1 + lns2
            labs = [l.get_label() for l in leg]
            ax1.legend(leg, labs, loc=0)
            plt.title('Température et pression', fontsize=20)
                    
            plt.show()








