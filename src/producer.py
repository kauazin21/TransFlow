import os
from rabbit_retry import connect_with_retry

RABBIT_URL = os.getenv("RABBIT_URL", "amqp://guest:guest@rabbitmq:5672/")
broker = None

async def get_broker():
    global broker
    if broker is None:
        broker = await connect_with_retry(RABBIT_URL)
    return broker
