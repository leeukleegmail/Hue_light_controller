from umqtt.simple import MQTTClient
from config import queue_topic, mq_host, send_client


def send_log_message_to_queue(log_message):
    c = MQTTClient(send_client, mq_host)
    c.connect()
    message = bytes(str(log_message), 'utf-8')
    print(message)
    c.publish(str.encode(queue_topic), message)
    c.disconnect()
