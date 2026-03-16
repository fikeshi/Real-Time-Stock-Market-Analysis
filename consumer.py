#python script to consumer data form kafka cluster 

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'stock_analysis',
    bootstrap_servers = ['localhost:9094'],
    auto_offset_reset = 'earliest',
    enable_auto_commit = True,
    group_id = 'my-consumer-group',
    value_deserializer = lambda x: json.loads(x.decode('utf-8'))
)


print("starting Kafka consumer. Waiting for message on topic 'stock analyisi'.... ")


for message in consumer:
    data = message.value 

    print(f"value (Deserialized): {data}")

# consumer.close()
print('Kafka consumer closed')
