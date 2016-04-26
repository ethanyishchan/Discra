from pykafka import KafkaClient
import json
import requests
import time


print "1"
client = KafkaClient("127.0.0.1:9092")
print "2"

simulator_url = "http://127.0.0.1:5000/conflict"
live_url = "http://127.0.0.1:5000/conflict_live"

live = True
# live = False

if live:
	post_url = live_url
else:
	post_url = simulator_url

def postPosition(url, pos):
	r = requests.post(url, verify=False,data= pos)

def getJsonPos(json_string):
	json_status = json.loads(json_string)
	position = json_status['flightId'] + "~" + json_status['lat'] + "~" +  json_status['lon']	 + "~" + json_status['heading']
	print position
	return position
topic_name = "status"
topic = client.topics[topic_name]
consumer = topic.get_simple_consumer()
for msg in consumer:
	if msg is not None:
		# time.sleep(1)
		print "msgmsg: ",msg
		json_string = msg.value
		drone1_json, drone2_json = json_string.split("~")

		# json_status = json.loads(json_string)
		# position = json_status['flightId'] + "~" + json_status['lat'] + "~" +  json_status['lon']	 + "~" + json_status['heading']
		# print "posting: ", position
		postPosition(post_url, getJsonPos(drone1_json))
		postPosition(post_url, getJsonPos(drone2_json))