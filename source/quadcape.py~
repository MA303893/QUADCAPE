#!/usr/bin/env python 
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
import os
import sys 
import signal 
import pwm
import menu

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
################################################################################
#					USER VARIABLES
################################################################################
#pid coefficients
pid_P_accel=31
pid_I_accel=35
pid_D_accel=1
pid_P_gyro=2
pid_I_gyro=0
pid_D_gyro= 0

#measurement offsets
gx_os=0 #in degrees/sec
gy_os=0
gz_os=0            
ax_os=0 #in Gs 
ay_os=0
az_os=0

#set_points
gx_sp=0
gy_sp=0
gz_sp=0
ax_sp=0
ay_sp=0
az_sp=1

#throttle
THROTTLE=0

#ratios for motor speed
MOTOR_SPEED_RATIO_throttle=.5
MOTOR_SPEED_RATIO_gyro=0
MOTOR_SPEED_RATIO_accel=6					
MOTOR_SPEED_RATIO_enable_z=0
base_speed=150
MAX_SPEED=800
#####################################################################################

 
#####################MENUS#####################################################
welcome_menu	=0
main_menu=0
tuning_menu=0
test_tuning_menu=0
#quadcape_menu.welcome_menu.display()
#quadcape_menu.main_menu.display()
#quadcape_menu.tuning_menu.display()
def init_menus():	
	global welcome_menu	
	global main_menu
	global tuning_menu
	global test_tuning_menu
	#welcome
	welcome_menu=menu.submenu("The system is ready to use.",["                   Press enter"],[0],['*'])
	welcome_menu.PRINT_ON_REFRESH=0
	welcome_menu.CLEAR_ON_REFRESH=0
	#main menu
	main_menu=menu.submenu("MAIN MENU",["RUN: Press R","CALIBRATION: Press C","SENSOR DIAGNOSTICS: Press S","BATTERY DIAGNOSTICS: Press B","TUNING: Press T","VISION: Press V","HELP: Press H","EXIT: Press E or SPACE" ],[f_run,f_calibrate,f_sensor,f_battery,f_tuning, f_vision,f_help,f_exit,f_exit], ["R","C","S","B","T","V","H","E"," "])
	main_menu.PRINT_ON_REFRESH=0
	main_menu.CLEAR_ON_REFRESH=0
	
	menu_list=["Display all tuning parameters: 0","UPDATE PID:","   Gyro P:     1","   Gyro I:     2","   Gyro D:     3","   ACCEL P:    4","   ACCEL I:    5","   ACCEL D:    6","Max speed:     7","Base speed:    8","RATIOS:","     throttle: a","     enable_z: s","     gyro:     d","     accel:    f","OFFSETS: gx: y    gy: u    gz: i","OFFSETS: ax: o    ay: p    az: [","TEST: T","Main menu: M","Back: B","Exit: E"]
	menu_functions=[tuning_menu_f1,tuning_menu_f2,tuning_menu_f3,tuning_menu_f4,tuning_menu_f5,tuning_menu_f6,lambda: update_pid("Max speed",""),lambda: update_pid("base speed",""),tuning,0,f_exit,0,lambda: update_pid("",""),lambda: update_pid("ratio","throttle"),lambda: update_pid("ratio","enable_z"),lambda: update_pid("ratio","gyro"),lambda: update_pid("ratio","accel"),lambda: update_pid("g","xos"),lambda: update_pid("g","yos"),lambda: update_pid("g","zos"),lambda: update_pid("a","xos"),lambda: update_pid("a","yos"),lambda: update_pid("a","zos")]
	tuning_menu=menu.submenu("TUNING",menu_list,menu_functions,["1","2","3","4","5","6","7","8","t","b","e","m","0","a","s","d","f","y","u","i","o","p","["])
	tuning_menu.IDLE_FUNCTION=idle_tuning
	tuning_menu.USE_BANNER=0
	#tuning test
	test_tuning_menu=menu.submenu("Test Tuning with current PID values",["Throttle: +10 press 5","          +1  press t","          -1  press g","          -10 press b","back: press SPACE"],[throttlepp,throttlep,throttlem,throttlemm,test_tuning_back],["5","t","g","b"," "])
	test_tuning_menu.ONCE_FUNCTION=lambda: start_motors(.1,base_speed)
	test_tuning_menu.IDLE_FUNCTION=run
	test_tuning_menu.USE_BANNER=0
	test_tuning_menu.PRINT_ON_REFRESH=0
	test_tuning_menu.CLEAR_ON_REFRESH=0
	test_tuning_menu.NO_RETURN_AFTER_KEY=1

	#run_menu=menu.submenu("RUN",[]
