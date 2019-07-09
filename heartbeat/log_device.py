import datetime
import json
import base64

def log_device(x,pt):
        files = open('{}.txt'.format(pt),'a')
        files.write("{}\n".format(x))
        files.close()
