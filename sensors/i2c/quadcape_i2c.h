#ifndef QUADCAPE_I2C_H
#define QUADCAPE_I2C_H

//#include <glib.h>
//#include <glib/gprintf.h>
#include <errno.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

//HMC5883L 3 axis digital compass www.adafruit.com/datasheets/HMC5883L_3-Axis_Digital_Compass_IC.pdf‎
//ITG3205 mems gyro dl.btc.pl/kamami_wa/itg3205.pdf
//BMA180 acceleration irtfweb.ifa.hawaii.edu/~tcs3/...BMA180/BMA180-DataSheet-v2.5.pdf
//BMP085 pressure sensor https://www.sparkfun.com/datasheets/Components/General/BST-BMP085-DS000-05.pdf

//ADDR<<1||RnW
#define 	HMC5883L_addr 	0111100b//read 0x3D write 0x3C
#define 	ITG3205_addr  	1101000b
#define 	BMA180_addr 	1000000b 
#define 	BMP085_addr 	1110111b

enum HMC5883L_enum {
	CONFIG_REG_A=0,
	CONFIG_REG_B,
	MODE_REG,
	DATA_OUT_X_MSB_REG,
	DATA_OUT_X_LSB_REG,
	DATA_OUT_Y_MSB_REG,
	DATA_OUT_Y_LSB_REG,
	DATA_OUT_Z_MSB_REG,
	DATA_OUT_Z_LSB_REG,
	STATUS_REG,
	ID_REG_A,
	ID_REG_B,
	ID_REG_C
};

class HMC5883L_C {
	public:
		int write(HMC5883L_enum reg, char data);
		int read(char * buffer, HMC5883L_enum reg, int amount_to_read);
		int init(int * Bus);
	private:
		char address;
		int * bus;
}HMC5883L;









#endif