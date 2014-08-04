#!/usr/bin/python

import os
import subprocess

def init():
	#apply overlays
	os.system("echo hcsr04 > /sys/devices/bone_capemgr.9/slots")
	
def getDistance():
	#make sure executable is in same directory as this file
	distance = float(subprocess.check_output("./hcsr04", shell=True))
	return distance

