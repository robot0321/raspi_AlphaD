import smbus
import time

#Program Starting time. For calculating data accept time
time0 =  time.time()

#Power manager, especially sleep Register at 0x6B.
#Default is sleep whenever it is awaken up
power_mgmt_1 = 0x6B

#Address of Device(MPU6050)
dev_addr = 0x68

bus = smbus.SMBus(1) # Revision 2

textHeader = ("Ax: ","Ay: ","Az: ", "T: ", "Gx: ", "Gy: ", "Gz: ")
dataBuffer = {0,0,0,0,0,0,0}

#****** Function Definition ******#

#Read raw 8 bits
def read_byte(reg_addr):
	return bus.read_byte_data(dev_addr, reg_addr)

#Read raw 16 bits
def read_word(reg_addr):
	high_byte = bus.read_byte_data(dev_addr, reg_addr)
	low_byte = bus.read_byte_data(dev_addr, reg_addr+1)
	return (high_byte<<8)+low_byte

#Read raw 16bits and transform to 'short-type' which have negative number
#Usually, this is not for configuration-register, but for raw data like gyro, accelero, etc.
def read_word_2c(reg_addr):
	raw_word = read_word(reg_addr)
	if(raw_word>=0x8000):
		return -((65535 - raw_word) + 1)
	else:
		return raw_word


#****** data mining ******#

#Waking Up
bus.write_byte_data(dev_addr, power_mgmt_1, 0)

#Saving data as text file (renew everytime running)
DataStorage = open("mpuData.txt", 'w')
DataStorage.write("Time\tAx\tAy\tAz\tT\tGx\tGy\tGz\n")

#Get period of mining from user (second)
delaytime = float(raw_input("Data Mining delay : "))

#Mining
while(1):
	try:
		#Mining time
		timeBuffer = (time.time() - time0)
		print "sysCLK : %.3f" %(timeBuffer),
		DataStorage.write(str(round(timeBuffer,3))+"\t")

		#Get some Data and write on txt
		for i, reg_addr in zip(range(1,7), range(0x3B, 0x47, 2)):
			print str(textHeader[i])+str(read_word_2c(reg_addr))+"/",
			DataStorage.write(str(read_word_2c(reg_addr))+"\t")

		print ""
		DataStorage.write("\n")
		time.sleep(delaytime)

	except KeyboardInterrupt: #if you put Ctrl-C, close the text file
		print "\n!!!Keyboard Interrupt raised!!!\n"
		DataStorage.close()
		break

