import datetime
import json
import base64

def log_device(x,pt):
    
   # print(x)
    ok = "OK"
    date = datetime.datetime.now()
    if x["port"]==128:
        if int(x["payload_fields"]["bat"])<250: 
            ok = "NOK"
            print("error  bat:      {}".format(x["payload_fields"]['bat']))
        if int(x["payload_fields"]['hour'])!=date.hour : 
            ok = "NOK"
            print("error  hour:     {}".format(x["payload_fields"]['hour']))
        if int(x['payload_fields']['minute']) > date.minute + 5 or int(x["payload_fields"]['minute']) < date.minute -5 : 
            ok = "NOK"
            print("error  minute:   {}".format(x["payload_fields"]['minute']))
        if int(x["payload_fields"]['presence']) != 1 : 
            ok = "NOK"
            print("error  presence: {}".format(x["payload_fields"]['hour']))
        if int(x["payload_fields"]['pressure']) < 950 or int(x["payload_fields"]['pressure']) > 1040 : 
            ok = "NOK"
            print("error pressure:  {}".format(x["payload_fields"]['pressure']))
        if int(x["payload_fields"]['ratio']) > 50 : 
            ok = "NOK"
            print("error ratio:     {}".format(x["payload_fields"]['ratio']))
        hexa = str(base64.b64decode(x['payload_raw']).hex())
        nomb = (len(hexa) - 14)//4
        for i in range(nomb):
            index = int( hexa[2+(i*4): 4+(i*4)],16 )
            value = int(hexa[4+(i*4):6+(i*4)],16)
            if (value*16*2.137) > 8000 : 
                ok ="NOK"
                print("error index: {} {}".format(i,index))
            if value > 255 : 
                ok = "NOK"
                print("error value: {} {}".format(i,value))
    
                

        print(x['dev_id'] + ' {}'.format(ok)) 

        #message = x['dev_id'] + ' {} '.format(ok) + x 
        #files = open('{}.txt'.format(pt),'a')
        #files.write("{}\n".format(message))
        #files.close()
