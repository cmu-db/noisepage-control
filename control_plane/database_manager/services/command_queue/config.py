from kombu import Exchange, Queue

ampq_exchange = Exchange("command", "direct", durable=True)
ampq_queue = Queue("command", exchange=ampq_exchange, routing_key="command")

ampq_connection_string = "amqp://%s:%s@%s:%s//" % (
    "guest",
    "guest",
    "localhost",
    "5672",
)
