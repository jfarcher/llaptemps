#!/usr/bin/python
import mosquitto
import os
import time
import serial
import datetime
import re

broker = "192.168.1.3"
tcpport = 1883
baud = 115200
port = '/dev/ttyAMA0'
ser = serial.Serial(port, baud)

mypid = os.getpid()
client_uniq = "pubclient_"+str(mypid)
mqttc = mosquitto.Mosquitto(client_uniq)

#Connect to broker
mqttc.connect(broker, tcpport, 60, True)

#Remain connected and publish
while mqttc.loop() == 0:
        llapMsg = ser.read(12)
        devID = llapMsg[1:3]
        temp = llapMsg[7:12]
	while temp.endswith("-"):
			temp = temp[:-1]
	mqttc.publish("house/temp/" + devID,temp)

