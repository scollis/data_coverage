#first we do some imports and check the version of Py-ART for consistency
import pyart
from matplotlib import pyplot as plt
from matplotlib import rc
import matplotlib.dates as mdates
import netCDF4
from netCDF4 import num2date
import numpy as np
import copy
import scipy
import os
from IPython.parallel import Client
import pickle
from time import time
print pyart.__version__
radar_in_dirs = [ '/data-in/radar/sgp/sgpcsaprsur/sur/', 
                 '/data-in/radar/sgp/sgpcsaprrhi/rhi/', 
                 '/data-in/radar/sgp/sgpcsaprvert/']
names = ['CSAPR Volume', 'CSAPR RHI', 'CSAPR VPT']
print "Done step 1"
files = []
for i in range(len(names)):
    these_files = os.listdir(radar_in_dirs[i])
    these_files.sort()
    fq_files = []
    for fl in these_files:
        subdir_contents = os.listdir(radar_in_dirs[i]+ fl)
        for final_file in subdir_contents:
            fq_files.append(radar_in_dirs[i]+ fl + '/' + final_file)
    files.append(fq_files)

print files[0][0]

def get_date(filename):
    try:
        radar = pyart.io.read(filename)
        t = (num2date(radar.time['data'][0], radar.time['units']), num2date(radar.time['data'][-1], radar.time['units']))
    except:
        #return start time and end time being the same
        t = (num2date(0, 'seconds since 2000-01-01T00:00:00Z'), num2date(0, 'seconds since 2000-01-01T00:00:00Z'))
    return t
    
        
t1 = time()
print get_date(files[0][0])
print time() - t1



results = []
for i in range(len(files)):
    print "Doing ", names[i] 
    t1 = time()
    c = Client()
    dview = c[:]
    dview.block = False
    dview.execute('import pyart')
    dview.execute('from netCDF4 import num2date')
    result = dview.map_async(get_date,files[i])
    datestrs = result.get()
    print (time()-t1)
    block_list = []
    for pair in datestrs:
        date_start = mdates.date2num(pair[0])
        scan_length = mdates.date2num(pair[1]) - date_start
        block_list.append((date_start, scan_length ))
    results.append(block_list)

data_dict = {}
for i in range(len(names)):
    data_dict.update({names[i]: results[i]})


print len(results)
outfile = '/home/sc8/csapr.pickle'
fh = open(outfile, 'w')
pickle.dump(data_dict, fh)
fh.close()


