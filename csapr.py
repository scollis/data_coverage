#first we do some imports and check the version of Py-ART for consistency
import pyart
from matplotlib import pyplot as plt
from matplotlib import rc
import matplotlib.dates as mdates
import netCDF4
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
