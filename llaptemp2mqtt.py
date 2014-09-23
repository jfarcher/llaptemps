#!/usr/bin/python
#import mosquitto
import paho.mqtt.client as mqtt
import os
import time
import serial
import datetime
import re
import sys
import signal

def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

broker = "192.168.1.3"
tcpport = 1883
baud = 115200
port = '/dev/ttyAMA0'
ser = serial.Serial(port, baud)

mypid = os.getpid()
client_uniq = "pubclient_"+str(mypid)
#mqttc = mosquitto.Mosquitto(client_uniq)
mqttc = mqtt.Client()

#Connect to broker
#mqttc.connect(broker, tcpport, 60, True)
mqttc.connect (broker, tcpport, 60)
#Remain connected and publish
#while mqttc.loop() == 0:
mqttc.loop_start()
while True:
	llapMsg = ser.read(12)
        devID = llapMsg[1:3]
	sensor = llapMsg[3:7]
        temp = llapMsg[7:12]
	while temp.endswith("-"):
			temp = temp[:-1]
	if sensor == "TEMP":
		mqttc.publish("house/temp/" + devID,temp, retain=True)
mqttc.loop_forever()
