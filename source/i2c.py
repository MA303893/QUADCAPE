#! /usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_I2C import Adafruit_I2C
import math

#HMC5883L 3 axis digital compass www.adafruit.com/datasheets/HMC5883L_3-Axis_Digital_Compass_IC.pdf
#ITG3205 mems gyro dl.btc.pl/kamami_wa/itg3205.pdf
#BMA180 acceleration irtfweb.ifa.hawaii.edu/~tcs3/...BMA180/BMA180-DataSheet-v2.5.pdf
#BMP085 pressure sensor https://www.sparkfun.com/datasheets/Components/General/BST-BMP085-DS000-05.pdf



BMA180= Adafruit_I2C(0x40)
BMP085= Adafruit_I2C(0x77)



#P8_27	imu9	P_XCLR
#P8_29	imu10	P_EOC


def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if( (val&(1<<(bits-1))) != 0 ):
        val = val - (1<<bits)
    return val
	
class compass:
	CONFIG_A = 0x00
	CONFIG_B = 0x01
	MODE_REG = 0x02
	DATAXMSB = 0x03
	DATAXLSB = 0x04
	DATAZMSB = 0x05
	DATAZLSB = 0x06
	DATAYMSB = 0x07
	DATAYLSB = 0x08
	STAT_REG = 0x09
	ID_REG_A = 0x0A
	ID_REG_B = 0x0B
	ID_REG_C = 0x0C
	TEMP_H=0x31
	TEMP_L=0x32
	DRDY ="P8_21"
	HMC5883L = Adafruit_I2C(0x1e)
	GAIN=1090
	GAIN_array=[1370,1090,820,660,440,390,330,230]
	GAUS_array=[.88,1.3,1.9,2.5,4.0,4.7,5.6,8.1]
	
	def set_samples_averaged(self,samples):#accepts 1,2,4,8
		if(samples==1 or samples==2 or samples==4 or samples==8 ):
			sa=int(math.log(samples,2))<<5
			ca=self.HMC5883L.readU8(self.CONFIG_A)&0x5f
			self.HMC5883L.write8(self.CONFIG_A,ca+sa)
			return 0
		return -1
	def set_output_rate_mode(self,rate):
		#0= 0.75HZ,1=1.5HZ,2=3HZ,3=7.5HZ,4=15HZdefault,5=30HZ,6=75HZ,7=reserved
		if(rate>=0 and rate<7):
			sa=rate<<2
			ca=self.HMC5883L.readU8(self.CONFIG_A)&0xe3
			self.HMC5883L.write8(self.CONFIG_A,ca+sa)
			return 0
		return -1 
	def set_measurement_mode(self,mode):
		#0=normal,1=positive bias,2=negative bias,3=reserved
		if(mode>=0 and mode<3):
			sa=mode
			ca=self.HMC5883L.readU8(self.CONFIG_A)&0xFC
			self.HMC5883L.write8(self.CONFIG_A,ca+sa)
			return 0
		return -1
	def set_gain_range(self,gaus):
		for x in range(0,8):
			if gaus<self.GAUS_array[x]:
				break
		self.GAIN=self.GAIN_array[x]
		self.HMC5883L.write8(self.CONFIG_B,x<<5)
		return 0
	def enable_i2c_highspeed(self):
		mr=self.HMC5883L.readU8(self.MODE_REG)&0x7f
		self.HMC5883L.write8(self.MODE_REG,mr+128)
		return 0
	def disable_i2c_highspeed(self):
		mr=self.HMC5883L.readU8(self.MODE_REG)&0x7f
		self.HMC5883L.write8(self.MODE_REG,mr)
		return 0
	def set_operating_mode(self,str):#"CONT","SING","IDLE"
		str=str.upper()[:4]
		if str=="CONT" :
			mr=self.HMC5883L.readU8(self.MODE_REG)&0xfc
			self.HMC5883L.write8(self.MODE_REG,mr)
			return 0
		elif str=="SING":
			mr=self.HMC5883L.readU8(self.MODE_REG)&0xfc
			self.HMC5883L.write8(self.MODE_REG,mr+1)
			return 0
		elif str=="IDLE":
			mr=self.HMC5883L.readU8(self.MODE_REG)&0xfc
			self.HMC5883L.write8(self.MODE_REG,mr+2)
			return 0
		else:
			return -1
	def __init__ (self,sample,rate,gain_range,highspeed,bias,mode):
		self.set_samples_averaged(sample)
		self.set_output_rate_mode(rate)
		self.set_gain_range(gain_range)
		if highspeed==1 :
			self.enable_i2c_highspeed()
		self.set_operating_mode(mode)
		self.set_measurement_mode(bias)
		GPIO.setup("P8_21", GPIO.IN)
		
	def get_operating_mode(self):
		mr=self.HMC5883L.readU8(self.MODE_REG)&0x03
		if mr==0 :
			return "CONT"
		if mr==1 :
			return "SING"
		return "IDLE"
	def get_x(self):
		return self.HMC5883L.readU8(self.DATAXMSB)*2**8+self.HMC5883L.readU8(self.DATAXLSB)
	def get_y(self):
		return self.HMC5883L.readU8(self.DATAYMSB)*2**8+self.HMC5883L.readU8(self.DATAYLSB)
	def get_z(self):
		return self.HMC5883L.readU8(self.DATAZMSB)*2**8+self.HMC5883L.readU8(self.DATAZLSB)
	def get_ID(self):
		return self.HMC5883L.readU8(self.ID_REG_C)*2**16+self.HMC5883L.readU8(self.ID_REG_B)* 2**8+self.HMC5883L.readU8(self.ID_REG_A)
	def data_locked(self):
		return self.HMC5883L.readU8(self.STAT_REG)&0x02>>1
	def RDY(self):
		return self.HMC5883L.readU8(self.STAT_REG)&0x01
	def DRDY(self):
		return GPIO.input("P8_21")
	def get(self):
		self.HMC5883L.write8(self.DATAXMSB,self.DATAXMSB)
		while 1:
			if 0==self.RDY():
				break
		x,xl,z,zl,y,yl=self.HMC5883L.readList( self.DATAXMSB, 6)
		t,tl=self.HMC5883L.readList( self.TEMP_H, 2)
		return twos_comp(x*2**8+xl,16),twos_comp(y*2**8+yl,16),twos_comp(z*2**8+zl,16)
		
		
