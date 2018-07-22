# PyforBoat
Code for getting GPS location, latitude - longitude, accelerometer and receiving and transmitting messages along the ocean via satellite.
The code also sotres everything into a small binary list which takes little data to transmit, this means that there is less cost to transmit each message across the ocean. The RockBlock has a credit system in which it charges each message transmitted.

This code will only work with specific hardware for the raspberry pi
I will list the component sources below
RockBlock(used for transmitting and receiving data via satellite)
CMP(used to find accelerometer, gyroscope and bearings)
RTC(Used to keep the correct data and time whilst the power is off)
GPS adafruit breakout board(Used to find exact gps location and latitude and longitude)

Please credit me for this code