############################################################################
def tuning_menu_f1()  : update_pid("g","p")
def tuning_menu_f2()  : update_pid("g","i")
def tuning_menu_f3()  : update_pid("g","d")
def tuning_menu_f4()  : update_pid("a","p")
def tuning_menu_f5()  : update_pid("a","i")
def tuning_menu_f6()  : update_pid("a","d")
def test_tuning_back():
	start_motors(0,0)
	THROTTLE=0
	test_tuning_menu.ret()
def throttlepp() : 
	global THROTTLE
	THROTTLE+=10
def throttlep () : 
	global THROTTLE
	THROTTLE+=1
def throttlem () :  
	global THROTTLE
	THROTTLE-=1
def throttlemm() :  
	global THROTTLE
	THROTTLE-=10

def tuning():
	test_tuning_menu.display()
	
def f_exit():
	menu.restore_stdin()
	print "User exit.\nRestoring stdin\nThank you for using Quadcape."
	exit()
	return	
def f_calibrate():
	return
def f_run():
	return
def f_sensor():
	return
def f_battery():
	return
def f_tuning(): 
	tuning_menu.display()
	return
def f_vision():
	return
def f_help():
	return
	
	
#end quadcape menus########################


def idle_tuning():
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
	global ax_os  
	global ay_os
	global az_os
	
	data_gx,data_gy,data_gz,t=Gyro.get() #degrees/sec
	data_ax,data_ay,data_az=Accel.get() #in G 
	data_gx,data_gy,data_gz=data_gx+gx_os,data_gy+gy_os,data_gz+gz_os
	data_ax,data_ay,data_az=data_ax+ax_os,data_ay+ay_os,data_az+az_os
	print "Accel:X:{} \n     Y:{} \n     Z:{} \nGyro: X:{} \n     Y:{} \n     Z:{}".format(data_ax,data_ay,data_az,data_gx,data_gy,data_gz)
	time.sleep(.1)
	return #idle_tuning

