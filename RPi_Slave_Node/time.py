import time 
import sys
tme = float(sys.argv[1])
print(tme)
if tme > 1000:
	time.clock_settime(time.CLOCK_REALTIME, tme)
	sys.exit()
	
else:
	now = time.time()
	tme = tme + now
	time.clock_settime(time.CLOCK_REALTIME, tme)
