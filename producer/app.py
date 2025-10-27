from confluent_kafka import Producer
from faker import Faker
import json, random, time, os, json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

fake = Faker()

KAFKA_BOOTSTRAP = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
TOPIC = os.environ.get('TOPIC')
TIMER = int(os.environ.get('TIMER'))
__CONFIG = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')))
__PRODUCER = Producer(__CONFIG)


def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print(f"✅ Produced event to topic {msg.topic()}")



def main():
    print("🚀 Starting Transaction Producer...")
    print(f"📡 Connecting to Kafka: {KAFKA_BOOTSTRAP}")

    message_count = 0
    try:
        while True:
            transaction = {
                "transaction_id": fake.uuid4(),
                "user_id": random.randint(1, 100),
                "amount": round(random.uniform(10, 5000), 2),
                "timestamp": fake.iso8601()
            }
            __PRODUCER.produce(
                TOPIC, 
                json.dumps(transaction).encode('utf-8'), 
                callback=delivery_callback
            )
            # Poll to handle delivery reports
            __PRODUCER.poll(0)
            message_count += 1
            print(f"📤 Sent message #{message_count}")
            time.sleep(TIMER)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping producer...")
    except Exception as e:
        print(f"💥 Producer error: {e}")
    finally:
        # Wait for any outstanding messages to be delivered
        __PRODUCER.flush(10)
        print(f"📊 Total messages sent: {message_count}")

if __name__ == "__main__":
    main()