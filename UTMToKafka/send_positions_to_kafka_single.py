import datetime
import json
from api import *

from pykafka import KafkaClient
import json
import requests
import time
# from json import jsonify
import numpy as np

print "1"
client = KafkaClient("127.0.0.1:9092")
print "2"
topic = client.topics['status']

oldtime_1 = datetime.datetime(2009, 12,2)
oldtime_2 = datetime.datetime(2009, 12,2)

gufi_1 = '6c4caf0d-1a25-4aaa-bede-97724dbc9fcb'
gufi_2 = 'ac147406-2f44-4f4c-b686-4a9a5a770e08'

with topic.get_sync_producer() as producer:
	while True:
		print "Getting Drone 1 .. "
		pos_1 = getPositions(gufi_1, 1000)
		timedash_1 = ' '.join(json.loads(pos_1)[-1]['time_received'][:-1].split('T'))
		#print timedash
		timethen_1 = time.strptime(timedash_1, '%Y-%m-%d %H:%M:%S')
		if datetime.datetime.fromtimestamp(time.mktime(timethen_1)) > oldtime_1:
			json_msg_1 = json.loads(pos_1)[-1]
			lon, lat = tuple(json.loads(json_msg_1['location'])['coordinates'])
			lon, lat = str(lon), str(lat)
			speed =  str(json_msg_1['speed'])
			heading =  json_msg_1['heading']
			heading = str(heading / 180.0 * np.pi)
			gufi =  str(json_msg_1['gufi'])
			msg_1 = "{\"flightId\":" + "\"" +gufi + "\"" +\
			",\"lat\":\"" + lat + "\"" + \
			",\"lon\":\"" + lon + "\"" + \
			",\"speed\":\"" + speed + "\"" + \
			",\"heading\":\"" + heading + "\"" + "}"
			print msg_1
			producer.produce(msg_1)
			oldtime_1 = datetime.datetime.fromtimestamp(time.mktime(timethen))

		print "Getting Drone 2 .. "
		pos_2 = getPositions(gufi_2, 1000)
		timedash = ' '.join(json.loads(pos_2)[-1]['time_received'][:-1].split('T'))
		#print timedash
		timethen = time.strptime(timedash, '%Y-%m-%d %H:%M:%S')
		if datetime.datetime.fromtimestamp(time.mktime(timethen)) > oldtime_2:
			json_msg = json.loads(pos_2)[-1]
			lon, lat = tuple(json.loads(json_msg['location'])['coordinates'])
			lon, lat = str(lon), str(lat)
			speed =  str(json_msg['speed'])
			heading =  json_msg['heading']
			heading = str(heading / 180.0 * np.pi)
			gufi =  str(json_msg['gufi'])
			msg_2 = "{\"flightId\":" + "\"" +gufi + "\"" +\
			",\"lat\":\"" + lat + "\"" + \
			",\"lon\":\"" + lon + "\"" + \
			",\"speed\":\"" + speed + "\"" + \
			",\"heading\":\"" + heading + "\"" + "}"
			print msg_2
			producer.produce(msg_2)
			oldtime_2 = datetime.datetime.fromtimestamp(time.mktime(timethen))

