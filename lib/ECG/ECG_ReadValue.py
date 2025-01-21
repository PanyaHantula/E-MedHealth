import board
import busio
import time
import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Import Filter
import scipy.signal as filter
import math

class ECG_Sensor():
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)      # Initialize the I2C interface
        self.ads = ADS.ADS1115( self.i2c)               # Create an ADS1115 object

    def ADC_ReadValue (self, SamplePoint = 400):
        self.channel0 = AnalogIn(self.ads, ADS.P0)      # Connect ECG to ADC0 on ADS1115 Module
        ECGdata = np.array([])
        cnt = SamplePoint        # Buffer data at 20 point 

        # Capture Time for cal HeartRate     
        start_time = time.time()   
        while (cnt > 0):
            value = self.channel0 .value
            #print('ECG : {0}'.format(value))
            ECGdata = np.append(ECGdata,int(value))
            cnt -= 1
                              
        end_time = time.time()     
        self.elapsed_time = (end_time - start_time) * 1000
        TimePerIndex = self.elapsed_time / len(ECGdata)
        # print("Capture Time {0}".format(self.elapsed_time))
        # print("TimePerIndex {0}".format(TimePerIndex))

        # Cuting data
        ECG_Filter = self.ECG_Filter(ECGdata)
        ECG_peaklist = self.PeakDetect(ECG_Filter)
        ECG_Norm = ECG_Filter / np.max(ECG_Filter)
        bpm = self.CalHeartRate(ECG_peaklist, TimePerIndex)
        if math.isnan(bpm):
            bpm = 0.0
        # print("Average Heart Beat is: %.01f" %(bpm)) #Round off to 1 decimal and print
        # print("No of peaks in sample are {0}".format(len(ECG_peaklist)))

        return ECG_Norm, bpm

    def ECG_Filter(self, RawData):
        # Filter requirements.
        fs = 30.0       # sample rate, Hz
        cutoff = 2      # desired cutoff frequency of the filter, Hz ,      slightly higher than actual 1.2 Hz
        nyq = 0.5 * fs  # Nyquist Frequency
        order = 2       # sin wave can be approx represented as quadratic

        # Filter ECG Data
        normal_cutoff = cutoff / nyq
        b, a = filter.butter(order, normal_cutoff, btype='low', analog=False)
        filterOut = filter.filtfilt(b, a, RawData)

        return filterOut

    def PeakDetect(self, data):
        #Mark regions of interest
        window = []
        peaklist = []
        listpos = 0 #We use a counter to move over the different data columns

        rollingmean = np.mean(data)
        rollingmax = np.amax(data)
        PeakThreshold = rollingmean + (rollingmax-rollingmean)*0.7
        # print('ECG Mean {0}'.format(rollingmean))
        # print('ECG max {0}'.format(rollingmax))
        # print('ECG PeakThreshold {0}'.format(PeakThreshold))

        for datapoint in data:
            if (datapoint < PeakThreshold) and (len(window) < 1): #If no detectable R-complex activity -> do nothing
                listpos += 1

            elif (datapoint > PeakThreshold): #If signal comes above local mean, mark ROI
                window.append(datapoint)
                listpos += 1
                
            else: #If signal drops below local mean -> determine highest point
                beatposition = listpos - len(window) + (window.index(max(window))) #Notate the position of the point on the X-axis
                peaklist.append(beatposition) #Add detected peak to list
                window = [] #Clear marked ROI
                listpos += 1

        #print(peaklist)
        return peaklist
    
    def CalHeartRate(self,peaklist, TimePerIndex):
        RR_list = []
        cnt = 2         # Non cal 2 Index in Peak list
        
        while (cnt < (len(peaklist)-2)):
            RR_interval = (peaklist[cnt+1] - peaklist[cnt]) #Calculate distance between beats in # of samples
            ms_dist = ((RR_interval * TimePerIndex)) #Convert sample distances to ms distances
            RR_list.append(ms_dist) #Append to list
            cnt += 1

        bpm = 60000 / np.mean(RR_list) #60000 ms (1 minute) / average R-R interval of signal
        return bpm
    
def main():

    print("Demo Code for ADS1115 : Get Raw ADC Data")
    print('Reading ADS1x15 channel 0...')
    
    ADS1115_ECG = ECG_Sensor()
    wait = 1
    
    while True:
        ECG_Filter, bpm = ADS1115_ECG.ADC_ReadValue()
        print("Average Heart Beat is:: {:.2f}".format(bpm))
        
        try:
            time.sleep(wait)
        except KeyboardInterrupt:
            print('keyboard interrupt detected, exiting...')

if __name__ == "__main__":
    main()
    
    
    
