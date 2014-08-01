#!/usr/bin/python


"""
This code initializes and controls the duty cycle (in ns) of the PWMs
P8_13 PWM Back Right	PWM1	
P8_19 PWM Front RIght	PWM2
P9_14 PWM Back Left	PWM3
P9_16 PWM Front Left	PWM4
"""

import os
import subprocess



def init():
	#Initializes the PWMs by echoing the overlays
	#uncomment next line if am33xx_pwm is not enabled at boot
	#os.system("echo am33xx_pwm > /sys/devices/bone_capemgr.9/slots")
        os.system("echo sc_pwm_P8_13 > /sys/devices/bone_capemgr.9/slots")
        os.system("echo sc_pwm_P8_19 > /sys/devices/bone_capemgr.9/slots")
        os.system("echo sc_pwm_P9_14 > /sys/devices/bone_capemgr.9/slots")
        os.system("echo sc_pwm_P9_16 > /sys/devices/bone_capemgr.9/slots")

class PWM:
	speed1 = 0
        speed2 = 0
        speed3 = 0
        speed4 = 0
	unit = 1250
	path1 = ''
	path2 = ''
	path3 = ''
	path4 = ''
	startDuty = "750000"

	def __init__(self):		
		#This block finds the paths for the directories for each PWM
		x = os.listdir('/sys/devices')
		for i in x:
			if len(i) == 5:
				if i[0:3] == 'ocp':
					nextDir = i
					break

		x = os.listdir('/sys/devices/' + nextDir)
		for i in x:
			l = len(i)
			if l > 15 and l < 18:
				if i[0:14] == "pwm_test_P8_13":
					self.path1 = nextDir + '/' + i
				elif i[0:14] == "pwm_test_P8_19":
					self.path2 = nextDir + '/' + i
				elif i[0:14] == "pwm_test_P9_14":
					self.path3 = nextDir + '/' + i
				elif i[0:14] == "pwm_test_P9_16":
					self.path4 = nextDir + '/' + i
				else:
					l = 0 #must have else, so dummy

		#Starts the PWMs
                os.system("echo 1 > /sys/devices/" + self.path1 + "/run")
                os.system("echo 1 > /sys/devices/" + self.path2 + "/run")
                os.system("echo 1 > /sys/devices/" + self.path3 + "/run")
                os.system("echo 1 > /sys/devices/" + self.path4 + "/run")

		#Changes the polarity so increasing speed adds and decreasing
		#speed decrements
                os.system("echo 0 > /sys/devices/" + self.path1 + "/polarity")
                os.system("echo 0 > /sys/devices/" + self.path2 + "/polarity")
                os.system("echo 0 > /sys/devices/" + self.path3 + "/polarity")
                os.system("echo 0 > /sys/devices/" + self.path4 + "/polarity")

		#Changes the duty cycle to minimum (750000 ns)
                os.system("echo " + self.startDuty + " > /sys/devices/" + self.path1 + "/duty")
                os.system("echo " + self.startDuty + " > /sys/devices/" + self.path2 + "/duty")
                os.system("echo " + self.startDuty + " > /sys/devices/" + self.path3 + "/duty")
                os.system("echo " + self.startDuty + " > /sys/devices/" + self.path4 + "/duty")


	#speed must be between 0 and 1000

	def changeSpeed1(self, speed):
		if speed >= 0 and speed <= 1000:
			os.system("echo " + str(int(speed*float(self.unit)+float(self.startDuty))) + " > " + "/sys/devices/" + self.path1 + "/duty")
			speed = subprocess.check_output("cat /sys/devices/" + self.path1 + "/duty", shell=True)
			self.speed1 = (float(speed) - float(self.startDuty))/float(self.unit)
			return self.speed1
		else:
			#when writing code, check if a string popped out as the error checker
			return "speed must be between 0 and 1000"

	def changeSpeed2(self, speed):
		if speed >= 0 and speed <= 1000:
			os.system("echo " + str(int(speed*float(self.unit)+float(self.startDuty))) + " > " + "/sys/devices/" + self.path2 + "/duty")
			speed = subprocess.check_output("cat /sys/devices/" + self.path2 + "/duty", shell=True)
			self.speed2 = (float(speed) - float(self.startDuty))/float(self.unit)
			return self.speed2
		else:
			#when writing code, check if a string popped out as the error checker
			return "speed must be between 0 and 1000"

	def changeSpeed3(self, speed):
		if speed >= 0 and speed <= 1000:
			os.system("echo " + str(int(speed*float(self.unit)+float(self.startDuty))) + " > " + "/sys/devices/" + self.path3 + "/duty")
			speed = subprocess.check_output("cat /sys/devices/" + self.path3 + "/duty", shell=True)
			self.speed3 = (float(speed) - float(self.startDuty))/float(self.unit)
			return self.speed3
		else:
			#when writing code, check if a string popped out as the error checker
			return "speed must be between 0 and 1000"

	def changeSpeed4(self, speed):
		if speed >= 0 and speed <= 1000:
			os.system("echo " + str(int(speed*float(self.unit)+float(self.startDuty))) + " > " + "/sys/devices/" + self.path4 + "/duty")
			speed = subprocess.check_output("cat /sys/devices/" + self.path4 + "/duty", shell=True)
			self.speed4 = (float(speed) - float(self.startDuty))/float(self.unit)
			return self.speed4
		else:
			#when writing code, check if a string popped out as the error checker
			return "speed must be between 0 and 1000"

	def stop(self):
                os.system("echo " + self.unit + " > /sys/devices/" + self.path1 + "/duty")
                os.system("echo " + self.unit + " > /sys/devices/" + self.path2 + "/duty")
                os.system("echo " + self.unit + " > /sys/devices/" + self.path3 + "/duty")
                os.system("echo " + self.unit + " > /sys/devices/" + self.path4 + "/duty")


		
		

