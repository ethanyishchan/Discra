import json
import time 
from pykafka import KafkaClient

f = open('032416_live_demo.txt').read()
f = open('032416_converted_curated.txt').read()

counter = 0
print "1"
client = KafkaClient("127.0.0.1:9092")
print "2"
topic = client.topics['status']

# oldtime_1 = datetime.datetime(2009, 12,2)
# oldtime_2 = datetime.datetime(2009, 12,2)

# gufi_1 = '6c4caf0d-1a25-4aaa-bede-97724dbc9fcb'
# gufi_2 = 'ac147406-2f44-4f4c-b686-4a9a5a770e08'

with topic.get_sync_producer() as producer:
	curr_data = f.split("\n")
	for i in range(0,len(curr_data)-1,2):
		counter += 1
		# if i <= len()
		line = curr_data[i] +  "~" + curr_data[i+1]
		print line
		producer.produce(line)
		# json_msg = json.loads(line)
		# if counter % 2  == 0:
		# 	time.sleep(0.1)
		# print json_msg
