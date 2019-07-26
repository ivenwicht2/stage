import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from bdd import *
from tkinter import *

def data_log(ligne,device,port,frame):
    mydb = Dtb()
    data = mydb.execute('select id,index1,index2,index3,index4,value1,value2,value3,value4,counter from {} where id = {} limit 240 '.format(port,device))
    Button(frame,text="log",command = lambda:graphic(data)).grid(column=12,row=ligne)

import numpy as np
def graphic(log):
    index1=[]
    index2=[]
    index3=[]
    index4=[]
    counter=[] 
    N = 0
    for item in log :
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




