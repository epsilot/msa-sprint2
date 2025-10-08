# build
FROM python:3.12-slim as builder

WORKDIR /app

RUN pip install --no-cache-dir grpcio==1.75.1 grpcio-tools==1.75.1

COPY ./src/booking.proto /app/

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. booking.proto


# run
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/booking_pb2.py /app/booking_pb2_grpc.py /app/
COPY ./src/booking_server.py ./src/booking.proto ./src/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50051
ENV PYTHONUNBUFFERED 1

CMD ["python", "booking_server.py"]
