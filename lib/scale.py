import serial
import numpy as np
import time
from matplotlib import pyplot as plt
from .config import TOTAL_BLOCKS, BLOCK_VARIANCE, SERIAL_PORT
import threading
import os

class ScaleThread(object):
    def __init__(self):
        #establish serial connection
        self.ser = serial.Serial()
        self.ser.port = SERIAL_PORT[0]

        self.ser.baudrate = 115200
        self.ser.open()
        self.alive = True

        #to receive direct serial data
        self.buffer = ''
  
    def start(self):
        while self.alive:
            data = self.ser.read(self.ser.inWaiting())
            if data:
                self.buffer +=  data.decode('utf-8')

    def stop(self):
        self.alive = False
        self.ser.close()

class Scale(ScaleThread):
    def __init__(self):
        super(Scale,self).__init__()
        #initiate variables
        self.total_blocks = TOTAL_BLOCKS #51
        self.block_variance = BLOCK_VARIANCE # % change from the mean
        self.current_status = "on"
        self.std_trigger = .0004

        #start serial parser thread
        self.t1 = threading.Thread(None,self.start)
        self.t1.start()

        self.tare()
         
        self.tower_wt = self.initial_tower_weight()
        self.avg_block_wt = self.tower_wt / self.total_blocks

        #since the blocks vary in weight/density, a min and max is approximated
        self.max_block_wt = (self.avg_block_wt * (1 + self.block_variance))
        self.min_block_wt = (self.avg_block_wt * (1 - self.block_variance))

        #set scale status variables
        self.on_max = self.tower_wt + self.avg_block_wt/10
        self.on_min = self.tower_wt - self.avg_block_wt/10

        self.off_max = self.tower_wt - self.min_block_wt
        self.off_min = self.tower_wt - self.max_block_wt
 
        self.pause = self.tower_wt + self.min_block_wt
        self.two_off = self.tower_wt - self.min_block_wt * 2
        self.collapse = self.tower_wt - self.min_block_wt * 6

        print ('setup complete')

    def tare(self):
        #tare scale
        input("remove all items from the scale and press enter...")
        print ("taring scale")
        self.ser.write(b'x')
        time.sleep(2)
        self.ser.write(b'1')
        time.sleep(2)
        self.ser.write(b'x')
        time.sleep(2)
        self.ser.reset_input_buffer()

    def current_weight(self):
        return self.parser(1)[0]

    def initial_tower_weight(self):
        """
        take initial weight of the tower
        """ 
        print ("waiting for blocks")

        while self.current_weight() < 1:
            pass

        std = 1
        stdmin = self.std_trigger

        while std > stdmin:
            print (std,end='\r')
            data = self.parser(5)
            std = np.std(data)
  
        return np.average(data)       


    def parser(self,items):
        """
        return float list of most recent append (items) from
        pyserial read. try until clean data is obtained.
        """
        while True:
            try:
                data = self.buffer[-100:]
                items_to_parse = data.split()[-items:]
                result = [float(i.split(',')[0]) for i in items_to_parse]
                break
            except:
                if self.buffer[-4:] == "Exit":
                    self.ser.write(b'x')

        return result 

    def on(self):
        """ return true if scale status equals on """
        return self.status() == "on"

    def off(self):
        """ return true if scale status equals off """
        return self.status() == "off"

    def paused(self):
        """ return true if scale status equals paused """
        return self.status() == "paused"

    def collapsed(self):
        """ return true if scale status equals collapsed """
        return self.status() == "collapsed"

    def disqualified(self):
        """ return true if scale status equals disqualifed """
        return self.status() == "disqualified"
   
    def status(self):
        """ 
        return the current status of the scale based on the average weight
        of the last four data elements
        """
        #import ipdb; ipdb.set_trace()
        dset = self.parser(4)
        self.avg = sum(dset)/4
        self.std = np.std(dset)

        if self.off_max >= self.avg >= self.off_min and self.std < self.std_trigger:
            self.current_status = "off"
            return "off"
        elif self.on_max >= self.avg >= self.on_min and self.std < self.std_trigger:
            self.current_status = "on"
            return "on"
        elif self.two_off >= self.avg >= self.collapse and self.std < self.std_trigger:
            self.current_status = "disqualified"
            return "disqualified"
        elif self.avg < self.collapse and self.std < self.std_trigger:
            self.current_status = "collapsed"
            return "collapsed"
        elif self.avg >= self.pause and self.std < self.std_trigger:
            self.current_status = "paused"
            return "paused"
        else:
            return self.current_status


      
def main():
    s = Scale()
    

if __name__ == "__main__":
    main()
