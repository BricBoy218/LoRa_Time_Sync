# main.py -- put your code here!
import pycom
import time
from network import WLAN
wlan = WLAN()

wlan.deinit()
pycom.heartbeat(False)
wlan.init(mode=WLAN.AP, ssid='Pycom1')
while True:
    pycom.rgbled(0xFF0000)  # Red
    time.sleep(1)    
    pycom.rgbled(0x00FF00)  # Green
    time.sleep(1)
    pycom.rgbled(0x0000FF)  # Blue
    time.sleep(1)
    print(wlan.ifconfig(id=1))
print("Done")

#pycom.rgbled()