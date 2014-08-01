import time

print"Importing i2c.py       "
time.sleep(1/6)
import i2c
print"Importing pid.py       "
time.sleep(1/6)
import pid
print"Importing led.py       "
time.sleep(1/6)
import led
print"Importing telemetry.py "
time.sleep(1/6)
import telemetry
print"Importing kbhit.py     "
time.sleep(1/6)
#import pwm
import kbhit
import os
import sys
import signal 
import pwm
"""
import os, sys, inspect
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])+"/PWM")
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)
	"""

	 
"""	 
import os, sys
lib_path = os.path.abspath('../../../lib')
sys.path.append(lib_path)

import mymodule
	 """

print "Loading user variables"
#pid coefficients
pid_P_accel=2
pid_I_accel=1
pid_D_accel=1
pid_P_gyro=2
pid_I_gyro=1
pid_D_gyro=1

#measurement offsets
gx_os=0 #in degrees/sec
gy_os=0
gz_os=0

ax_os=0 #in Gs 
ay_os=0
az_os=0


#devices
print "Initializing accelerometer"
Accel=i2c.accel()
time.sleep(1/6)
print "Initializing gyroscope"
Gyro=i2c.gyro()
time.sleep(1/6)
print "Initializing pid controllers"
gx=pid.PID(pid_P_gyro,pid_I_gyro,pid_D_gyro)
gy=pid.PID(pid_P_gyro,pid_I_gyro,pid_D_gyro)
gz=pid.PID(pid_P_gyro,pid_I_gyro,pid_D_gyro)
ax=pid.PID(pid_P_gyro,pid_I_gyro,pid_D_gyro)
ay=pid.PID(pid_P_gyro,pid_I_gyro,pid_D_gyro)
az=pid.PID(pid_P_gyro,pid_I_gyro,pid_D_gyro)


#set_points
gx_sp=0
gy_sp=0
gz_sp=0
ax_sp=0
ay_sp=0
az_sp=1

gx.setPoint(gx_sp)
gy.setPoint(gy_sp)
gz.setPoint(gz_sp)
ax.setPoint(ax_sp)
ax.setPoint(ax_sp)
ax.setPoint(ax_sp)


#throttle
THROTTLE=0
#pwm max speeds
PWM_MAX=300
#####################################################################################

def print_header():
	print "*" * 80
	print " " * 35+"Welcome to"
	print "*" * 80
	print " " * 12 +"   ___  _   _   _    ____   ____    _    ____  _____"
	print " " * 12 +"  / _ \| | | | / \  |  _ \ / ___|  / \  |  _ \| ____|"
	print " " * 12 +" | | | | | | |/ _ \ | | | | |     / _ \ | |_) |  _|  "
	print " " * 12 +" | |_| | |_| / ___ \| |_| | |___ / ___ \|  __/| |___ "
	print " " * 12 +"  \__\_\\___/_/   \_\____/ \____/_/   \_\_|   |_____|"
	print "*" * 80
	print " " * 32 + "Raising innovation"
	print "*" * 80
	
	

#update_set_points()
def run():
	global data_gx
	global data_gy
	global data_gz
	global Gyro
	global data_ax
	global data_ay
	global data_az
	global Accel
	global gx_os
	global gy_os
	global data_gz
	global gz_os
	global THROTTLE
		
		
	while 1:
		data_gx,data_gy,data_gz,t=Gyro.get() #degrees/sec
		data_ax,data_ay,data_az=Accel.get() #in G 
		data_gx,data_gy,data_gz=data_gx+gx_os,data_gy+gy_os,data_gz+gz_os
		data_ax,data_ay,data_az=data_ax+ax_os,data_ay+ay_os,data_az+az_os
		#update_set_points()
		
		if kbhit.kbhit()>0:
			char=kbhit.getch().lower()
			if ' ' in char:
				print "SIGNAL: user abort"
				THROTTLE=0
				break 
			if '\n' in char:
				THROTTLE =0
			if 'w' in char:
				THROTTLE +=1
			if 's' in char:
				THROTTLE -=1
			if '2' in char:
				THROTTLE +=10
			if 'x' in char:
				THROTTLE -=10
			print "Throttle: ",
			print THROTTLE
			
		#update pid
def user_menu():
	MENU=1 
	while MENU==1:
		os.system("clear")
		print_header()
		print_main_menu("OPTIONS",["Run","Calibration","Sensor Diagnostics","Tuning","Vision","Help","Exit"])
		noresponse=1
		while noresponse:

			if kbhit.kbhit()>0:
				char=kbhit.getch().lower()				
				if char=='t':
					print "tuning"
					tuning()
				if char =='r':
					print "run"
					run()
				if char=="e":
					MENU=0
					kbhit.restore_stdin()
					break
				#more menu items
				noresponse=0				
	return

