import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from bdd import *
from tkinter import *
import numpy as np

class graphe :
    def __init__(self,ligne,device,port,frame):
        mydb = Dtb()
        self.data = mydb.execute('select id,index1,index2,index3,index4,value1,value2,value3,value4,counter from {} where id = {} limit 240 '.format(port,device))
        self.data_hb = mydb.execute('select * from {}_HB where id = {} limit 40 '.format(port,device))
        Button(frame,text="log",command = lambda:self.graphic_data()).grid(column=12,row=ligne)
        Button(frame,text="HB",command = lambda:self.graphic_hb()).grid(column=13,row=ligne)

    def graphic_data(self):
        index1=[]
        index2=[]
        index3=[]
        index4=[]
        counter=[] 
        N = 0
        for item in self.data :
            id1 = 0
            id2 = 0
            id3 = 0
            id4 = 0
            if str(item[5]) != 'None' : id1 = item[5] 
            if str(item[6]) != 'None' : id2 = item[6] 
            if str(item[7]) != 'None' : id3 = item[7] 
            if str(item[8]) != 'None' : id4 = item[8] 
            index1.append(int(id1))
            index2.append(int(id2))
            index3.append(int(id3))
            index4.append(int(id4))
            counter.append(int(item[9]))
            N += 1
        index = pd.Index(counter, name='counter')
        data = {'index1':index1,'index2':index2,'index3':index3,'index4':index4}
        df = pd.DataFrame(data, index=index)
        ax = df.plot(kind='bar', stacked=True, figsize=(18.5, 10.5))
        ax.set_ylabel('foo')
        plt.savefig('stacked.png')
        plt.show()
   
    def graphic_hb(self):
            pressure = []
            temp = []
            ratio = []
            for item in self.data_hb:
                pressure.append(int(item[1]))
                temp.append(int(item[2]))
                rt = int(item[1])/int(item[2])
                ratio.append(float(rt))
            iterable =  np.arange(len(pressure))
            plt.title("HeartBeat")
            plt.scatter(iterable,pressure,c='blue',label = "pressure")
            plt.scatter(iterable,temp,c='red',label = "temp")
            plt.scatter(iterable,ratio,c='yellow',label = "ratio")
            plt.legend()
            plt.xlabel('')
            plt.ylabel('')
            plt.show()





