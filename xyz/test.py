import math
import collections
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import mysql.connector

app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')
# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)
p6 = win.addPlot(title="accelerometer yaw")
p6.setLabel('left', 'rotation in degrees')
curve = p6.plot(pen='y')
# collections is a module which provides high performance container datatypes.
# deque object can be used as a queue with fast appends and pops to either end of the queue
data = collections.deque(100*[1250], 100)
ptr = 0
def update():
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="theo",
        passwd="root",
        database="xyz"
        )
        mycursor = mydb.cursor()
        mycursor.execute('Select * from data3 where id = 000208 order by count DESC limit 1')
        dt = mycursor.fetchall()
        print(dt)
        global curve, data, ptr, p6
        # get data from edison server. Here, 3-axis accelerometer reading is being received. However, in general, it can be any data read from a sensor connected to edison.
        # note: the setup is such that edison sends the three axis readings as space seperated values ex: "1300 1500 1350"
        print(dt)
        az = dt[0][3]
        ay = dt[0][2]
        ax = dt[0][1]
        # subtract the x-axis and y-axis  offsets calculated using calibration program.
        Az = int(az)  
        Ax = int(ax) 
        # convert accelerometer readings to angle in radians and then convert radians to degrees 
        angle = math.atan2(Ax, -1*Az) * (180 / math.pi)
        # append the angle data point to queue
        data.appendleft(angle)
        # convert the queue into an array
        plot_data = np.array(data)
        # modify the curve with the modified array with the new angle reading
        curve.setData(plot_data)
    finally:
        # initialize timer
        timer = QtCore.QTimer()
        # recursively call the update() function every 50 milli-seconds
        # this causes a new angle reading to be added to the graph periodically
        timer.singleShot(12000, update)
update()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

