import datetime
import json
import base64

def log_device(x,pt,conf):
    
    ok = "OK"
    date = datetime.datetime.now()
    if x["port"]==128:
        if int(x["payload_fields"]["bat"])<conf[0]: 
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
        if int(x["payload_fields"]['pressure']) < conf[3] - conf[4]  or int(x["payload_fields"]['pressure']) > conf[3] + conf[4] : 
            ok = "NOK"
            print("error pressure:  {}".format(x["payload_fields"]['pressure']))
        if int(x["payload_fields"]['ratio']) > conf[5] : 
            ok = "NOK"
            print("error ratio:     {}".format(x["payload_fields"]['ratio']))
        hexa = str(base64.b64decode(x['payload_raw']).hex())
        nomb = (len(hexa) - 14)//4
        index_test = 0
        for i in range(nomb):
            index = int( hexa[2+(i*4): 4+(i*4)],16 )
            value = int(hexa[4+(i*4):6+(i*4)],16)
            index = round(index * 16 *2.137)
            if index <= conf[1] + conf[2] and  index >= conf[1] - conf[2] and value > conf[8] and value < 250 :
                index_test = 1
                print("index : {} value : {}".format(index,value))
            else :
                print("error index: {} {}".format(index,value))
    
        if index_test == 0 : ok = "NOK"

        print(x['dev_id'] + ' {}'.format(ok))
        gtw=""
        gateways = x["metadata"]["gateways"]
        for gw in gateways:
            gtw= ',' + gw['time'] + ',' + str(gw['rf_chain']) + ',' + str(gw['snr']) + ',' + str(gw['channel']) + ',' + str(gw['rssi'])+ ',' + str(gw['longitude']) + ',' + gw['gtw_id'] + ',' + gw['location_source'] + ',' + str(gw['latitude']) + ',' + str(gw['timestamp'])
                    








#        print(str( x['metadata']['gateways']['rf_chain']))       
        message = x['dev_id'] + ' {}'.format(ok) + ','+ str(base64.b64decode(x['payload_raw']).hex()) + ',' + str(x["hardware_serial"])+','+str(x["port"])+ ',' + x['metadata']['data_rate'] +','+ x['metadata']['time']+gtw+','+ x['metadata']['coding_rate']+','+ str(x['metadata']['frequency'])+','+ str(x['metadata']['airtime'])+','+ x['app_id']+','+"{}".format(x['is_retry'])+','+ str(x['counter'])+','+str( x['payload_fields'])+','+x['dev_id']

 
        files = open('{}.txt'.format(pt),'a')
        files.write("{}\n".format(message))
        files.close()
