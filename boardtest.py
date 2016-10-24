#!/usr/bin/python

# simple testprogram to show the functionallity of the Display/ADC-Board for the Raspberry Pi
# Falkensteiner Software 2016
# http://www.falkensteiner-software.at
#
# feel free to take this sourcecode and reuse/modify it in your project, but please reference 'Falkensteiner Software' as source 

import time
import RPi.GPIO as GPIO

import mcp3008 as ADC
import hd44780 as LCD

Leds = [14,15,18,17,27,22,23,24]
Buttons = [5,6,12]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Leds, GPIO.OUT)
GPIO.setup(Buttons, GPIO.IN)

def LedBlinking(button):
	LCD.message("Led blinking....")
	LCD.message("", 2)

	for i in range(0,10):
		GPIO.output(Leds, GPIO.HIGH)
		time.sleep(0.2)
		GPIO.output(Leds, GPIO.LOW)
		time.sleep(0.2)

def LedRunning(button):
	LCD.message("Led running....")
	LCD.message("", 2)
	for i in range(0,5):
		for led in Leds:
			GPIO.output(led, GPIO.HIGH)
			time.sleep(0.05)
			GPIO.output(led, GPIO.LOW)
			time.sleep(0.05)


def AdcTest(button):
	ADC.Open()
	v = ADC.GetVoltageValue()
	LCD.message("ADC: Channel 0")
	LCD.message(str(v) + "V", 2)



GPIO.add_event_detect(5, GPIO.RISING, callback=LedBlinking, bouncetime=500)
GPIO.add_event_detect(6, GPIO.RISING, callback=LedRunning, bouncetime=500)
GPIO.add_event_detect(12, GPIO.RISING, callback=AdcTest, bouncetime=200)

LCD.config()
LCD.init()

LCD.message(" Falkensteiner")
LCD.message("    Software    ", 2)

raw_input("Press Enter to exit...")

GPIO.cleanup()

