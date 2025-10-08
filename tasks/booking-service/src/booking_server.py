import grpc
import psycopg
import os
import requests
import json
from concurrent import futures

from psycopg.rows import dict_row
from kafka import KafkaProducer

import booking_pb2
import booking_pb2_grpc


class BookingServiceServicer(booking_pb2_grpc.BookingServiceServicer):
    def __init__(self, dsn: str, api_url: str, kafka_url: str, kafka_topic: str):
        self._dsn: str = dsn
        self._api_url: str = api_url
        self._kafka_url = kafka_url
        self._kafka_topic = kafka_topic
        self._connection: psycopg.Connection|None = None
        self._kafka_producer: KafkaProducer|None = None

    def __del__(self):
        if self._connection:
            self._connection.close()
        if self._kafka_producer:
            self._kafka_producer.flush()
            self._kafka_producer.close()

    def CreateBooking(self, request, context):
        user_id = request.user_id
        hotel_id = request.hotel_id
        promo_code = request.promo_code

        print(f"Received CreateBooking request for User ID: {user_id}")

        user = self._get_user(user_id)
        try:
            self._validate_user(user)
            self._validate_hotel(hotel_id)
        except Exception as e:
            context.abort(code=grpc.StatusCode.INVALID_ARGUMENT, details=str(e))

        base_price = self._resolve_basic_price(user)
        discount = self._resolve_promo_discount(promo_code, user)

        final_price = base_price - discount
        booking = self._create_new_booking(user_id, hotel_id, final_price, discount, promo_code)
        self._fire_booking_created_event(user_id, hotel_id, booking['created_at'].isoformat())

        print(f"Booking {booking['id']} created successfully.")

        return self._row_to_response(booking)

    def ListBookings(self, request, context):
        print(f"Received ListBookings request for User ID: {request.user_id}")

        conn = self._get_connect()

        bookings_for_user = []
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM booking WHERE user_id = %s", (request.user_id,))
            bookings_for_user = list((self._row_to_response(booking) for booking in cursor.fetchall()))

        print(f"Found {len(bookings_for_user)} bookings for user {request.user_id}.")
        return booking_pb2.BookingListResponse(bookings=bookings_for_user)

    def _get_connect(self) -> psycopg.connection.Connection:
        if self._connection is None:
            self._connection = psycopg.connect(self._dsn, row_factory=dict_row)

        return self._connection

    def _get_kafka(self) -> KafkaProducer:
        if self._kafka_producer is None:
            self._kafka_producer = KafkaProducer(
                bootstrap_servers=[self._kafka_url],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )

        return self._kafka_producer

    def _fire_booking_created_event(self, user_id: str, hotel_id: str, created_at_str: str):
        producer = self._get_kafka()

        payload = {
            "event_name": "BookingCreated",
            "user_id": user_id,
            "hotel_id": hotel_id,
            "created_at": created_at_str
        }

        record_metadata = producer.send(self._kafka_topic, value=payload).get(timeout=1)

        print("--------------------------------------------------")
        print(f"Successfully sent one BookingCreated message.")
        print(f"  Topic: {record_metadata.topic}")
        print(f"  Partition: {record_metadata.partition}")
        print(f"  Offset: {record_metadata.offset}")
        print(f"  Data: {json.dumps(payload)}")

    def _row_to_response(self, row: dict) -> booking_pb2.BookingResponse:
        return booking_pb2.BookingResponse(
            id=str(row['id']),
            user_id=row['user_id'],
            hotel_id=row['hotel_id'],
            promo_code=row['promo_code'],
            discount_percent=round(row['discount_percent'], 2),
            price=round(row['price'], 2),
            created_at=row['created_at'].isoformat()
        )

    def _create_new_booking(self, user_id: str, hotel_id: str, price: float, discount: float, promo_code: str) -> dict:
        conn = self._get_connect()
        q = """
          INSERT INTO public.booking (
              user_id, hotel_id, price, discount_percent, promo_code, created_at
          ) VALUES (
              %s, %s, %s, %s, %s, NOW()
          ) RETURNING *;
          """

        with conn.cursor() as cursor:
            cursor.execute(q, (user_id, hotel_id, price, discount, promo_code))
            new_booking_row = cursor.fetchone()
            conn.commit()

        return new_booking_row

    def _get_user(self, user_id: str) -> dict:
        return requests.get(''.join([self._api_url, f'/users/{user_id}'])).json()

    def _validate_user(self, user: dict) -> None:
        if user['blacklisted']:
            raise Exception('User is blacklisted')

        if not user['active']:
            raise Exception('User is inactive')

    def _validate_hotel(self, hotel_id: str) -> None:
        hotel = requests.get(''.join([self._api_url, f'/hotels/{hotel_id}'])).json()
        if not hotel['operational']:
            raise Exception('Hotel is not operational')

        if hotel['fullyBooked']:
            raise Exception('Hotel is fully booked')

        trusted = requests.get(''.join([self._api_url, f'/reviews/hotel/{hotel_id}/trusted'])).text

        if trusted.lower() != 'true':
            raise Exception('Hotel is not trusted based on reviews')

    def _resolve_basic_price(self, user: dict) -> float:
        return 80.0 if user['status'].lower() == 'vip' else 100.0

    def _resolve_promo_discount(self, promo_code: str, user: dict) -> float:
        data = {
            'userId': user['id'],
            'code': promo_code,
        }
        response = requests.post(''.join([self._api_url, f'/promos/validate']), data)

        return 0 if response.status_code != 200 else float(response.json()['discount'])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServiceServicer_to_server(
        BookingServiceServicer(
            os.getenv('DB_URL'),
            os.getenv('MONOLITH_API_URL'),
            os.getenv('KAFKA_URL'),
            os.getenv('KAFKA_BOOKING_TOPIC'),
        ), server)

    server_address = f'[::]:50051'
    server.add_insecure_port(server_address)
    server.start()

    print(f"🚀 gRPC Server started, listening on {server_address}")

    server.wait_for_termination()


if __name__ == '__main__':
    serve()
