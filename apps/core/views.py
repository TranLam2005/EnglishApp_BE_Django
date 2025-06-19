import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
import pika
import redis
import time

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0) # connect redis params1 host, params2 port redis will listen on this port, param3 db=0 redis has 16 database indexed from 0 to 15 db assign db[0] to do cache
def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    chanel = connection.channel()
    chanel.queue_declare(queue="request_queue", durable=True)
    return chanel

LIMIT = 10
KEY = "request_this_second"

def send_request_to_queue(request):

    chanel = connect_to_rabbitmq()
    chanel.basic_publish(
        exchange='',
        routing_key='request_queue',
        body=request,
    )
    print(f"Request added to queue: {request}")
def process_request(request):
    print(f"Processing request")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secret_view(request):
    current_request = redis_client.get(KEY)
    user_id = request.user.id
    if current_request and int(current_request) > LIMIT:
        send_request_to_queue(request)
        start_time = time.time()
        while time.time() - start_time < 30:
            result = redis_client.get(user_id)
            if user_id:
                result_data = json.loads(result)
                return Response(result_data)
        return Response({"message": "Request queued (over limit)"}, status=202)
    redis_client.incr(KEY)
    redis_client.expire(KEY, 1)
    user = UserSerializer(request.user).data
    return Response({"message": "This is view protected", "user": user})