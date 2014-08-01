#!/usr/bin/python

#handle pwm signals 0-1024
"""
P9_14	pwm back left
P9_16	pwm front left
P8_13	pwm back right
P8_19	pwm front right
"""
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
pwm_bl=0
pwm_fl=0
pwm_br=0
pwm_fr=0


def init(period_us,pwm_bl_tr0,pwm_fl_tr0,pwm_br_tr0,pwm_fr):
	
	
	return
	
	
def start_all():
	
	return
	
def get_input():
	return
	
def init_pwm():
PWM.start("P9_14", 40, 4)
PWM.start("P9_16", 40, 4)
PWM.start("P8_13", 40, 4)
PWM.start("P8_19", 40, 4)
	return

