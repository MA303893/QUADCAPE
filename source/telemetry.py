#!/usr/bin/python
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
ina_br=0
ina_fr=0
ina_fl=0
ina_bl=0
	
def init():
	GPIO.setup("P9_41",GPIO.OUT)
	ADC.setup()
	GPIO.output("P9_41",GPIO.LOW);
	return
	
	
def batt():
	#enable is P9_41
	#adc input is P9_36
	GPIO.output("P9_41",GPIO.HIGH);
	
	#there is a bug currently that the first read is not the latest value
	value = ADC.read("P9_36")
	value=0;
	for x in range(0,5):
		value += ADC.read("P9_36")
	GPIO.output("P9_41",GPIO.LOW);
	value/=5
	#values are returned in 0-1.0 range, multiplying by 1.8 gives the actual result
	value*=1.8
	#1.12k and 8.22k resistor divider 
	return value*8.339
	
def aquire_current():
	#P9_37	ina br
	#P9_38	ina fr
	#P9_39	ina fl
	#P9_40	ina bl
	ina_br=0
	ina_fr=0
	ina_fl=0
	ina_bl=0
	ADC.read("P9_37")
	ADC.read("P9_38")
	ADC.read("P9_39")
	ADC.read("P9_40")
	for x in range(0,5):
		ina_br+=ADC.read("P9_37")
		ina_fr+=ADC.read("P9_38")
		ina_fl+=ADC.read("P9_39")
		ina_bl+=ADC.read("P9_40")
	#we have a 1mOhm shunt with ina213's giving a gain of 50
	#so temp=ina_xx/50 gives us the voltage drop across the shunt and temp*1000 gives the current
	#therefore, ina_xx*20 is the current measurement in amps. 
	#also, the adc returns 1.8 volts scaled between 0-1.0 so we must multiply by 1.8 and divide by 5
	#since we sampled 5 times. 20*1.8/5=7.2 
	ina_br*=7.2
	ina_fr*=7.2
	ina_fl*=7.2 
	ina_bl*=7.2
	return