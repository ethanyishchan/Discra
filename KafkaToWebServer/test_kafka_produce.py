# from kafka import KafkaClient, KafkaConsumer
from pykafka import KafkaClient

client = KafkaClient("127.0.0.1:9092")
# consumer = KafkaConsumer('my-topic',
#                          group_id='my-group',
#                          bootstrap_servers=['localhost:9092'])

topic = client.topics['conflict']


gufi = "drone1"
lat = "100"
lon = "100"
speed = "3"
heading = "3.14"

with topic.get_sync_producer() as producer:
	for i in range(4):
		msg = "{\"flightId\":" + gufi + \
		",\"lat\":\"" + lat + "\"" + \
		",\"lon\":\"" + lon + "\"" + \
		",\"speed\":\"" + speed + "\"" + \
		",\"heading\":\"" + heading + "\"" + \
		"}"
		print msg
		producer.produce(msg)
