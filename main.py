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
import threading
import component_tests



class MoExample(rockBlockProtocol):
  def __init__(self):
      self.rb = rockBlock.rockBlock("/dev/ttyUSB1", self)
  def main(self):

    # rb = rockBlock.rockBlock("/dev/ttyUSB1", self)
    
    #print("Hello World")
    self.rb.sendMessage("Hello World RockBLOCK!")

    self.rb.close()

  def rockBlockTxStarted(self):
    pass#print "rockBlockTxStarted"

  def rockBlockTxFailed(self):
    pass#print "rockBlockTxFailed"

  def rockBlockTxSuccess(self,momsn):
    #global passed, variable array <- you cant use globals in classes
    print("rockBlockTxSuccess ") + str(momsn)

def smbus_setup():
    while True:
        time.sleep(0.1)
        bus = smbus.SMBus(1)
        if bus == smbus.SMBus(1): #if error is thrown bus wont be assigned to the correct port.
            break                 #in which case a manual fix is necessary
        else:
            break #pass

class Timer: # This is a timer class which simplifies having to do anything at certain intervals
    def __init__(self, toexecute, delay): #This can easiliy be reused
        self.function = toexecute
        self.wait = delay
        self.thread1 = threading.Thread(target=(self.loop)) # allows creation of multiple threads running simultaneously
        self.running = True
    def loop(self):
        while self.running:
            time.sleep(self.wait)
            self.function()
    def start(self):
        self.thread1.start()
    def stop(self):
        self.runnning = False


run_gps = True

GPIO.setmode(GPIO.BCM)

fileName = "Coloured abbey fields - (52.349527, -1.587642), (52.347117, -1.583197) text"

file1 = open("/home/pi/Desktop/"+fileName+".txt","r")


f = file1.read() #opens and reads the file containing the map into an array
array = []
for x in f.split("\n")[:-1]:
  yArr = []
  for y in x.split(",")[:-1]:
    yArr.append(y)
  array.append(yArr)

#pinList is a list of 7 GPIO pin numbers to be used
#movementBearing is the direction it should move in
def updateMotors(pinList, compassBearing, movementBearing,upSideDown):
  
  #The motors being turned on are opposite the direction of motion
  motorBearing = movementBearing + 180

  #Finds the angle between the compass sensor and the motor(s) to
  #be turned on, and ensures it's between 0 and 360
  motorAngle = (motorBearing - compassBearing) % 360
  
  if upSideDown:
    motorAngle = 360 - motorAngle

  #Converts this into a binary string that can be represented by 
  #the 6 GPIO pins in pinList
  binaryAngle = bin(int(round((motorAngle*63)/360)))[2:]
  while len(binaryAngle) < 6:
    binaryAngle = '0' + binaryAngle
  #Controls each pin individually
  for i in range(1,7):
    pin = pinList[i]

    #Converts character to integer
    pinValue = int(binaryAngle[i-1])
    #print pinValue

    if pinValue:
      GPIO.output(pin,1)
    else:
      GPIO.output(pin,0)
  #movement bearings of over 360 tell the pi to stay still
  if movementBearing > 360:
    for i in range(7):
      GPIO.output(pinList[6-i],0)
  else:
    GPIO.output(pinList[0],1)
    
#Lattitude and longitude found from GPS sensor
class map:
    def __init__(self, array):
        self.array = array #class allows you to add more functions later on if necessary easier
    def mapReader(self, lattitude, longitude, array):
        # Tuples containing the lattitude and longitude of the array elements at the corners
        topLeft = (52.349527, -1.587642)
        bottomRight = (52.347117, -1.583197)

        lattCorrect = (lattitude > bottomRight[0]) and (lattitude < topLeft[0])
        longCorrect = (longitude > topLeft[1]) and (longitude < bottomRight[1])

        if lattCorrect and longCorrect:
            # Gets dimensions of array
            xSize = len(self.array)
            ySize = len(self.array[1])

            # Gets length and width of 'map' in terms of latt and long
            longSize = abs(bottomRight[1] - topLeft[1])
            latSize = abs(topLeft[0] - bottomRight[0])

            # Gets the pixel by interpolating the coordinates
            currentPixelX = round(((longitude - topLeft[1]) / longSize) * xSize)
            currentPixelY = round(((topLeft[0] - lattitude) / latSize) * ySize)

            return self.array[currentPixelX][currentPixelY]
        else:
            return 0


