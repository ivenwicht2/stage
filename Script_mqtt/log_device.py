
def log_device(device,payload,pt):
    files = open('{}'.format(pt),'a')
    files.write("{}, {}\n".format(device,payload))
    files.close()
