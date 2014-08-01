#!/usr/bin/python

import Adafruit_BBIO.GPIO as GPIO
import time

"""
Ultrasound Handling
P9_27	Echo
P9_23	Trig

"""

class ultraSound:
	speedofsound = 340
	t1 = 0
	t2 = 0
	distance = 0
	trigRD = 0	

	def __init__(self):
		GPIO.setup("P9_27", GPIO.IN)
		GPIO.setup("P9_23", GPIO.OUT)

	def echoStart(self, pin):
		self.t1 = time.time()
		GPIO.remove_event_detect("P9_27")
		GPIO.add_event_detect("P9_27", GPIO.FALLING, self.echoEnd)
		

	def echoEnd(self, pin):
		self.t2 = time.time()
		trigRD = 0
		self.findDistance()

	def findDistance(self):
		self.distance = (self.t2-self.t1)*self.speedofsound/2

	def trigEN(self):
		GPIO.remove_event_detect("P9_27")
		GPIO.add_event_detect("P9_27", GPIO.RISING, self.echoStart)
		self.trigRD = 1

	def trig(self):
		GPIO.output("P9_23", 1)
		time.sleep(0.0001)
		GPIO.output("P9_23", 0)

			
					

""" Version 2; overestimates a whole lot more
#!/usr/bin/python

import Adafruit_BBIO.GPIO as GPIO
import time

"""
Ultrasound Handling
P9_27	Echo
P9_23	Trig

"""

class ultraSound:
	speedofsound = 340
	t1 = 0
	t2 = 0
	distance = 0	

	def __init__(self):
		GPIO.setup("P9_27", GPIO.IN)
		GPIO.setup("P9_23", GPIO.OUT)
		GPIO.add_event_detect("P9_27", GPIO.BOTH, self.record)

	def record(self, pin):
		t = time.time()
		if GPIO.input("P9_27"):
			self.t1 = t
		else:
			self.t2 = t		

	def findDistance(self):
		self.distance = (self.t2-self.t1)*self.speedofsound/2


	def trig(self):
		GPIO.output("P9_23", 1)
		time.sleep(0.000001)
		GPIO.output("P9_23", 0)


"""			


