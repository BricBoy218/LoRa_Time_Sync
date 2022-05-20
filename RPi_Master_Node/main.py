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
		print("JSON decode error")
	
		
def getGps_time():						
	cmd = "sudo python3 gps_time.py"
				
	os.system(cmd)


		
def make_JSON(mess):
	
	try:
		dicT = json.loads(mess)
	except json.decoder.JSONDecodeError:
		dicT = None
	finally:
		return dicT   

def main():
	print("Started")
	device_id = "0x00"
	toDevice = "0xff"
	#os.system(cmd)
	sync = "false"
	prop = 0
	pyNode1= False
	pyNode2= False
	rpiNode1= False
	getGps_time()
	while True:
		message = recv()
		if message:
			dicT = make_JSON(message)
	
		if dicT:
			
			
			
					
			if dicT['To'] == device_id and dicT['Sync'] == False:
				
				rcvTme = dicT['MyTime']
				if dicT["From"] == "0x01":
					print("Device Unsynced = Pycom1 @ " + str(time.mktime(time.localtime()))+ ", Device Time = " + str(rcvTme)+", Sending time now")
					toDevice = "0x01"
					sync = "false"
					pyNode1= False
			
					for i in range (0,12):
						tme = time.mktime(time.localtime())
						send_str = "{\"To\":\""+ toDevice +"\",\"From\":\"" + device_id + "\",\"MyTime\":"+ str(tme) + ",\"Sync\":" + sync + "}" 
						
						send_str = json.dumps(send_str)
						#print(len(send_str))
						cmd = './dragino_lora_app sender ' + str(send_str) 
				
						os.system(cmd)
						i+=1
				elif dicT["From"] == "0x02":
					print("Device Unsynced = Pycom2 @ " + str(time.mktime(time.localtime())) + ", Device Time = " + str(rcvTme) + ", Sending time now")
					toDevice = "0x02"
					sync = "false"
	
					pyNode2= False
		
					for i in range (0,12):
						tme = time.mktime(time.localtime())
						send_str = "{\"To\":\""+ toDevice +"\",\"From\":\"" + device_id + "\",\"MyTime\":"+ str(tme) + ",\"Sync\":" + sync + "}" 
						
						send_str = json.dumps(send_str)
						#print(len(send_str))
						cmd = './dragino_lora_app sender ' + str(send_str) 
				
						os.system(cmd)
						i+=1
						
				elif dicT["From"] == "0x03":
					print("Device Unsynced = RPi_node @ " + str(time.mktime(time.localtime()))+ ", Device Time = " + str(rcvTme)+", Sending time now")
					toDevice = "0x03"
					sync = "false"
				

					rpiNode1= False			
					for i in range (0,12):
						tme = time.mktime(time.localtime())
						send_str = "{\"To\":\""+ toDevice +"\",\"From\":\"" + device_id + "\",\"MyTime\":"+ str(tme) + ",\"Sync\":" + sync + "}" 
						
						send_str = json.dumps(send_str)
						#print(len(send_str))
						cmd = './dragino_lora_app sender ' + str(send_str) 
				
						os.system(cmd)
						i+=1


			elif dicT['To'] == device_id and dicT['Sync'] == True:
				print(dicT["From"])
				tme = time.mktime(time.localtime())
				print("---------------------------------------------------------")
				rcvTme = dicT['MyTime']
			
				prop = tme - rcvTme
				
				
				if rcvTme == tme:
					if dicT["From"] == "0x01":
						print("****************************************************************")
						print("Device Synced = Pycom1 @ " + str(time.mktime(time.localtime())))
						print("****************************************************************")
						toDevice = "0x01"
						pyNode1= True

					elif dicT["From"] == "0x02":
						print("****************************************************************")
						print("Device Synced = Pycom2 @ " + str(time.mktime(time.localtime())))
						print("****************************************************************")
						toDevice = "0x02"
						pyNode2= True
	
					elif dicT["From"] == "0x03":
						print("****************************************************************")
						print("Device Synced = RPi_node @ " + str(time.mktime(time.localtime())))
						print("****************************************************************")
						toDevice = "0x03"
						rpiNode1= True
					sync = "true"
					for i in range (0,12):
						tme = time.mktime(time.localtime())
						tme = tme + prop
						send_str = "{\"To\":\""+ toDevice +"\",\"From\":\"" + device_id + "\",\"MyTime\":"+ str(prop) + ",\"Sync\":" + sync + "}" 
						send_str = json.dumps(send_str)
						cmd = './dragino_lora_app sender ' + str(send_str) 
						os.system(cmd)
						i+=1
					print("---------------------------------------------------------")
				else:
					print("Difference = " + str(prop))
					sync = "false"
					if dicT["From"] == "0x01":
						print("Sending Difference to Pycom1")
						pyNode1= False

					elif dicT["From"] == "0x02":
						print("Sending Difference to Pycom2")
						pyNode2= False
	
					elif dicT["From"] == "0x03":
						print("Sending Difference to RPi_node")
				
						rpiNode1= False
					
					for i in range (0,20):
						tme = time.mktime(time.localtime())
						tme = tme + prop
						send_str = "{\"To\":\""+ dicT["From"] +"\",\"From\":\"" + device_id + "\",\"MyTime\":"+ str(prop) + ",\"Sync\":" + sync + "}" 
						send_str = json.dumps(send_str)
						cmd = './dragino_lora_app sender ' + str(send_str) 
						os.system(cmd)
						i+=1
					
					
			if pyNode1 == True and pyNode2 == True and 	rpiNode1 == True:
				print("!!!!!!!!!!!!!!!!!!!!")
				print("!!System Synced!!!!!")
				print("!!!!!!!!!!!!!!!!!!!!")
				getGps_time()



		
	
				


						
				
main()