def tuning():
	global data_gx
	global data_gy
	global data_gz
	global Gyro
	global data_ax
	global data_ay
	global data_az
	global Accel
	global gx_os
	global gy_os
	global data_gz
	global gz_os
	global THROTTLE
	global pid_P_accel
	global pid_I_accel
	global pid_D_accel
	global pid_P_gyro
	global pid_I_gyro
	global pid_D_gyro
	global pwm
	
	os.system("clear")
	print_header()
	print_main_menu("TUNING",["START: s","GYRO: gp gi gd", "ACCEL: ap ai ad","THROTTLE+: t","THROTTLE-: h","EXIT: e"])
	notstart=1
	while notstart:
		if kbhit.getch()=='s' or kbhit.getch()=='S':
			break
	print "                               Choose an item above"
	
	while 1:
		data_gx,data_gy,data_gz,t=Gyro.get() #degrees/sec
		data_ax,data_ay,data_az=Accel.get() #in G 
		data_gx,data_gy,data_gz=data_gx+gx_os,data_gy+gy_os,data_gz+gz_os
		data_ax,data_ay,data_az=data_ax+ax_os,data_ay+ay_os,data_az+az_os
		#update_set_points()
		MAX_SPEED=0
		if kbhit.kbhit()>0:
			char=kbhit.getch().lower()
			if 'e' in char:
				print "exit"
				THROTTLE=0
				tuning()
				break 
			if ' ' in char:
				print "SIGNAL: user abort"
				THROTTLE=0
				tuning()
				break 				
			if '\n' in char:
				THROTTLE =0
				
			if 't' in char:
				THROTTLE +=1
			if 'h' in char:
				THROTTLE -=1
			if 'g' in char:
				char=kbhit.getch()
				update_pid("g",char)
			if 'a' in char:
				char=kbhit.getch()
				update_pid("a",char)
			if 'p' in char:
				MAX_SPEED+=10
			if ';' in char:
				MAX_SPEED+=1
			if '/' in char:
				MAX_SPEED-=10 
				
			os.system("clear")
			print_main_menu("TUNING",["RUN: r","GYRO: gp gi gd", "ACCEL: ap ai ad","THROTTLE: t","EXIT: e","help: h"])
			print "Accel: P ={} I={} D={}                GYR0:  P ={} I={} D={} ".format(pid_P_accel,pid_I_accel,pid_D_accel,pid_P_gyro,pid_I_gyro,pid_D_gyro)
			print "Throttle: ",
			print THROTTLE
			gx.setPoint(gx_sp)
			gy.setPoint(gy_sp)
			gz.setPoint(gz_sp)
			ax.setPoint(ax_sp)
			ax.setPoint(ax_sp)
			ax.setPoint(ax_sp)
			
			data_gx,data_gy,data_gz,t=Gyro.get() #degrees/sec
			data_ax,data_ay,data_az=Accel.get() #in G 
			print "Accel: {} {} {} Gyro: {} {} {}".format(data_ax,data_ay,data_az,data_gx,data_gy,data_gz)
				
			#quick run
			if 'r' in char:
				tune=1
				os.system("clear")
				print "running..."
				print "Throttle:5++ t+ h- n-- Enter=0  SPACE stop"
				THROTTLE=0
				LEDs=0
				pwm_br =0
				pwm_bl = 0
				pwm_fl =0
				pwm_fr =0
				br_err=0
				bl_err = 0
				fl_err =0 
				fr_err = 0 
				while tune:
					os.system("clear")
					print "running..."
					print "Throttle:5++ t+ h- n-- MAX_SPEED: +10 p, +1 :, -10 / \nEnter=0  SPACE stop"
					print "MAX_SPEED  {}  THROTTLE: {}  br {} fr {} bl {} fl {}".format(MAX_SPEED,THROTTLE,pwm_br,pwm_fr,pwm_bl,pwm_fl)
					if br_err>0:
						print "ERROR, backright max speed error"
					if bl_err>0:
						print "ERROR, backleft max speed error"
					if fr_err>0:
						print "ERROR, frontright max speed error"
					if fl_err>0:
						print "ERROR, frontleft max speed error"
					
					data_gx,data_gy,data_gz,t=Gyro.get() #degrees/sec
					data_ax,data_ay,data_az=Accel.get() #in G 	
					data_gx,data_gy,data_gz=data_gx+gx_os,data_gy+gy_os,data_gz+gz_os
					data_ax,data_ay,data_az=data_ax+ax_os,data_ay+ay_os,data_az+az_os
					
					gx_up=gx.update(data_gx)
					gy_up=gy.update(data_gy)
					gz_up=gz.update(data_gz)
					ax_up=ax.update(data_ax)
					ay_up=ay.update(data_ay)
					az_up=az.update(data_az)
					
					#decide ratios
					pwm_br =.5*THROTTLE+(-.3)*az_up 
					pwm_bl =.5*THROTTLE+(-.3)*az_up 
					pwm_fl =.5*THROTTLE+(-.3)*az_up 
					pwm_fr =.5*THROTTLE+(-.3)*az_up 
						
					#errors
					br_err=0
					bl_err = 0
					fl_err =0 
					fr_err = 0 
					
					if pwm_br>MAX_SPEED:
						br_err=1
					if pwm_br>MAX_SPEED:
						bl_err = 1
					if pwm_br>MAX_SPEED:
						fl_err =1 
					if pwm_br>MAX_SPEED:
						fr_err = 1 
					
					
					
					#update motors` 
					#P8_13 PWM Back Right	PWM1	
					#P8_19 PWM Front RIght	PWM2
					#P9_14 PWM Back Left	PWM3
					#P9_16 PWM Front Left	PWM4
					pwm.changeSpeed1(pwm_br)
					pwm.changeSpeed2(pwm_fr)
					pwm.changeSpeed3(pwm_bl)
					pwm.changeSpeed4(pwm_fl)
					
					if kbhit.kbhit()>0:
						char=kbhit.getch().lower()
						if ' ' in char:
							print "SIGNAL: user abort"
							THROTTLE=0
							tune=0
							pwm.stop()
							break 				
						if '\n' in char:
							THROTTLE =0
							
						if 't' in char:
							THROTTLE +=1
						if 'h' in char:
							THROTTLE -=1
						if '5' in char:
							THROTTLE +=1
						if 'n' in char:
							THROTTLE -=10
						if 'p' in char:
							MAX_SPEED+=10
						if ';' in char:
							MAX_SPEED+=1
						if '/' in char:
							MAX_SPEED-=10 
								
					if LEDs==0:
						led.back("0000")
						LEDs=1 
					else:
						led.back("1111")
						LEDs=0
			
			
	return #tuning
