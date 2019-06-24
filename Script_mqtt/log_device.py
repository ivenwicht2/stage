
def log_device(device,pt):
    files = open('{}.txt'.format(pt),'a')
    files.write("{}\n".format(device))
    files.close()
