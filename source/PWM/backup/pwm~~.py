#!/usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
import os,sys
import time


#period in ms
if len(sys.argv)>1:
	period=int(sys.argv[1])-2
else:
	period=18
pid=open('/home/ubuntu/python/pwm/interface/pid','w')
pid.write(str(os.getpid()))
pid.close()
run=open('/home/ubuntu/python/pwm/interface/run','w')
run.write('0')
run.close()
pwm_P9_14 = open('/home/ubuntu/python/pwm/interface/pwm_P9_14', 'w')
pwm_P9_16 = open('/home/ubuntu/python/pwm/interface/pwm_P9_16', 'w')
pwm_P8_13 = open('/home/ubuntu/python/pwm/interface/pwm_P8_13', 'w')
pwm_P8_19 = open('/home/ubuntu/python/pwm/interface/pwm_P8_19', 'w')
pwm_P9_14.write('0')
pwm_P9_16.write('0')
pwm_P8_13.write('0')
pwm_P8_19.write('0')
pwm_P9_14.close()
pwm_P9_16.close()
pwm_P8_13.close()
pwm_P8_19.close()
run=open('/home/ubuntu/python/pwm/interface/run', 'r')
pwm_P9_14 = open('/home/ubuntu/python/pwm/interface/pwm_P9_14', 'r')
pwm_P9_16 = open('/home/ubuntu/python/pwm/interface/pwm_P9_16', 'r')
pwm_P8_13 = open('/home/ubuntu/python/pwm/interface/pwm_P8_13', 'r')
pwm_P8_19 = open('/home/ubuntu/python/pwm/interface/pwm_P8_19', 'r')
GPIO.setup("P8_19",GPIO.OUT)
GPIO.setup("P8_13",GPIO.OUT)
GPIO.setup("P9_16",GPIO.OUT)
GPIO.setup("P9_14",GPIO.OUT)
GPIO.output("P8_19",GPIO.LOW)
GPIO.output("P8_13",GPIO.LOW)
GPIO.output("P9_16",GPIO.LOW)
GPIO.output("P9_14",GPIO.LOW)

while 1:
	run.seek(0)
	if int(run.read()):
		counter=0
		time.sleep(.001) #1ms base
		GPIO.output("P8_19",GPIO.HIGH)
		GPIO.output("P8_13",GPIO.HIGH)
		GPIO.output("P9_16",GPIO.HIGH)
		GPIO.output("P9_14",GPIO.HIGH)
		pwm_P9_14.seek(0)
		pwm_P9_16.seek(0)
		pwm_P8_13.seek(0)
		pwm_P8_19.seek(0)
		
		P9_14 = int(pwm_P9_14.read())
		P9_16 = int(pwm_P9_16.read())
		P8_13 = int(pwm_P8_13.read())
		P8_19 = int(pwm_P8_19.read())
		
		for x in range(0,1000):
			time.sleep(.000001)
			counter+=1
			if P8_19<counter:
				GPIO.output("P8_19",GPIO.LOW)
			if P8_13<counter:
				GPIO.output("P8_13",GPIO.LOW)
			if P9_16<counter:
				GPIO.output("P9_16",GPIO.LOW)
			if P9_14<counter:
				GPIO.output("P9_14",GPIO.LOW)
		time.sleep(period/1000)
	else:
		time.sleep((period+2)/1000)
	






	
	