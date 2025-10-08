import os
import json
import psycopg
import datetime
from kafka import KafkaConsumer
from psycopg.rows import dict_row

KAFKA_BROKER = os.getenv('KAFKA_URL')
KAFKA_TOPIC = os.getenv('KAFKA_BOOKING_TOPIC')
CONSUMER_GROUP = 'booking_processors'
DB_ULR = os.getenv('DB_URL')

USERS_STAT_SQL = """
    INSERT INTO users_stat (user_id, count, updated_at)
    VALUES (%s, 1, NOW())
    ON CONFLICT (user_id) DO UPDATE
    SET count = users_stat.count + 1, updated_at = NOW();
"""

HOTELS_STAT_SQL = """
    INSERT INTO hotels_stat (hotel_id, count, updated_at)
    VALUES (%s, 1, NOW())
    ON CONFLICT (hotel_id) DO UPDATE
    SET count = hotels_stat.count + 1, updated_at = NOW();
"""

DAYS_STAT_SQL = """
    INSERT INTO days_stat (date, count, updated_at)
    VALUES (%s, 1, NOW())
    ON CONFLICT (date) DO UPDATE
    SET count = days_stat.count + 1, updated_at = NOW();
"""


def run_consumer(db_connection: psycopg.Connection):
    try:

        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            group_id=CONSUMER_GROUP,
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
    except Exception as e:
        print(f"Error connecting to Kafka: {e}")
        return

    for message in consumer:
        booking_data = message.value
        user_id = booking_data.get("user_id")
        hotel_id = booking_data.get("hotel_id")
        created_at_str = booking_data.get("created_at")

        print("-" * 50)
        print(f"Received BookingCreated from partition {message.partition}, offset {message.offset}:")
        print(f"  User ID: {user_id} Hotel ID: {hotel_id} Created At: {created_at_str}")

        with db_connection.cursor() as cursor:
            created_at = datetime.datetime.fromisoformat(created_at_str)

            cursor.execute(USERS_STAT_SQL, (user_id,))
            cursor.execute(HOTELS_STAT_SQL, (hotel_id,))
            cursor.execute(DAYS_STAT_SQL, (created_at.date(),))

            db_connection.commit()


if __name__ == '__main__':
    run_consumer(psycopg.connect(DB_ULR, row_factory=dict_row))
