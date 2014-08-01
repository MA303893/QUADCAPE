#include "quadcape_i2c.h"


//////////////////////////////////////////////////////////////////////
int HMC5883L_C::write(HMC5883L_enum reg, char data){
	unsigned char buf[2];
	buf[0]= reg;
	buf[1]=data;
	
if (write(bus,buf,2) != 2) {
    /* ERROR HANDLING: i2c transaction failed */
    printf("Failed to write to the i2c bus.\n");
    buffer = g_strerror(errno);
    printf(buffer);
    printf("\n\n");
	return -1;
}
return 0;

}

int HMC5883L_C::read(char * buffer, HMC5883L_enum reg, int amount_to_read){
	unsigned char buf[1];
	buf[0]= reg;
	
if (write(bus,buf,1) != 1) {
    /* ERROR HANDLING: i2c transaction failed */
    printf("Failed to write to the i2c bus.\n");
    buffer = g_strerror(errno);
    printf(buffer);
    printf("\n\n");
	return -1;
}



    // Using I2C Read
    if (read(bus,buffer,amount_to_read) != amount_to_read) {
        /* ERROR HANDLING: i2c transaction failed */
        printf("Failed to read from the i2c bus.\n");
        buffer = g_strerror(errno);
        printf(buffer);
        printf("\n\n");
		return -1;
    } else {
        return 0;
    }
}

int HMC5883L_C::init(int * Bus){
	address=HMC5883L_addr;
	bus=Bus;
	if (ioctl(bus, I2C_SLAVE, (address<<1)||1) < 0) {
		printf("Failed to acquire bus access and/or talk to slave.\n");
		/* ERROR HANDLING; you can check errno to see what went wrong */
		return -1;
	}
	return 0;
}




//////////////////////////////////////////////////////////////////////
int I2C_bus_init(int * bus,char * device){

	if ((bus = open(device, O_RDWR)) < 0) {
		/* ERROR HANDLING: you can check errno to see what went wrong */
		perror("Failed to open the i2c bus");
	return -1;
	}
	return 0;
}
		
/////////////////////////////////////////////////////////////////


int main(){		
		
	//initialize bus	
	int * bus;
	if(I2C_bus_init(bus,"/dev/i2c-2")!=0){
		exit(1);
	}
		
	//initialize the device
	if(HMC5883L.init(bus)!=0){
		exit(1);
	}
	
	//read from device
	char buf[10];
	HMC5883L.read(buf,CONFIG_REG_A,1);
	HMC5883L.write(CONFIG_REG_A,01110010b);
	HMC5883L.read(buf,CONFIG_REG_A,1);
	
	
return 0;
}


