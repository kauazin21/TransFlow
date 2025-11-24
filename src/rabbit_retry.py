import asyncio
from faststream.rabbit import RabbitBroker

async def connect_with_retry(url, retries=20, delay=3):
    for _ in range(retries):
        try:
            broker = RabbitBroker(url)
            await broker.connect()
            return broker
        except Exception:
            print("RabbitMQ não disponível, tentando de novo...")
            await asyncio.sleep(delay)
    raise Exception("Falha ao conectar no RabbitMQ após vários retries")
