from lib.scale import Scale
from matplotlib import pyplot as plt
import time
import numpy as np

def graph():

    scale = Scale() 

    x = [] 
    x_vert = []
    y1 = []
    y2 = [] 
    y3 = [] 
    y4 = [] 
    y5 = []
    y6 = []
    y7 = []
    y8 = []

    axv_count = 0
    start = time.time()
    base = scale.tower_wt - scale.min_block_wt * 4
    start_time = time.time()
    input("Press enter to start graphing. Press down on tower lightly to end analysis.")
    print (base)

    while True:

        print ("status:{} wt:{} min:{} max:{}".format(scale.status(),round(scale.avg,4),scale.off_min,scale.off_max),end='\r')

        y1.append(scale.avg)
        y2.append(scale.off_min)
        y3.append(scale.off_max)
        y4.append(scale.std + base)
        y5.append(scale.on_min)
        y6.append(scale.on_max)
        y7.append(scale.std_trigger + base)
        y8.append(scale.pause)
 
        if scale.off() and axv_count == 0:
            x_vert.append(time.time() -start_time)
            x.append(time.time() -start_time)
            axv_count += 1
        else:
            x.append(time.time() - start_time)
   
        if scale.on():
            axv_count = 0

        if scale.current_weight() > 2:
            break

    #plot everything
    plt.plot(x,y7,label='std trigger', color='black')
    plt.plot(x,y1,label='current weight', color='blue', alpha=.6)
    plt.plot(x,y2,label='off range', color='yellow', alpha=0.2)
    plt.plot(x,y5,label='on range', color='grey', alpha=0.2)
    plt.plot(x,y4,label='tower std + 1.68', color='red', alpha=.6)
    plt.plot(x,y3,color='yellow', alpha=0.2)
    plt.plot(x,y6,color='grey', alpha=0.2)
    plt.plot(x,y8,label='pause line', color='blue', alpha=0.2)

    for xc in x_vert:
        plt.axvline(x=xc, color='k', linestyle='--')

    plt.xlabel('Seconds')
    plt.ylabel('Weight')
    plt.legend()

    plt.fill_between(x,y2,y3,color='yellow',alpha=0.2) #interpolate=True
    plt.fill_between(x,y5,y6,color='grey',alpha=0.2) #interpolate=True
    plt.title('Scale Status')

    scale.stop()        
    print ('graphing...')
    plt.show()
       
    std_list = zip(y4,y1) #zip std and average weight together into a tuple list
    std_list = [x[0] for x in std_list if x[1] < scale.off_max and x[1] > scale.off_min]
    print (min(std_list) - 1.64)
    print (x_vert)

def write_to_file(self,info):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    with open("zero_outputs_" + timestr,'w') as f:
        f.write(info)

if __name__ == "__main__":
    graph()
