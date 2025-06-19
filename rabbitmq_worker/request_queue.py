import pika
import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    chanel = connection.channel()
    chanel.queue_declare(queue='request_queue')
    return chanel

def process_request_from_queue(ch, method, properties, body):
    req = json.loads(body.decode())
    user_id = req["user_id"]
    request_info = req["request_body"]

    result = {
        "status": "success", "user_id": user_id
    }
    redis_client.set(user_id, json.dumps(result))

    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_worker():
    chanel = connect_to_rabbitmq()
    chanel.basic_consume(queue='request_queue', on_message_callback=process_request_from_queue)
    chanel.start_consuming()
if __name__ == '__main__':
    start_worker()