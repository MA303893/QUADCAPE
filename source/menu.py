
#menu.py
import time
import kbhit
import os
import sys 
import signal 
import subprocess
"""
call menu.example() for an example
USAGE:
	menu.unbuffer_stdin() for normal menu operation, menu.restore_stdin() on 
	exit or to get normal behavior back.
	newMenu=menu.submenu(name,menu_options_list,menu_functions_list,menu_characters_list)
	the menu will display a the options from above and when an item from 
	characters is pressed, the corresponding function will be called. 
	Additionally,	CLEAR_ON_REFRESH,PRINT_ON_REFRESH,	USE_BANNER can be cleared
	for extra flexibility
	Finally, to make sure the menu is not blocking, IDLE_FUNCTION=0 can be set 
	to a function of the user's
	choice and will be repeatedly called until a key is pressed. After every 
	return from the function, the menu will check for keypresses. A keypress 
	will not cause an early abort from the idle function
	
	The menu will ignore keys that are not on the characters_list, but will 
	interrupt on SIGINT. 
	Also, the arrow keys, up, down, right, left, can be captured with A,B,C,D 
	respectively, in addition to the letter keys. It may be advisable to not 
	use those letters if this behavior is not desired. 
	
	Also, note that if the input passed in the menu_options_list is greater 
	than 48 characters, it will be truncated. 
	
	If you try to check for '*' then this will match any character that is not 
	in any other menu_characters_list element. 
"""
	
################################################################################
def example():
	unbuffer_stdin()
	menu2=submenu("No banner on this menu, refreshes screen constantly",["line3: press 3","other: press any key"],[test3,0],["3","*"])
	menu2.USE_BANNER=0
	#leave defaults of clear and refresh
	MAIN=submenu("MAIN",["line1: press A","line2: press B","another menu: press c"],[test1,test2,menu2.display ],["A","b","c"])
	MAIN.CLEAR_ON_REFRESH=0
	MAIN.PRINT_ON_REFRESH=0
	#MAIN.USE_BANNER=0
	
	MAIN.display();
	restore_stdin()
	print "Have now exited and stdin restored."
	
def test1():
	print "test1"
def test2():
	print "test2"
def test3():
	print "test3"
	
################################################################################
def signal_handler(signal,frame):
	kbhit.restore_stdin()
	print "Caught SIGINT            "	
	print "Restoring stdin"
	kbhit.restore_stdin()
	exit(0)
	
def restore_stdin():
	kbhit.restore_stdin()
def unbuffer_stdin():
	kbhit.unbuffer_stdin()
def banner():
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
	return
def print_menu(title, lines):
	LINE_LENGTH=48
	
	title_len=len(title)
	spaces=(10+LINE_LENGTH-title_len)/2
	if (len(title) % 2)==0:
		offset=0
	else:
		offset=1
	print "\n"+" " *10 + "*"*60+"\n"+" "*10+"*"+" "*spaces+title+" "*(spaces+offset)+"*\n"+" " *10 + "*"*60+"\n"+" "*10+"*"+" "*58+"*\n",
	for line in lines:
		print " " *10+"*    ",
		if len(line)<LINE_LENGTH:
			print line,
		else:
			print line[0:LINE_LENGTH],
		print " "* (LINE_LENGTH-len(line))+"    *"
	print " "*10+"*"+" "*58+"*\n"+" " *10 + "*"*60+"\n"
	return
	
	
class submenu:
	menu_array=[]
	depth=0
	def __init__(self,title_in,items_in,functions_in,keys_in):
		
		#############################################
		#User callable outside
		self.CLEAR_ON_REFRESH=1
		self.PRINT_ON_REFRESH=1
		self.USE_BANNER=1
		self.IDLE_FUNCTION=0
		self.ONCE_FUNCTION=0
		self.NO_RETURN_AFTER_KEY=0
		#############################################
		self.title=title_in
		self.items=items_in
		self.functions=functions_in
		self.keys=keys_in
		self.RETURN_KEY=0
		for x in range(0,len(self.keys)):
			self.keys[x]=self.keys[x].lower()

	def display(self):
		
		submenu.depth+=1
		index = 1
		while index < len(submenu.menu_array):    
 			if submenu.menu_array[index] == submenu.menu_array[index-1]:
				submenu.menu_array.pop(index)
				index -= 1  
    			index += 1
    		submenu.menu_array.append(self)
		print submenu.menu_array
		noresponse=1
		self.refresh(1)
		if self.ONCE_FUNCTION!=0:
			self.ONCE_FUNCTION()
		
		while noresponse>0:
			if self.IDLE_FUNCTION!=0:
				self.IDLE_FUNCTION()
			if kbhit.kbhit()>0:
					char=kbhit.getch().lower()	
					for x in range(0,len(self.keys)):
						#if we find a key then call the function
						if char==self.keys[x]:
							if self.functions[x]:
								self.functions[x]()
							noresponse=0 +self.NO_RETURN_AFTER_KEY-self.RETURN_KEY
						#if the key is not found but we have a wild card, call teh function
						elif self.keys[x]=='*':
							if self.functions[x]:
								self.functions[x]()
							noresponse=0 +self.NO_RETURN_AFTER_KEY-self.RETURN_KEY				
			#now that keypress has been evaluated, refresh if proper flags are set
			self.refresh()
		if len(submenu.menu_array)>0:
			submenu.menu_array.pop()
		submenu.depth-=1
		self.RETURN_KEY=0
	def ret(self):
		self.RETURN_KEY=1
	def refresh(self,force=0):
		if force==1:
			try:
				subprocess.call(["clear"])
			except OSError:
				subprocess.call(["cls"])
			finally:
				if self.USE_BANNER==1:	
					banner()
				print_menu(self.title,self.items)
			return

		if self.CLEAR_ON_REFRESH==1:
			try:
				subprocess.call(["clear"])
			except OSError:
				subprocess.call(["cls"])
		if self.PRINT_ON_REFRESH==1:
			if self.USE_BANNER==1:	
				banner()
			print_menu(self.title,self.items)

		return
		
		
def back():
	submenu.menu_array.pop(len(submenu.menu_array)-2).display()
def current():
	submenu.menu_array.pop(len(submenu.menu_array)-1).display()
signal.signal(signal.SIGINT, signal_handler)
#example()

	