def update_pid(device,param):
	global pid_P_accel
	global pid_I_accel
	global pid_D_accel
	global pid_P_gyro
	global pid_I_gyro
	global pid_D_gyro
	kbhit.restore_stdin()
	nonnumber=1
	print "Accel: P ={} I={} D={}                GYR0:  P ={} I={} D={} ".format(pid_P_accel,pid_I_accel,pid_D_accel,pid_P_gyro,pid_I_gyro,pid_D_gyro)
	print "Modifying:       "+device+param
	while nonnumber:
		print "Enter new value: ",
		userinput = sys.stdin.readline().rstrip()
		try:
			userinpuit=float(userinput)
			nonnumber=0
		except ValueError:
			print "Error:"+userinput+" is not a number"
	# now we have a new float for the pid			
	kbhit.unbuffer_stdin()
	print userinput
	if device=='a':
		if param=='i':
			 pid_I_accel=userinput
		if param=='p':
			 pid_P_accel=userinput
		if param=='d':
			 pid_D_accel=userinput
	if device=='g':
		if param=='i':
			 pid_I_gyro=userinput
		if param=='p':
			 pid_P_gyro=userinput
		if param=='d':
			 pid_D_gyro=userinput
	return
	
	
	
def print_main_menu(title, lines):
	LINE_LENGTH=48
	print "\n"+" " *10 + "*"*60+"\n"+" "*10+"*"+" "*26+title+" "*25+"*\n"+" " *10 + "*"*60+"\n"+" "*10+"*"+" "*58+"*\n",
	for line in lines:
		print " " *10+"*    ",
		if len(line)<LINE_LENGTH:
			print line,
		else:
			print line[0:LINE_LENGTH],
		print " "* (LINE_LENGTH-len(line))+"    *"
	print " "*10+"*"+" "*58+"*\n"+" " *10 + "*"*60+"\n"
	return

	
	
def update_set_points():
	global gx_sp
	global gy_sp
	global gz_sp
	global ax_sp
	global ay_sp
	global az_sp
	global gx
	global gy
	global gz
	global ax
	global ay
	global az
	gx_sp=0
	gy_sp=0
	gz_sp=0
	ax_sp=0
	ay_sp=0
	az_sp=-1
	gx.setPoint(gx_sp)
	gy.setPoint(gx_sp)
	gz.setPoint(gx_sp)
	ax.setPoint(gx_sp)
	ay.setPoint(gx_sp)
	az.setPoint(gx_sp)

def main():
	user_menu()
	return
	


def signal_handler(signal,frame):
	print "Caught ^C \n"+"Restoring stdin"
	kbhit.restore_stdin()
	exit(0)
	
	
####################################################################	
print "Done importing"
print "Initializing LEDS"
led.init()
led.right("01")
led.left("01")
print "Initializing PWM"
pwm.init()
pwm=pwm.PWM()
time.sleep(1/3)
print_header()
signal.signal(signal.SIGINT, signal_handler)
kbhit.unbuffer_stdin()
print "Press Enter"
kbhit.getch()
main()