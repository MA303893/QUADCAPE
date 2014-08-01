#!/usr/bin/python
"""
LED handling
P8_14	LED DISP5
P8_15	LED DISP3
P8_16	LED DIPS4
P8_17	LED DISP1
P8_18	LED DISP2
P9_22	led bl1
P9_24	LED bl2
P9_26	LED br1
P9_28	LED br2
P9_29	led sl2
P9_31	led sl1
P8_9	led sr2
P8_33	led sr1
"""

import Adafruit_BBIO.GPIO as GPIO


def init():
	GPIO.setup("P8_14", GPIO.OUT);
	GPIO.setup("P8_15", GPIO.OUT);
	GPIO.setup("P8_16", GPIO.OUT);
	GPIO.setup("P8_17", GPIO.OUT);
	GPIO.setup("P8_18", GPIO.OUT);
	GPIO.setup("P8_9", GPIO.OUT);
	GPIO.setup("P8_33", GPIO.OUT);
	GPIO.setup("P9_22", GPIO.OUT);
	GPIO.setup("P9_24", GPIO.OUT);
	GPIO.setup("P9_26", GPIO.OUT);
	GPIO.setup("P9_28", GPIO.OUT);
	GPIO.setup("P9_29", GPIO.OUT);
	GPIO.setup("P9_31", GPIO.OUT);
	return
	
#Led_gauge(12345)
def gauge(str):
	if str[0]== '1':
		GPIO.output("P8_17", GPIO.HIGH) #1
	else:
		GPIO.output("P8_17", GPIO.LOW)
		
	if str[1]== '1':
		GPIO.output("P8_18", GPIO.HIGH) #2
	else:
		GPIO.output("P8_18", GPIO.LOW)
	
	if str[2]== '1':
		GPIO.output("P8_15", GPIO.HIGH) #3
	else:
		GPIO.output("P8_15", GPIO.LOW) 
	
	if str[3]== '1':
		GPIO.output("P8_16", GPIO.HIGH)#4
	else:
		GPIO.output("P8_16", GPIO.LOW)
		
	if str[4]== '1':
		GPIO.output("P8_14", GPIO.HIGH) #5
	else:
		GPIO.output("P8_14", GPIO.LOW) 
		
	return
 
 
"""
P9_22	led bl1
P9_24	LED bl2
P9_26	LED br1
P9_28	LED br2
"""
def back(str):
	if str[0]== '1':
		GPIO.output("P9_22", GPIO.HIGH) #1
	else:
		GPIO.output("P9_22", GPIO.LOW)
		
	if str[1]== '1':
		GPIO.output("P9_24", GPIO.HIGH) #2
	else:
		GPIO.output("P9_24", GPIO.LOW)
	
	if str[2]== '1':
		GPIO.output("P9_26", GPIO.HIGH) #3
	else:
		GPIO.output("P9_26", GPIO.LOW) 
	
	if str[3]== '1':
		GPIO.output("P9_28", GPIO.HIGH)#4
	else:
		GPIO.output("P9_28", GPIO.LOW)
	return
	
def right(str):
	if str[0]== '1':
		GPIO.output("P8_33", GPIO.HIGH) #1
	else:
		GPIO.output("P8_33", GPIO.LOW)
		
	if str[1]== '1':
		GPIO.output("P8_9", GPIO.HIGH) #2
	else:
		GPIO.output("P8_9", GPIO.LOW)
	
	return
	
def left(str):
	if str[0]== '1':
		GPIO.output("P9_31", GPIO.HIGH) #1
	else:
		GPIO.output("P9_31", GPIO.LOW)
		
	if str[1]== '1':
		GPIO.output("P9_29", GPIO.HIGH) #2
	else:
		GPIO.output("P9_29", GPIO.LOW)
	
	return	

	
	
	
def cleanup():
	GPIO.cleanup();
	return

   