#def mapReader(lattitude,longitude,array):


def read_cmp():
    start = time.time()
    #while 1:
    time.sleep(0.1)
    bus = SMBus(1)
    bearing = float(bus.read_byte_data(0x60, 0x01)) * 360/255
    acc_z = bus.read_byte_data(0x60, 0x10)
        #if bearing == float(bus.read_byte_data(0x60, 0x01)) and acc_z == bus.read_byte_data(0x60, 0x10):
        #    break #breaks out the loop since the bearing and acceleration is correct
        #else:
        #    trace = traceback.format_exc() # allows to forward the error message back to via email ?
        #    #rb.sendMessage(trace) # todo I cant remember the code for this..#
#
  #          time.sleep(5)
 #           continue  #this causes the function to run again
                      #if you want the file to start again, something else needs to done


    cal_state = bus.read_byte_data(0x060, 0x1E)
    bus.close()
    # bearing_l = bus.read_byte_data(0x60, 0x03)
    # bearing_h = bus.read_byte_data(0x60, 0x02)
    end = time.time() - start
    return bearing, acc_z, cal_state

def read_gps():
    start = time.time()
    time.sleep(0.1)
    while True:
        try:
            session = gps.gps("localhost", "2947")
            session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
            break
        except:
            pass
    hasLat = hasLong = 0
    while ((hasLat==0) or (hasLong==0)):
        report = session.next()
        if report['class'] == 'TPV':
          if hasattr(report, 'lon'):
            hasLat = 1
            lon_int = report.lon
        if report['class'] == 'TPV':
          if hasattr(report, 'lat'):
            hasLong = 1
            lat_int = report.lat
    #GPIO.output[] # todo This is for the LED lightining, so when hasLat and hasLong is fetched the LED outputs whatever
    end = time.time() - start # how it took to get the values, this can be returned and transmitted.
    return lat_int, lon_int

#if __name__ == '__main__':.

class Timer: # This is a timer class which simplifies having to do anything at certain intervals
    def __init__(self, toexecute, delay): #This can easiliy be reused
        self.function = toexecute
        self.wait = delay
        self.thread = threading.Thread(self.loop) # allows creation of multiple threads running simultaneously
        self.running = True
    def loop(self):
        while self.running:
            time.sleep(self.wait)
            self.function()
    def start(self):
        self.thread.start()
    def stop(self):
        self.runnning = False

pinList = [17,27,22,10,9,11,5]
for pin in pinList:
  GPIO.setup(pin,GPIO.OUT)

movementBearing = 0
trans_data = ""

def check_lopsided():
    cmp_timer = Timer(check_lopsided, delay=2)

    cmp_timer.start()

    while True:
        compassBearing, acc_z = read_cmp()
        if acc_z >= 128:
            upsideDown = 0
        else:
            upsideDown = 1
        updateMotors(pinlist, compassBearing, movementBearing, upsideDown)
        return upsideDown

    cmp_timer.stop()


def run_gps():
    gps_timer = Timer(read_gps, delay=60)

    gps_timer.start()
    while True:
        latt, longi = read_gps()

        movementBearing = map.mapReader(latt, longi, array)

    gps_timer.stop()


def location_repo():
    location_timer = Timer(read_gps, delay=1800)
    location_timer.start()

    while True:
        long_repo *= 1000
        long_repo = round(long_repo, 0)

        latitude_repo *= 1000
        latitude_repo = round(latitude_repo, 0)

        # This is converting into 15 bit binary number and adding it the the list
        trans_data.append('{0:015b}'.format(long_repo))
        trans_data.append('{0:015b}'.format(latitude_repo))

    location_timer.stop()

def message_sent():

    message_timer = Timer()

    GPIO.output(pinList[0], 0)
    RB = MoExample()
    if RB.passed == 1:
        time_tomessage = time.time() + 21600
        trans_data = ""
    else:
        time_tomessage = time.time() + 600
    GPIO.output(pinList[0], 1)
    return time_tomessage


location_timer =

if location_timer.running() and message_timer.running() and gps_timer.running()

    # read_gps()
    # read_cmp()
    #
    location_timer = Timer(location_repo(), delay=1800)
    message_timer = Timer(message_sent(), delay = message_sent())
    #
    #
    gps_timer.start()
    location_timer.start()
    message_timer.start()
    #
    gps_timer.stop()
    location_timer.stop()
    message_timer.stop()



    #whatever else you want to go on forever

