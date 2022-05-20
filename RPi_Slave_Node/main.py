#! /usr/bin/python3
import os
import time
import json

def recv():
	out = os.popen('./dragino_lora_app recv')
	try:
		message = out.read()	
		return message	
	except:
		print("")

		
	

def make_JSON(mess):
	try:
		dicT = json.loads(mess)
	except json.decoder.JSONDecodeError:
		dicT = None
	return dicT	

def main():
	print("Started")
	device_id = "0x03"

	#os.system(cmd)
	sync = "false"
	
	while True:
		
		for i in range (0,12):
			tme = time.mktime(time.localtime())

			send_str = "{\"To\":\"0x00\",\"From\":\"" + device_id + "\",\"MyTime\":"+ str(tme) + ",\"Sync\":" + sync + "}" 
			send_str = json.dumps(send_str)
			cmd = './dragino_lora_app sender ' + str(send_str) 
			time.sleep(.5)
			i += 1
				
		
		os.system(cmd)
		time.sleep(.5)
		message = recv()
		if message:
			dicT = make_JSON(message)
		
			if dicT:
				if dicT["To"] == device_id or dicT["To"] == "0xff" :
					print("Message Recieved")
					if dicT["Sync"] == False:
						recvtme = dicT["MyTime"] 
						print(recvtme)
						if sync == "false":
							cmd = "sudo python3 time.py " + str(recvtme)
							os.system(cmd)
							print("Time Changed")
							sync = "true"
						elif sync == "true":
							cmd = "sudo python3 time.py " + str(recvtme)
							os.system(cmd)
							print("Time Updated")
					elif dicT["Sync"] == True:
						print("Synced up!!!")
						time.sleep(120)
			



		
	
				


						
				
main()