#run will update the controllers and send the data to the pwms once. 
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
	global pid_P_accel
	global pid_I_accel
	global pid_D_accel
	global pid_P_gyro
	global pid_I_gyro
	global pid_D_gyro
	global pwm
	global LEDs_flag
	global base_speed
	global ax_os  
	global ay_os
	global az_os
	
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
	#MOTOR_SPEED_RATIO_throttle
	#MOTOR_SPEED_RATIO_gyro
	#MOTOR_SPEED_RATIO_accel					
	#MOTOR_SPEED_RATIO_enable_z
	
	pwm_br =base_speed+MOTOR_SPEED_RATIO_throttle*THROTTLE+(-MOTOR_SPEED_RATIO_gyro*gx_up-MOTOR_SPEED_RATIO_gyro*gy_up-MOTOR_SPEED_RATIO_gyro*MOTOR_SPEED_RATIO_enable_z*gz_up)  +(-MOTOR_SPEED_RATIO_accel*ax_up +MOTOR_SPEED_RATIO_accel* ay_up+MOTOR_SPEED_RATIO_accel*MOTOR_SPEED_RATIO_enable_z* az_up)
	pwm_bl =base_speed+MOTOR_SPEED_RATIO_throttle*THROTTLE+(-MOTOR_SPEED_RATIO_gyro*gx_up+MOTOR_SPEED_RATIO_gyro*gy_up+MOTOR_SPEED_RATIO_gyro*MOTOR_SPEED_RATIO_enable_z*gz_up)  +(+MOTOR_SPEED_RATIO_accel*ax_up +MOTOR_SPEED_RATIO_accel* ay_up+MOTOR_SPEED_RATIO_accel*MOTOR_SPEED_RATIO_enable_z* az_up)
	pwm_fl =base_speed+MOTOR_SPEED_RATIO_throttle*THROTTLE+(+MOTOR_SPEED_RATIO_gyro*gx_up+MOTOR_SPEED_RATIO_gyro*gy_up-MOTOR_SPEED_RATIO_gyro*MOTOR_SPEED_RATIO_enable_z*gz_up)  +(+MOTOR_SPEED_RATIO_accel*ax_up -MOTOR_SPEED_RATIO_accel* ay_up+MOTOR_SPEED_RATIO_accel*MOTOR_SPEED_RATIO_enable_z* az_up)
	pwm_fr =base_speed+MOTOR_SPEED_RATIO_throttle*THROTTLE+(+MOTOR_SPEED_RATIO_gyro*gx_up-MOTOR_SPEED_RATIO_gyro*gy_up+MOTOR_SPEED_RATIO_gyro*MOTOR_SPEED_RATIO_enable_z*gz_up)  +(-MOTOR_SPEED_RATIO_accel*ax_up -MOTOR_SPEED_RATIO_accel* ay_up+MOTOR_SPEED_RATIO_accel*MOTOR_SPEED_RATIO_enable_z* az_up)
		
	#errors
	br_err=0
	bl_err = 0
	fl_err =0 
	fr_err = 0 
	
		
	if pwm_br>MAX_SPEED:
		br_err=1
		pwm_br=MAX_SPEED
	if pwm_bl>MAX_SPEED:
		bl_err = 1						
		pwm_bl=MAX_SPEED
	if pwm_fl>MAX_SPEED:
		fl_err =1 
		pwm_fl=MAX_SPEED
	if pwm_fr>MAX_SPEED:
		fr_err = 1 
		pwm_fr=MAX_SPEED
	
	
	
	#update motors` 
	#P8_13 PWM Back Right	PWM1	
	#P8_19 PWM Front RIght	PWM2
	#P9_14 PWM Back Left	PWM3
	#P9_16 PWM Front Left	PWM4
	pwm.changeSpeed1(pwm_br)
	pwm.changeSpeed2(pwm_fr)
	pwm.changeSpeed3(pwm_bl)
	pwm.changeSpeed4(pwm_fl)
	if LEDs_flag==0:
		led.back("0000")
		LEDs_flag=1 
	else:
		led.back("1111")
		LEDs_flag=0	
	return
###########################end run
	
				
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






