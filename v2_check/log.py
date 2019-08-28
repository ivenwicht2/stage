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
        first = self.mydb.execute('select counter from {} where id = {} order by time DESC limit 1'.format(self.port,self.device ))
        self.data = self.mydb.execute('select id,index1,index2,index3,index4,value1,value2,value3,value4,counter from {} where id = {} and counter <= {} and counter > {}-50 order by time DESC limit 240 '.format(self.port,self.device,first[0][0],first[0][0]))
        real_data = []
        dn = 0
        for i in range(0,51):
            if i < len(self.data):
                if int(self.data[dn][9]) == int(first[0][0]) - i :
                    real_data.append([self.data[dn][0],self.data[dn][1],self.data[dn][2],self.data[dn][3],self.data[dn][4],self.data[dn][5],self.data[dn][6],self.data[dn][7],self.data[dn][8],self.data[dn][9]])
                    dn +=1
                else :
                    real_data.insert(0,[0,0,0,0,-200,0,0,0,0,int(first[0][0])-i])
            else : real_data.insert(0,[0,0,0,0,-200,0,0,0,0,int(first[0][0])-i]) 
        index1=[]
        index2=[]
        index3=[]
        index4=[]
        counter=[] 
        c1 = []
        c2 = []
        c3 = []
        c4 = []
        N = 0
        r=[]
        dt=[0,0,0,0,0,0,0,0]
        
        for item in real_data :
            if str(item[1]) != 'None' : dt[0] = int(item[1])
            if str(item[2]) != 'None' : dt[1] = int(item[2]) 
            if str(item[3]) != 'None' : dt[2] = int(item[3]) 
            if str(item[4]) != 'None' : dt[3] = int(item[4]) 
            if str(item[5]) != 'None' : dt[4] = int(item[5])
            if str(item[6]) != 'None' : dt[5] = int(item[6])
            if str(item[7]) != 'None' : dt[6] = int(item[7])
            if str(item[8]) != 'None' : dt[7] = int(item[8])
            
        
            c1.append(dt[4])
            c2.append(dt[5])
            c3.append(dt[6])
            c4.append(dt[7])
            index1.append(int(dt[0]))
            index2.append(int(dt[1]))
            index3.append(int(dt[2]))
            index4.append(int(dt[3]))
            counter.append(int(item[9]))
            r.append(N)
            N += 1
         
        limit = [0,254]
        normalize = matplotlib.colors.Normalize(vmin=min(limit), vmax=max(limit))
        cmap = matplotlib.cm.get_cmap('jet')
        fig,ax = plt.subplots(figsize=(10,10))
        colors1 = [cmap(normalize(value)) for value in c1]
        colors2 = [cmap(normalize(value)) for value in c2]
        colors3 = [cmap(normalize(value)) for value in c3]
        colors4 = [cmap(normalize(value)) for value in c4]
        rc('font', weight='bold')
        barWidth = 1
        b1 = plt.bar(r, index4, color=colors4, edgecolor='white', width=barWidth)
        b2 = plt.bar(r, index3, color=colors3, edgecolor='white', width=barWidth)
        b3 = plt.bar(r, index2, color=colors2, edgecolor='white', width=barWidth)
        b4 = plt.bar(r, index1, color=colors1, edgecolor='white', width=barWidth)
        plt.xticks(r, counter, fontweight='bold',rotation='vertical')
        plt.xlabel("counter")
        plt.ylabel("index")
        plt.title(self.device)
        cax, _ = matplotlib.colorbar.make_axes(ax)
        cbar = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap, norm=normalize)
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()

    def log_index(self):
        data_index = self.mydb.execute('select * from {} where id = {} order by time DESC limit 20 '.format(self.port,self.device))
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
        Label(top,text='p',bg='white').grid(column=9,row=0)
        Label(top,text='time',bg='white').grid(column=10,row=0)
        Label(top,text='rssi',bg='white').grid(column=11,row=0)
        Label(top,text='counter',bg='white').grid(column=12,row=0)
        ligne = 1
        for item in data_index : 
            Label(top,text=item[0],bg='white').grid(column=0,row=ligne)
            Label(top,text=item[1],bg='white').grid(column=1,row=ligne)
            Label(top,text=item[2],bg='white').grid(column=2,row=ligne)
            Label(top,text=item[3],bg='white').grid(column=3,row=ligne)
            Label(top,text=item[4],bg='white').grid(column=4,row=ligne)
            Label(top,text=item[5],bg='white').grid(column=5,row=ligne)
            Label(top,text=item[6],bg='white').grid(column=6,row=ligne)
            Label(top,text=item[7],bg='white').grid(column=7,row=ligne)
            Label(top,text=item[8],bg='white').grid(column=8,row=ligne)
            Label(top,text=item[9],bg='white').grid(column=9,row=ligne)
            time = str(item[10])
            time = time[:19].replace('T','//')
            Label(top,text=time,bg='white').grid(column=10,row=ligne)
            Label(top,text=item[11],bg='white').grid(column=11,row=ligne)
            Label(top,text=item[12],bg='white').grid(column=12,row=ligne)
            ligne += 1
    


   
    def graphic_hb(self):
        data_hb = self.mydb.execute('select * from {}_HB where id = {} limit 40 '.format(self.port,self.device))
        pressure = []
        temp = []
        for item in data_hb:
            pressure.append(int(item[1]))
            temp.append(float(item[2]))
            rt = int(item[1])/float(item[2])

        x =  np.arange(len(pressure)) 


        fig, ax1  =  plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('Trame')
        ax1.set_ylabel('Pressure', color=color)
        ax1.plot(x, pressure, color=color)
        ax1.tick_params(axis='y', labelcolor=color)
	
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
	
        color = 'tab:blue'
        ax2.set_ylabel('Température', color=color)  # we already handled the x-label with ax1
        ax2.plot(x, temp, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
	
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()





















