import gps
#import rockBlock
#from rockBlock import rockBlockProtocol
#from smbus2 import SMBus
import time
import datetime
#import RPi.GPIO as GPIO
import traceback
import importlib
#import main
import threading
#from main import Timer
#from main import read_cmp
#from main import read_gps
clock = time.time()
from main import read_gps
from main import read_cmp
from main import Timer


def gps_test():
    
    current = []
    #
    # lat, long1 = read_gps()
    # current.append(lat)
    # current.append(long1) # The long and lat 5 seconds before
    # time.sleep(5)
    #
    # if (lat - current[0]) > 10 or (long1 - current[1]) > 10: # Another plausability test in order to test is its accurate or not
    #     gps_ok = False
    #     trace_back =[lat, long1] #allows us to examine the values to see whats going on
    # elif current[0] == 0 or current[1] == 0:
    #     gps_ok = False
    # else:
    #     gps_ok = True

    # output2 = ("GPS OK : {} Moved values : {}, {}".format(gps_ok, lat, long1))

    print "gps_test"
    #print output2
    print("GPS_TEST")

    none = ""

def cmp_test():
    trace_back = 0.0
    try_ = 0
    # while try_ > 6:
    #     try:
    #         bearing, a, b = read_cmp() #again a and b are unneeded in this so I just named it something random
    #         pass
    #     except:
    #         try_ += 1
    #         bearing, a, b = read_cmp()
    #         time.sleep(1)
    #         trace = traceback.format_exc()

        # current = bearing # the bearing 5 seconds before
        # end = bearing
        # turn = current - end # plausability test for the bearing change to check whether or not its accurate
        # if turn > 180: # you might need to change this value by making it smaller
        #     cmp_ok = False #depending on whats possible or not
        #     trace_back = turn #allows to trace value seing whats wrong
        # else:
        #     cmp_ok = True
        #
        # a, b, cal_state = read_cmp()# I named long and lat a and b because its not needed for this, only cal_state is
        # if cal_state != 3:
        #     calibration = False
        # else:
        #     calibration = True
        #
        # output = ("Calibration status : {}, Compass OK : {} Turn values : {}".format(calibration, cmp_ok, trace_back))
        # print bearing
    print "cmp_test"

gps_timer = Timer(cmp_test, delay=5)
cmp_timer = Timer(gps_test, delay=5)

gps_timer.start()
cmp_timer.start()


gps_timer.stop()
cmp_timer.stop()

while cmp_timer.running and gps_timer.running:
    pass