def update_pid(device,param):
	global pid_P_accel
	global pid_I_accel
	global pid_D_accel
	global pid_P_gyro
	global pid_I_gyro
	global pid_D_gyro
	global MAX_SPEED
	global base_speed
	global MOTOR_SPEED_RATIO_throttle
	global MOTOR_SPEED_RATIO_gyro
	global MOTOR_SPEED_RATIO_accel					
	global MOTOR_SPEED_RATIO_enable_z
	
	global gx_os 
	global gy_os
	global gz_os            
	global ax_os  
	global ay_os
	global az_os


	menu.restore_stdin()
	nonnumber=1
	os.system("clear")
	print "*"*80
	print "Modifying PID control:"
	print "*"*80
	print "Accel: P ={} \n       I ={} \n       D ={}\nGYR0:  P ={} \n       I ={} \n       D ={} ".format(pid_P_accel,pid_I_accel,pid_D_accel,pid_P_gyro,pid_I_gyro,pid_D_gyro)
	print "*"*80
	print "MAX_SPEED= {}                base_speed= {}".format(MAX_SPEED, base_speed)
	print "*"*80
	print "pid output - motor speed ratios:\n     throttle: {}\n     gyro: {}\n     Accel: {}\n     enable_z: {}".format( MOTOR_SPEED_RATIO_throttle,MOTOR_SPEED_RATIO_gyro, MOTOR_SPEED_RATIO_accel,MOTOR_SPEED_RATIO_enable_z)
	print "\n"+"*"*80
	print "OFFSETS"
	print "\n"+"*"*80
	print "     GX:{}\n     GY:{}\n     GZ:{}\n     AX:{}\n     AY:{}\n     AZ:{}".format(gx_os,gy_os,gz_os,ax_os,ay_os, az_os)
	print "\n"+"*"*80
	
	
	
	if device=="" and param=="":
		print "Press enter"
		userinput = sys.stdin.readline().rstrip()
		menu.unbuffer_stdin()
	else:
		print "Modifying:"+str(device.upper())+str(param.upper())
		print "*"*80
		while nonnumber:
			print "Enter new value: ",
			userinput = sys.stdin.readline().rstrip()
			try:
				userinput=float(userinput)
				nonnumber=0
			except ValueError:
				print "Error:"+userinput+" is not a number"
		# now we have a new float for the pid			
		menu.unbuffer_stdin()
		print userinput
		if device=='a':
			if param=='i':
				 pid_I_accel=userinput
			if param=='p':
				 pid_P_accel=userinput
			if param=='d':
				 pid_D_accel=userinput
			if param=="xos":
				ax_os=userinput
			if param=="yos":
				ay_os=userinput
			if param=="zos":
				az_os=userinput

		elif device=='g':
			if param=='i':
				 pid_I_gyro=userinput
			if param=='p':
				 pid_P_gyro=userinput
			if param=='d':
				 pid_D_gyro=userinput
			if param=="xos":
				gx_os=userinput
			if param=="yos":
				gy_os=userinput
			if param=="zos":
				gz_os=userinput

		elif device=="max speed":
			MAX_SPEED=userinput
		elif device=="base speed":
			base_speed=userinput
		elif device=="ratio":
			if param=="throttle":
				MOTOR_SPEED_RATIO_throttle=userinput
			if param=="enable_z":
				MOTOR_SPEED_RATIO_enable_z=userinput
			if param=="gyro":
				MOTOR_SPEED_RATIO_gyro=userinput
			if param=="accel":
				MOTOR_SPEED_RATIO_accel=userinput
	#open
	configuration=open("user_config/pid.config","w")
	configuration.write("PIDfile1.0\n")
	configuration.write("pid_P_accel="+str(pid_P_accel)+"\n")
	configuration.write("pid_I_accel="+str(pid_I_accel)+"\n")
	configuration.write("pid_D_accel="+str(pid_D_accel)+"\n")
	configuration.write("pid_P_gyro="+str(pid_P_gyro)+"\n")
	configuration.write("pid_I_gyro="+str(pid_I_gyro)+"\n")
	configuration.write("pid_D_gyro="+str(pid_D_gyro)+"\n")
	configuration.write("MAX_SPEED="+str(MAX_SPEED)+"\n")
	configuration.write("base_speed="+str(base_speed)+"\n")
	configuration.write("MOTOR_SPEED_RATIO_throttle="+str(MOTOR_SPEED_RATIO_throttle)+"\n")
	configuration.write("MOTOR_SPEED_RATIO_gyro="+str(MOTOR_SPEED_RATIO_gyro)+"\n")
	configuration.write("MOTOR_SPEED_RATIO_accel="+str(MOTOR_SPEED_RATIO_accel)+"\n")			
	configuration.write("MOTOR_SPEED_RATIO_enable_z="+str(MOTOR_SPEED_RATIO_enable_z)+"\n")	
	configuration.write("gx_os=" +str(gx_os)+"\n")
	configuration.write("gy_os="+str(gy_os)+"\n")
	configuration.write("gz_os=" +str(gz_os)+"\n")
	configuration.write("ax_os=" +str(ax_os)+"\n")
	configuration.write("ay_os="+str(ay_os)+"\n")
	configuration.write("az_os="+str(az_os)+"\n")
	configuration.close()
	
	
	
	os.system("clear")
	menu.current()
	return
