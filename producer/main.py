# Entry point for the stock data pipeline.
# Fetches stock data from the API and publishes each record to a Kafka topic.

from extract import connect_to_api, extract_json
from producer_setup import init_producer, topic
import time



#Fetches stock data from the API and stream each record to a Kafka topic
def main():
    response = connect_to_api()

    data = extract_json(response)

    producer = init_producer()


    for stock in data:
        # Select only the fields we want to, drop any extra API fields.
        result = {
            'date': stock['date'],
            'symbol': stock['symbol'],
            'open':stock['open'],
            'low':stock['low'],
            'high':stock['high'],
            'close':stock['close'],
        }

        producer.send(topic, result)

        print(f'Data sent to {topic} topic')

        time.sleep(2)
    producer.flush()
    producer.close()
    return None



if __name__ == '__main__':
    main()