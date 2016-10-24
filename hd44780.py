#!/usr/bin/python

# simple functions for controlling a LCD 16x2 Display on the GPIO Pins of the Raspberry Pi
# Falkensteiner Software 2016
# http://www.falkensteiner-software.at
#
# feel free to take this sourcecode and reuse/modify it in your project, but please reference 'Falkensteiner Software' as source 
# the origin of this script is: 'http://tutorials-raspberrypi.de/raspberry-pi-lcd-display-16x2-hd44780/'
# I reused it by myself and mofified it to meet my own requirements


import time
import RPi.GPIO as GPIO

LCD_RS = 19
LCD_E  = 13
LCD_DATA4 = 26
LCD_DATA5 = 16
LCD_DATA6 = 20
LCD_DATA7 = 21

LCD_WIDTH = 16 		# characters per line
LCD_LINE_1 = 0x80 	# Address of 1. Display line 
LCD_LINE_2 = 0xC0 	# Address of 2. Display line
LCD_CHR = GPIO.HIGH
LCD_CMD = GPIO.LOW
E_PULSE = 0.0005
E_DELAY = 0.0005

def lcd_send_byte(bits, mode):
	GPIO.output(LCD_RS, mode)
	GPIO.output(LCD_DATA4, GPIO.LOW)
	GPIO.output(LCD_DATA5, GPIO.LOW)
	GPIO.output(LCD_DATA6, GPIO.LOW)
	GPIO.output(LCD_DATA7, GPIO.LOW)
	if bits & 0x10 == 0x10:
	  GPIO.output(LCD_DATA4, GPIO.HIGH)
	if bits & 0x20 == 0x20:
	  GPIO.output(LCD_DATA5, GPIO.HIGH)
	if bits & 0x40 == 0x40:
	  GPIO.output(LCD_DATA6, GPIO.HIGH)
	if bits & 0x80 == 0x80:
	  GPIO.output(LCD_DATA7, GPIO.HIGH)
	time.sleep(E_DELAY)    
	GPIO.output(LCD_E, GPIO.HIGH)  
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, GPIO.LOW)  
	time.sleep(E_DELAY)      
	GPIO.output(LCD_DATA4, GPIO.LOW)
	GPIO.output(LCD_DATA5, GPIO.LOW)
	GPIO.output(LCD_DATA6, GPIO.LOW)
	GPIO.output(LCD_DATA7, GPIO.LOW)
	if bits&0x01==0x01:
	  GPIO.output(LCD_DATA4, GPIO.HIGH)
	if bits&0x02==0x02:
	  GPIO.output(LCD_DATA5, GPIO.HIGH)
	if bits&0x04==0x04:
	  GPIO.output(LCD_DATA6, GPIO.HIGH)
	if bits&0x08==0x08:
	  GPIO.output(LCD_DATA7, GPIO.HIGH)
	time.sleep(E_DELAY)    
	GPIO.output(LCD_E, GPIO.HIGH)  
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, GPIO.LOW)  
	time.sleep(E_DELAY)  

def config():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(LCD_E, GPIO.OUT)
	GPIO.setup(LCD_RS, GPIO.OUT)
	GPIO.setup(LCD_DATA4, GPIO.OUT)
	GPIO.setup(LCD_DATA5, GPIO.OUT)
	GPIO.setup(LCD_DATA6, GPIO.OUT)
	GPIO.setup(LCD_DATA7, GPIO.OUT)

def init():
	lcd_send_byte(0x33, LCD_CMD)
	lcd_send_byte(0x32, LCD_CMD)
	lcd_send_byte(0x28, LCD_CMD)
	lcd_send_byte(0x0C, LCD_CMD)  
	lcd_send_byte(0x06, LCD_CMD)
	lcd_send_byte(0x01, LCD_CMD)  

def message(message, line=1):
	if line == 1:
		lcd_send_byte(LCD_LINE_1, LCD_CMD)
	else:
		lcd_send_byte(LCD_LINE_2, LCD_CMD)

	message = message.ljust(LCD_WIDTH," ")  
	for i in range(LCD_WIDTH):
	  lcd_send_byte(ord(message[i]),LCD_CHR)

def shift(text, idx, dispLen):
	idx = idx % len(text)
	a = text[idx:dispLen+idx]
	if len(a) < dispLen:
		diff = dispLen - len(a)
		b = text[0:diff]
		a = a+b
    
	return a

if __name__ == '__main__':

	config()

	init()

	message(" Falkensteiner ")
	message("    Software    ", 2)
	
	time.sleep(2)
	
	msg1 = "  Raspberry Pi  "
	msg2 = "Disp./ADC Board"
	for i in range(len(msg1)):
		message(msg1[:i+1])
		message("", 2)
		time.sleep(0.1)	
	for i in range(len(msg2)):
		message(msg1)
		message(msg2[:i+1], 2)
		time.sleep(0.1)
	
	msg1 = "Falkensteiner Software, Kaprunerstr. 29, 5700 Zell am See, Austria       "
	for i in range(0,150):
		m = shift(msg1, i, LCD_WIDTH)
		message(m)
		time.sleep(0.2)



	time.sleep(2)
	
	GPIO.cleanup()
