
import pyvisa
from time import sleep
from datetime import datetime

class SpectrumAnalyzer(object):
    def __init__(self,
        resource_name='USB0::0x2A8D::0x0B0B::MY54200340::INSTR',
        ref_level_dbm=20,
        start_freq_mhz=5825,
        stop_freq_mhz=5875,
        rbw_mhz=1,
        auto_calibration=False):

        assert(stop_freq_mhz >= start_freq_mhz)

        rm = pyvisa.ResourceManager()
        self.instr = rm.open_resource(resource_name)

        # factory reset
        self.instr.write(':SYST:PRES:Type Fact')

        # configure freq range
        self.instr.write(f':FREQuency:STAR {start_freq_mhz} MHz')
        self.instr.write(f':FREQuency:STOP {stop_freq_mhz } MHz')

        # configure rbw
        self.instr.write(f':BANDwidth:RESolution {rbw_mhz} MHz')

        self.instr.write(f':DISPlay:WINDow:TRACe:Y:RLEVel {ref_level_dbm}')

        # calibrate
        #self.instr.write(':CAL')

        print('Spectrum Analyzer Init Messages:')
        print('--------------------------------')

        # infinite timeout
        print('  Instrument has infinite timeout...')
        self.instr.timeout = None

        # calibrate now if an alignment is expired
        res = self.instr.query(':CALibration:EXPired?')
        print(f'  calibration expired: {res}')

        # wait until operation is complete
        print('  Waiting Until Operation is Complete')
        self.instr.query('*OPC?')

        self.set_auto_align(auto_calibration)

        print('')


    def set_auto_align(self, auto_align=True):
        self.instr.write(':CAL:AUTO %s'%('ON' if auto_align else 'OFF'))


    def set_max_hold(self):
        self.instr.write(':TRACe1:TYPE MAXHold')

    def clear_write(self):
        self.instr.write(':TRACe1:TYPE WRIT')

    def sleep(self, sec):
        while sec >= 1.0:
            print('waiting for 1 sec')
            sleep(1)
            sec -= 1.0

        if sec > 0:
            print('waiting for %.2f sec'%sec)
            sleep(sec)


    def peak_measurement_dbm(self, delay_time_sec=1):
        #print('taking measurement...')
        sleep(delay_time_sec)
        self.instr.write(':CALCulate:MARKer1:MAXimum')
        return float(self.instr.query(':CALC:MARK1:Y?'))


    def take_peak_measurements_dbm(self, num, delay_time_sec=1):
        return [
            self.peak_measurement_dbm(
                delay_time_sec) for _ in range(num)]

    def set_attenuation_man_db(self, num):
        self.instr.write(':POWer:ATTenation '+str(num))

if __name__ == '__main__':

    s = SpectrumAnalyzer()

    s.set_max_hold()
    # let settle for 5 seconds
    s.sleep(5)
    meas = s.take_peak_measurements_dbm(10, delay_time_sec=.1)
    #print(meas)
    #get current date and time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    #convert date and time to string
    now = str(now)
    #create an unique file name with date and time  
    file_name = "spectrum_" + now + ".csv"
    #write the data to the file
    #
    #
    f=open(file_name,"w")
    f.write("Frequency,Power\n")
    for i in range(len(meas)):
        f.write(str(5825+i)+","+str(meas[i])+"\n")
    f.close()
    print('done')
    #write the data to the file
    
    
   
    

    #f=open("spectrum.csv","w")
    #f.write("Frequency,Power\n")
    #for i in range(len(meas)):
    #    f.write(str(5825+i)+","+str(meas[i])+"\n")
    #f.close()
    #print('done') 
    #s.instr.close()
    #print('instrument closed')
    
    