def configuration_read():
	print "Getting user configuration data."
	global pid_P_accel
	global pid_I_accel
	global pid_D_accel
	global pid_P_gyro
	global pid_I_gyro
	global pid_D_gyro
	global MAX_SPEED
	global base_speed
	global MOTOR_SPEED_RATIO_throttle
	global MOTOR_SPEED_RATIO_gyro
	global MOTOR_SPEED_RATIO_accel					
	global MOTOR_SPEED_RATIO_enable_z
	global gx_os 
	global gy_os
	global gz_os            
	global ax_os  
	global ay_os
	global az_os


	#read
	print "Opening user_config/pid.config ..."
	configuration=open("user_config/pid.config","r")
	array=[]
	print "Reading..",
	error=0
	for x in range(0,19):
		print ".",
		array.append(configuration.readline())
		print array[x]
		if array[x]=="":
			print "\nConfiguration file is corrupted. Check user_config/pid.config or use the tuning utility to recreate the file.\nPID values may not be correct"
			error=1
			break
	
	if error==0:
		pid_P_accel=float( array[1][array[1].rstrip().find("=")+1:])
		pid_I_accel=float( array[2][array[2].rstrip().find("=")+1:])
		pid_D_accel=float( array[3][array[3].rstrip().find("=")+1:])
		pid_P_gyro=float( array[4][array[4].rstrip().find("=")+1:])
		pid_I_gyro=float( array[5][array[5].rstrip().find("=")+1:])
		pid_D_gyro=float( array[6][array[6].rstrip().find("=")+1:])
		MAX_SPEED=float( array[7][array[7].rstrip().find("=")+1:])
		base_speed=float( array[8][array[8].rstrip().find("=")+1:])
		MOTOR_SPEED_RATIO_throttle=float( array[9][array[9].rstrip().find("=")+1:])
		MOTOR_SPEED_RATIO_gyro=float( array[10][array[10].rstrip().find("=")+1:])
		MOTOR_SPEED_RATIO_accel=float( array[11][array[11].rstrip().find("=")+1:])		
		MOTOR_SPEED_RATIO_enable_z=float( array[12][array[12].rstrip().find("=")+1:])
		
		gx_os=float( array[13][array[13].rstrip().find("=")+1:])
		gy_os=float( array[14][array[14].rstrip().find("=")+1:])
		gz_os=float( array[15][array[15].rstrip().find("=")+1:])
		ax_os=float( array[16][array[16].rstrip().find("=")+1:])
		ay_os=float( array[17][array[17].rstrip().find("=")+1:])
		az_os=float( array[18][array[18].rstrip().find("=")+1:])
	configuration.close()
	print "Closing config"
	
def start_motors(delay,speed):
	print "Restarting ESCs..."
	pwm.changeSpeed1(0)
	pwm.changeSpeed2(0)
	pwm.changeSpeed3(0)
	pwm.changeSpeed4(0)
	print "All motors off."
	time.sleep(1)
	print "Starting with delay for current balance"
	time.sleep(delay)
	print "INITIALIZING: Motor 1, Back right"
	pwm.changeSpeed1(int)
	time.sleep(delay)
	print "INITIALIZING: Motor 2, Front right"
	pwm.changeSpeed2(speed)
	time.sleep(delay)
	print "INITIALIZING: Motor 3, Front left"
	time.sleep(delay)	
	pwm.changeSpeed4(speed)
	print "INITIALIZING: Motor 4, Back left"
	pwm.changeSpeed3(speed)
	time.sleep(delay)	
	print "All motors initialized"
				

####################################################################
LEDs_flag=0 #global var for running, do not touch	
def signal_handler(signal,frame):
	print "Caught ^C \n"+"Restoring stdin"
	menu.restore_stdin()
	exit(0)
	
	
#devices
print "Done importing"
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
gx.setPoint(gx_sp)
gy.setPoint(gy_sp)
gz.setPoint(gz_sp)
ax.setPoint(ax_sp)
ax.setPoint(ax_sp)
ax.setPoint(ax_sp)

print "Initializing LEDS"
led.init()
led.right("01")
led.left("01")
print "Initializing PWM"
pwm.init()
pwm=pwm.PWM()
time.sleep(1/3)
signal.signal(signal.SIGINT, signal_handler)
configuration_read()
print "Initializing menus"
init_menus()
menu.unbuffer_stdin()
welcome_menu.display()

while 1:
	main_menu.display()
	print "returned here"

