from kombu import Exchange, Queue

from django.conf import settings

ampq_exchange = Exchange("message", "direct", durable=True)
ampq_queue = Queue("message", exchange=ampq_exchange, routing_key="message")

""" 
    These settings would be available only in CONTROL_PLANE mode
    But that's alright, since this file would be loaded only by CONTROL_PLANE
"""
ampq_connection_string = "amqp://%s:%s@%s:%s//" % (
    settings.AMPQ_USER,
    settings.AMPQ_PASSWORD,
    settings.AMPQ_URL,
    settings.AMPQ_PORT,
)
