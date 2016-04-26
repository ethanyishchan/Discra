from pykafka import KafkaClient
import json
import requests
import time
# from json import jsonify

print "1"
client = KafkaClient("127.0.0.1:9092")
print "2"

def postAdvisories(url, pos):
	r = requests.post(url, verify=False,data= pos)

topic_name = "advisory"

simulator_url = "http://127.0.0.1:5000/consume_advisory"
live_url = "http://127.0.0.1:5000/consume_advisory_live"

live = True
# live = False

if live:
	post_url = live_url
else:
	post_url = simulator_url
	
topic = client.topics[topic_name]
consumer = topic.get_simple_consumer()
for msg in consumer:
	if msg is not None:
		# time.sleep(1)
		json_string = msg.value
		json_status = json.loads(json_string)
		# print json_string
		json_packet_list = json_status['advisories']
		print json_packet_list
		postAdvisories(post_url, json.dumps(json_packet_list))
