import grpc
import booking_pb2
import booking_pb2_grpc

SERVER_ADDRESS = 'localhost:50051'


def create_booking(stub, user_id, hotel_id, promo_code=""):
    print(f"\n--- Creating Booking for User: {user_id} ---")

    request = booking_pb2.BookingRequest(
        user_id=user_id,
        hotel_id=hotel_id,
        promo_code=promo_code
    )

    try:
        response = stub.CreateBooking(request)

        print(f"Successfully created Booking ID: {response.id}")
        print(f"  Hotel ID: {response.hotel_id}")
        print(f"  Price: ${response.price:.2f}")
        if response.promo_code:
            print(f"  Promo Code Used: {response.promo_code} (Discount: {response.discount_percent:.2f}%)")
        return response

    except grpc.RpcError as e:
        print(f"RPC Error during CreateBooking: {e.code().name} - {e.details()}")
        return None


def list_bookings(stub, user_id):
    print(f"\n--- Requesting Bookings for User: {user_id} ---")

    request = booking_pb2.BookingListRequest(user_id=user_id)

    try:
        response = stub.ListBookings(request)

        if not response.bookings:
            print("No bookings found for this user.")
            return

        print(f"Found {len(response.bookings)} total bookings:")
        for i, booking in enumerate(response.bookings, 1):
            print(
                f"  {i}. ID: {booking.id[:8]}... | Hotel: {booking.hotel_id} | Price: ${booking.price:.2f} | Created: {booking.created_at}")

    except grpc.RpcError as e:
        print(f"RPC Error during ListBookings: {e.code().name} - {e.details()}")


def run():
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = booking_pb2_grpc.BookingServiceStub(channel)

    print(f"Connecting to gRPC server at {SERVER_ADDRESS}...")
    create_booking(stub,
                   user_id='test-user-2',
                   hotel_id="test-hotel-1",
                   promo_code="TESTCODE1")

    create_booking(stub,
                   user_id='test-user-3',
                   hotel_id="test-hotel-2")

    list_bookings(stub, user_id='test-user-2')

    channel.close()


if __name__ == '__main__':
    run()
