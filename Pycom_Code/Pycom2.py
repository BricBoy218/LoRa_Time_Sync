from network import LoRa
import socket
import time
import machine
import utime
import ujson
import pycom



def fixTme(prop,rtc):
    print(prop)
    tme = utime.time() + int(prop)
    cal = list(utime.gmtime(tme))
    rtc.init(cal)
    print("Fixed Time")
    print(rtc.now())
    print("----------------------------------------------------------------------------------")
    time.sleep(5)
    

def makeTme(tme,rtc):
    cal = list(utime.gmtime(tme))
    rtc.init(cal)
    print("New Time")
    print(rtc.now())
    print("----------------------------------------------------------------------------------")
                        

def send(sock,send_str):
    
    sock.send(send_str)

def makeJson(pac):
    pac = pac.replace("F","f")
    
    try:
        dicT = ujson.loads(pac)
        
    except:
        
        dicT = None
        
    finally:
        return(dicT)
    

def recv(sock):
    pac = sock.recv(64)
    try:
        pac = pac.decode("utf-8")
    except UnicodeError:
        #print("A Unicode error occured")
        #print(pac)
        pac = None
    finally:
        return pac

def main():
    lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, sf = 7)
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sock.setblocking(False)
    
    sync = "false"
    lora.frequency(868100000)
    rtc = machine.RTC()
    rtc.init(utime.localtime(utime.time()))
    print("Starting")
    device_id = "0x02"
    print("Contacting Gateway")
    while True:
        
        
        send_str = "{\"To\" :\"0x00\",\"From\" : \"" + device_id +"\", \"MyTime\" : "+ str(utime.time()) + ", \"Sync\" :" + sync + "}"
        send(sock,send_str)
        time.sleep(1)
        pac = recv(sock)
        time.sleep(1)
        if pac:
            newDicT = makeJson(pac)
            if newDicT:    
                
                if newDicT["To"]=="0xff" or newDicT["To"]== device_id:
                    
                    
                    if newDicT['Sync'] == False:
                        if sync == "true" and newDicT["MyTime"] < 1000:
                            fixTme(newDicT["MyTime"],rtc)
                            
                        else:
                            print("Changing Time")
                            
                            makeTme(int(newDicT['MyTime']),rtc)
                            sync = "true"
                            
                        time.sleep(5)
                    elif newDicT['Sync'] == True:
                        
                        sync = "true"
                        
                        print("Still Synced")
                        time.sleep(120)        
            
                

        
main()