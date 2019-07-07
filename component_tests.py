import gps
import rockBlock
from rockBlock import rockBlockProtocol
import smbus
from smbus import SMBus
import time
import datetime
import RPi.GPIO as GPIO
import traceback
import _thread
import main.py
import threading
from main.py import Timer
from main import read_cmp
from main import read_gps


cmp_ok = True


def gps_test():
    current = []
    gps_timer = Timer(read_gps(), delay=5) #Here I used the Timer class yet again in order to create a thread which runs all
    gps_timer.start() # of this every 5 seconds.
    lat, long = read_gps()
    current.append(lat, long) # The long and lat 5 seconds before
    time.sleep(5)
    if (lat - current[0]) > 10 or (long - current[1]) > 10: # Another plausability test in order to test is its accurate or not
        gps_ok = False
        trace_back =[lat, long] #allows us to examine the values to see whats going on
    elif current[0] == 0 or current[1] == 0:
        gps_ok = False
    else:
        gps_ok = True

    gps_timer.stop()

    return gps_ok, trace_back



def cmp_test():
    trace_back = 0.0
    bearing, a, b = read_cmp() #again a and b are unneeded in this so I just named it something random
    cmp_timer = Timer(read_cmp(), delay=5)
    cmp_timer.start()
    current = bearing # the bearing 5 seconds before
    time.sleep(5)
    end = bearing
    turn = current - end # plausability test for the bearing change to check whether or not its accurate
    if turn > 180: # you might need to change this value by making it smaller
        cmp_ok = False #depending on whats possible or not
        trace_back = turn #allows to trace value seing whats wrong
    else:
        cmp_ok = True


    a, b, cal_state = read_cmp()# I named long and lat a and b because its not needed for this, only cal_state is
    if cal_state != 3:
        calibration = False
    else:
        calibration = True

    cmp_timer.stop()
    return calibration, cmp_ok, trace_back

start_time = time.time()

while True:
    cmp_test()
    gps_test()
    cal, cmp_ok, trace_cmp = cmp_test()
    gps_ok, trace_gps =  gps_test()
    output = ("Calibration status : {}, Compass OK : {} Turn values : {}".format(cal, cmp_ok, trace_cmp))
    output2 = ("GPS OK : {} Moved values : {}".format(gps_ok, trace_gps))
    message_timer = Timer(rb.message(output, output2), delay =5)



