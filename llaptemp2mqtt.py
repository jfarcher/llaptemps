#!/usr/bin/python
import mosquitto
import os
import time
import serial
import datetime
import re
#import eeml

broker = "127.0.0.1"
tcpport = 1883
baud = 9600
port = '/dev/pts/4'
#port = '/dev/ttyAMA0'
ser = serial.Serial(port, baud)

mypid = os.getpid()
client_uniq = "pubclient_"+str(mypid)
mqttc = mosquitto.Mosquitto(client_uniq)

#Connect to broker
mqttc.connect(broker, tcpport, 60, True)

#Remain connected and publish
while mqttc.loop() == 0:
        llapMsg = ser.read(12)
	#llapMsg = "aA1TEMP13---"
	print llapMsg
        #mqttc.publish("TempSensors", llapMsg)
        devID = llapMsg[1:3]

        if re.search("aA1TEMP", llapMsg):
                temp = llapMsg[7:12]
		mqttc.publish(devID + "TempSensor",temp)

        if re.search("aA2TEMP", llapMsg):
                temp = llapMsg[7:12]
		mqttc.publish(devID + "TempSensor",temp)

        #Push data to XIVELY
        try:
		print llapMsg
        except:
                print("ERROR : Failed to Send...")
