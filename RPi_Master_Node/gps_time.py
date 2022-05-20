import serial
import re
import time
port = "/dev/serial0"

            
def main():
    serialPort = serial.Serial(port, baudrate = 9600, timeout = 1.0)

    try:
        stra = str(serialPort.readline())
        x = stra.find("GNRMC")
        if x > 0: 
            strb = stra.split("r")
            
              
            for i in range (0,len(strb)):
                
                j = re.search("GNRMC",strb[i])
                if j:
                    nmeaS = strb[i] 
                    
            
            par = nmeaS.split(",")
            timeStamp = par[1] + par[9]
            hrs = timeStamp[0] + timeStamp[1]
            minutes = timeStamp[2] + timeStamp[3]
            sec = timeStamp[4] + timeStamp[5]
            day = timeStamp[10] + timeStamp[11] 
            month = timeStamp[12] + timeStamp[13]
            year = "20" + timeStamp[14] + timeStamp[15]
            
            tt = (int(year),int(month),int(day),int(hrs),int(minutes),int(sec),0,0,0)
            epoch = time.mktime(tt)
            time.clock_settime(time.CLOCK_REALTIME, epoch)
            print("Time changed to GPS time")
            print("System time now " + str(time.gmtime(time.time())))
        else:
            print("Time message not obtained from GPS")
   
    except:
        print("Error getting gps time")
    

main()