def init():
			#sample,rate,gain_range,highspeed,bias,mode
	Compass=compass(8,4,5,0,1,"cont")
	
"""	
Compass.get_x(),Compass.get_y(),Compass.get_z()
Compass.data_locked()
Compass.get_operating_mode()

c1= compass(1,,4,,)
c2=compass(2,,8,)

c1.GAIN

"""


	
	
	
class gyro:
	ITG3205= Adafruit_I2C(0x68)
	WHO_AM_I=0x00
	SMPLRT_DIV=0x15
	DLPF_FS=0x16
	INT_CFG=0x17
	INT_STATUS=0x1A
	TEMP_OUT_H =0x1B 
	TEMP_OUT_L=0x1C 
	GYRO_XOUT_H=0x1D 
	GYRO_XOUT_L=0x1E 
	GYRO_YOUT_H=0x1F 
	GYRO_YOUT_L=0x20 
	GYRO_ZOUT_H =0x21
	GYRO_ZOUT_L =0x22 
	PWM_MGM=0x3E
	G_INT="P8_25"
	DLPF_CFG_IN=1000
	def __init__ (self):
		GPIO.setup(self.G_INT,GPIO.IN)
		return
	def verify(self):
		return  0x68==self.ITG3205.readU8(self.WHO_AM_I)
	def sample_rate_divider(self,frequency):
		SMPLRT_DIV_VAL=int(self.DLPF_CFG_IN/frequency-1)
		if SMPLRT_DIV_VAL>=0 and SMPLRT_DIV_VAL<=255:
			self.ITG3205.write8(self.SMPLRT_DIV,SMPLRT_DIV_VAL)
			return 0 
		return -1 
	def set_full_scale(self):
		dlpf=self.ITG3205.readU8(self.DLPF_FS)&0xe7
		self.ITG3205.write8(self.DLPF_FS,3<<3)
		return 0 
	def set_dlpf(self,mode):
		if mode>7 or mode<0:
			return -1
		dlpf=self.ITG3205.readU8(self.DLPF_FS)&0xf8
		if mode==0:
			DLPF_CFG_IN=8000
			self.ITG3205.write8(self.DLPF_FS,dlpf)
		else:
			DLPF_CFG_IN=1000
			self.ITG3205.write8(self.DLPF_FS,dlpf + mode)
		return 0 
	def int_actl(self,mode):#mode=1 for active low
		if mode==1 or mode==0:
			intcfg=self.ITG3205.readU8(self.INT_CFG)&0x7f
			self.ITG3205.write8(self.INT_CFG,mode<<7+intcfg)
			return 0 
		return -1 
	def int_open(self,mode):#mode=1 for open drain
		if mode==1 or mode==0:
			intcfg=self.ITG3205.readU8(self.INT_CFG)&0xbf
			self.ITG3205.write8(self.INT_CFG,mode<<6+intcfg)
			return 0 
		return -1
	def int_latch(self,mode):#mode=1 for latch until cleared
		if mode==1 or mode==0:
			intcfg=self.ITG3205.readU8(self.INT_CFG)&0xdf
			self.ITG3205.write8(self.INT_CFG,mode<<5+intcfg)
			return 0 
		return -1
	def int_anyrd(self,mode):#mode=1 any read clears, mode=0 only status reg read clears
		if mode==1 or mode==0:
			intcfg=self.ITG3205.readU8(self.INT_CFG)&0xef
			self.ITG3205.write8(self.INT_CFG,mode<<4+intcfg)
			return 0 
		return -1
	def int_rdy_en(self,mode):#mode=1 rdy_en int enabled
		if mode==1 or mode==0:
			intcfg=self.ITG3205.readU8(self.INT_CFG)&0xfb
			self.ITG3205.write8(self.INT_CFG,mode<<2+intcfg)
			return 0 
		return -1
	def int_raw_en(self,mode):#mode=1 raw_rdy_en int enabled
		if mode==1 or mode==0:
			intcfg=self.ITG3205.readU8(self.INT_CFG)&0xfe
			self.ITG3205.write8(self.INT_CFG,mode+intcfg)
			return 0 
		return -1
	def int_itgrdy_rawrdy(self):
		intstat=self.ITG3205.readU8(self.INT_STATUS)
		return  intstat&3 != 0, intstat&1 != 0
	def get(self):
		t,tl,x,xl,y,yl,z,zl=self.ITG3205.readList(self.TEMP_OUT_H,8)
		x,y,z,t=twos_comp(x*2**8+xl,16),twos_comp(y*2**8+yl,16),twos_comp(z*2**8+zl,16),twos_comp(t*2**8+tl,16)
		x,y,z,t=x/14.375,y/14.375,z/14.375,9*(35+(t+13200.0)/280.0)/5+32
		
		return  x,y,z,t
	def reset(self):
		pwmgt=self.ITG3205.readU8(self.PWM_MGM)&0x7f
		self.ITG3205.write8(self.PWM_MGM,pwmgt+128)
		return 0 
	def sleep(self):
		pwmgt=self.ITG3205.readU8(self.PWM_MGM)&0xbf
		self.ITG3205.write8(self.PWM_MGM,pwmgt+64)
		return 0 
	def awake(self):
		pwmgt=self.ITG3205.readU8(self.PWM_MGM)&0xbf
		self.ITG3205.write8(self.PWM_MGM,pwmgt)
		return 0 
	def stby_x(self,sleep):
		if sleep ==0 or sleep ==1:
			pwmgt=self.ITG3205.readU8(self.PWM_MGM)&0xdf
			self.ITG3205.write8(self.PWM_MGM,pwmgt+sleep<<5)
			return 0 
		return -1 
	def stby_y(self,sleep):
		if sleep ==0 or sleep ==1:
			pwmgt=self.ITG3205.readU8(self.PWM_MGM)&0xef
			self.ITG3205.write8(self.PWM_MGM,pwmgt+sleep<<4)
			return 0 
		return -1 
	def stby_z(self,sleep):
		if sleep ==0 or sleep ==1:
			pwmgt=self.ITG3205.readU8(self.PWM_MGM)&0xf7
			self.ITG3205.write8(self.PWM_MGM,pwmgt+sleep<<3)
			return 0 
		return -1 
	def set_clk_mode(self,mode):
		if mode<0 or mode>5:
			return -1 
		pwmgt=self.ITG3205.readU8(self.PWM_MGM)&0xf8
		self.ITG3205.write8(self.PWM_MGM,pwmgt+mode)
		return 0 
	def int_pin(self):
		return GPIO.input(self.G_INT)
	
	
	
