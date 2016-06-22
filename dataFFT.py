import numpy as np
import matplotlib.pyplot as plt
import csv
from numpy.fft import fft, fftshift


#Make array with mpuData.txt as column line which has same type of data.
with open("mpuData.txt",'r') as data:
	print "\nData Sequence: %s" % (data.readline())
	column = zip(*[line for line in csv.reader(data, dialect="excel-tab")])
	np_time = np.array(column[0], dtype='float')
	np_Ax = np.array(column[1], dtype='float')
	np_Ay = np.array(column[2], dtype='float')
	np_Az = np.array(column[3], dtype='float')
	np_T = np.array(column[4], dtype='float')
	np_Gx = np.array(column[5], dtype='float')
	np_Gy = np.array(column[6], dtype='float')
	np_Gz = np.array(column[7], dtype='float')

#Drawing graphs with raw data of accelero meter & Gyroscope
graphTitle = ['Accelero X', 'Accelero Y', 'Accelero Z', 'Gyro X', 'Gyro Y', 'Gyro Z']
npData = np.array([np_Ax, np_Ay, np_Az, np_Gx, np_Gy, np_Gz])

plt.figure(1,figsize=(12,8))
for i in range(0,6):
	plt.subplot(2,3,i+1)
	plt.title(graphTitle[i])
	plt.plot(np_time, npData[i], '.-')
	plt.xlabel('sec')
	plt.ylabel('raw value')



#****** [FFT] ******#
#try:
npFFT = []
plt.figure(2, figsize=(12,8))
for i in range(0,6):
	#1. Just do FFT & shifting zero-point to the middle of graph
	npFFT.append(fftshift(fft(npData[i])))	#Results are complex numbers

	#2. Get (or define) sampling frequency
	ts = round(np_time[1]-np_time[0],1)	#sampling period
	fs = 1./ts				#sampling frequency

	#3. Calculating 'Frequency Step' to draw graph in f-plane
	#Frequency Step = (sampling frequency)/(number of sampling)
	N = np_time.size
	FreqStep = fs/N
	FreqDomain = FreqStep*np.arange(-N/2, N/2)

	#4. plot graph in f-plane
	plt.subplot(2,3,i+1)
	plt.title(graphTitle[i]+" FFT")
	plt.plot(FreqDomain, abs(npFFT[i]), '.-r')
	plt.xlabel('Freq')
	plt.ylabel('Magnitude')

plt.show()

#except:
#	print "err"

