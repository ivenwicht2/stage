from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import mysql.connector
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224,projection = '3d')
ax1.set_title('x')
ax2.set_title('y')
ax3.set_title('z')
ax4.set_title('orientation')

inp = input("numéro du capteur: ")

def update(frame) :


        mydb = mysql.connector.connect(     
        host="192.168.1.58",
        user="bdd",
        passwd="nqutic",
        database="xyz"
        )

        x,y,z  = [],[],[]
        mycursor = mydb.cursor()
        mycursor.execute('Select * from data where id = {} order by count DESC  limit 20'.format(inp))
        data = mycursor.fetchall()
        for item in data :
                x.insert(0,int(item[1]))
                y.insert(0,int(item[2]))
                z.insert(0,int(item[3]))
        count = list(range(len(x)))

        ax1.clear()
        ax2.clear()
        ax3.clear()

        ax1.plot(count,x)
        ax2.plot(count,y)
        ax3.plot(count,z)

        
        arX = x.pop()
        arY = y.pop()
        arZ = z.pop()
        
        Az = int(arZ) - 1974
        Ax = int(arX) - 1958

        angle = math.atan2(Ax, -1*Az) * (180 / math.pi)

        ax4.clear()
        ax4.quiver(0,0,0,arX,arY,arZ)
        ax4.set_xlim([-1000,1000])
        ax4.set_ylim([-1000,1000])
        ax4.set_zlim([-1000,1000])
        """ 
        for angle in range(0, 360):
            ax4.view_init(30, angle)
            plt.draw()
            plt.pause(.001)
        """  
animation = FuncAnimation(fig ,update, interval=1000)
plt.show()
