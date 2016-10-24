#!/usr/bin/python

# simple functions for controlling a MCP3008 ADC chip on the SPI-Port of the Raspberry Pi
# Falkensteiner Software 2016
# http://www.falkensteiner-software.at
#
# feel free to take this sourcecode and reuse/modify it in your project, but please reference 'Falkensteiner Software' as source 
import spidev
import time

spi = None

# open the SPI channel
def Open():
	global spi
	spi=spidev.SpiDev()
	if spi == None:
		raise Exception("error creating SPI object")

	spi.open(0,0)

# gets the raw binary value from the ADC on the given channel
def GetRawValue(channel=0, differential=False):
	global spi
	if spi == None:
		raise Exception("SPI not opened")

	if channel < 0 or channel > 7:
		raise Exception("Channel must be between 0-7")

	mode = 128
	if differential == True:
		mode = 0

	resp=spi.xfer([1,mode+(channel << 4),0])
	if 0<= resp[1]<=3: 
		w=((resp[1]*256)+resp[2])
	return w

# returns the voltage value instead of the raw binary value from the ADC
# for 10Bit and 3,3V reference voltage we have a resolution of 3,2mV (3,3V / 1023)
# 1023 comes from (2^10 - 1) 
def GetVoltageValue(channel=0, differential=False):
	if channel < 0 or channel > 7:
		raise Exception("Channel must be between 0-7")

	w = GetRawValue(channel, differential)
	return w * 0.0032 

def Close():
	if spi != None:
		spi.close();



if __name__ == '__main__':
	Open()
	while True:
		for i in range(0,8):
			w = GetVoltageValue(i)
			print "Channel: " + str(i) + " - " + str(w)
		
		time.sleep(2)

	Close()