class accel:
	BMA180= Adafruit_I2C(0x40)
	LSB_PER_G=.125#multiply by G range and then use as LSB per mg. will be updated automatically
	LSB_TEMP=.5#1 lsb=.5 degrees c
	
	class __REG__enum:
		chip_id=0x00
		version=0x01
		acc_x_lsb=0x02
		acc_x_msb=0x03
		acc_y_lsb=0x04
		acc_y_msb=0x05
		acc_z_lsb=0x06
		acc_z_msb=0x07
		temp=0x08
		status_reg1=0x9
		status_reg2=0xA
		status_reg3=0xb
		status_reg4=0xc
		ctrl_reg0=0xd 
		ctrl_reg1=0xe 
		ctrl_reg2=0xf  
		reset=0x10
		bw_tcs=0x20
		ctrl_reg3=0x21
		ctrl_reg4=0x22
		hy =0x23
		slope_tapsens_info=0x24 
		high_low_info =0x25
		low_dur=0x26
		high_dir=0x27
		tapsens_th=0x28
		low_th=0x29
		high_th=0x2a
		slope_th=0x2b
		cd1=0x2c
		cd2=0x2d
		tco_x=0x2e
		tco_y=0x2f
		tco_z=0x30
		gain_t=0x31
		gain_x=0x32
		gain_y=0x33
		gain_z=0x34
		offset_lsb1=0x35
		offset_lsb2=0x36
		offset_t=0x37
		offset_x=0x38
		offset_y=0x39
		offset_z=0x3a
		#0x3b-0x3f resv
		ee_bw_tcs=0x40
		ee_ctrl_reg3=0x41 
		ee_ctrl_reg4=0x42 
		ee_hy=0x43 
		ee_slope_tapsens_info=0x44 
		ee_high_low_info=0x45 
		ee_low_dur=0x46 
		ee_high_dur=0x47
		ee_tapsens_th=0x48
		ee_low_th=0x49 
		ee_high_th=0x4a
		ee_slope_th=0x4b
		ee_cd1=0x4c
		ee_cd2=0x4d
		ee_tco_x=0x4e
		ee_tco_y=0x4f
		ee_tco_z=0x50
		ee_gain_t=0x51 
		ee_gain_x=0x52
		ee_gain_y=0x53
		ee_gain_z=0x54
		ee_offset_lsb1=0x55
		ee_offset_lsb2=0x56 
		ee_offset_t=0x57
		ee_offset_x=0x58
		ee_offset_y=0x59
		ee_offset_z=0x5a
		ee_crc=0x5b
		#0x56-0x8f resv 
	reg=__REG__enum()
	NEWx=0 
	NEWy=0 
	NEWz=0 
	G_array=[1,1.5,2,3,4,8,16]
	G_adc_resolution=[.13,.19,.25,.38,.5,.99,1.98]
	gpio_int="P8_23"
	def chip_id(self):
		return self.BMA180.readU8(self.reg.chip_id)
	def version(self):
		return self.BMA180.readU8(self.reg.version)>>4, self.BMA180.readU8(self.reg.version)&0x0f
	def get(self):#not done
		#xl,x,yl,y,zl,z = self.BMA180.readList(self.reg.acc_x_lsb,6)
		#x,y,z=twos_comp(x*2**6+xl>>2,14)*.00025,twos_comp(y*2**6+yl>>2,14)*.00025,twos_comp(z*2**6+zl>>2,14)*.00025
		#tco_x,tco_y,tco_z,gain_t,gain_x,gain_y,gain_z,olsb1,olsb2,ot,ox,oy,oz = self.BMA180.readList(self.reg.tco_x,13)
		#x,y,z=x+(((olsb1>>4)+(ox*2**4))*.00025)-2,y+(((olsb2&0x0f)+(oy*2**4))*.00025)-2,z+(((olsb2>>4)+(oz*2**4))*.00025)-2
		xl,x,yl,y,zl,z = self.BMA180.readList(self.reg.acc_x_lsb,6)
		x,y,z=twos_comp(x*2**6+xl/4,14)*.00025+.025,twos_comp(y*2**6+yl/4,14)*.00025,twos_comp(z*2**6+zl/4,14)*.00025+.05
		return x,y,z
	def temp(self):#not done
		return 9./5.*self.LSB_TEMP*(twos_comp(self.BMA180.readU8(self.reg.temp),8))+32
	def __init__(self):
		self.chip_id=self.chip_id()
		self.version=self.version()
		GPIO.setup(self.gpio_int,GPIO.IN)
	def set_gain_range(self,g_range):
		for x in range(0,7):
			if math.fabs(g_range)<=self.G_array[x]:
				break
		rg=self.BMA180.readU8(self.reg.offset_lsb1)&0xf1
		self.LSB_PER_G=self.G_adc_resolution[x]
		self.BMA180.write8(self.reg.offset_lsb1<<1)
		return 0
	def get_gain_range(Self):
		return (self.BMA180.readU8(self.reg.offset_lsb1)&0x0e)>>1
	bw_array=[10,20,40,75,150,300,600,1200,"high","band"]
	def set_bw_mode(self,bandwidth):
		if bandwidth =='band':
			bw=9
		elif bandwidth =='high':
			bw=8
		else:
			for x in range(0,8):
				if bandwidth<=bw_array[x]:
					break
		rg=self.BMA180.readU8(self.reg.bw_tcs)&0xf
		self.BMA180.write8(self.reg.bw_tcs,rg+x<<4)
		return
	def get_bw_mode(self):
		return bw_array[self.BMA180.readU8(self.reg.bw_tcs)>>4]
	def set_power_mode(self,mode):
		if mode=="low_noise":
			mode=0
		elif mode=="ultra_low_noise":
			mode=1
		elif mode=="reduced_power":
			mode=2
		elif mode=="low_power":
			mode=3
		elif mode>3 or mode<0:
			return -1
		rg=self.BMA180.readU8(self.reg.tco_z)&0xfC
		self.BMA180.write8(self.reg.tco_z,rg+mode)
		return 0
	def get_power_mode(self):#returns (mode,description)
		array=["low_noise","ultra_low_noise","reduced_power","low_power"]
		rg=self.BMA180.readU8(self.reg.tco_z)&0x03
		return rg,array[rg]
	def set_readout_12bit(self):
		rg=self.BMA180.readU8(self.reg.offset_t)&0xfe 
		self.BMA180.write8(self.reg.offset_t,rg+1)
		return
	def set_readout_14bit(self):
		rg=self.BMA180.readU8(self.reg.offset_t)&0xfe 
		self.BMA180.write8(self.reg.offset_t,rg)
		return
	def get_Readout_mode(self):
		return 12+(self.BMA180.readU8(self.reg.offset_t)&1)*2
	def set_sample_skipping(Self):
		return
	def clr_sample_skipping(self):
		return 0
	def get_sample_skipping_mode(self):
		return 0
	def shadow_disable(self):
		rg=self.BMA180.readU8(self.reg.gain_y)&0xfe 
		self.BMA180.write8(self.reg.gain_y,rg+1)
		return 0 
	def shadow_enable(self):
		rg=self.BMA180.readU8(self.reg.gain_y)&0xfe 
		self.BMA180.write8(self.reg.gain_y,rg)
		return 0
	def internal_regulator_disable(Self,device_voltage):
		device_voltage=3.3
		if device_voltage>=2.00:
			print "ERROR: internal regulator cannot be disabled if supply if greater than 2v\n"
			return -1
		return 0 
	def wake_up(self):
		return
	def dis_wake_up(self):
		return
	def set_wake_up_dur(Self,durration):
		return
	def get_wake_up_dur(self):
		return
	def set_slope_alert(self):
		return 
	def clr_slope_alert(Self):
		return
	def dis_i2c(Self):
		return 
	def en_i2c(self):
		return 
	def gpio_interrupt(self):
		return GPIO.input(self.gpio_int)
	def get_interrupts(self):#	
		return 
	
	
	
	

	
	
	
	
#example
class a:
	def a(self):
		return 2
	def __init__(self):
		self.a=self.a()
#A=a() to make a member
#A.a returns 2 
	
	
	
	
	
	
	
	
	
	