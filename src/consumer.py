from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue
from src.database.mongo_client import corridas_collection
from src.database.redis_client import redis_client
from src.models.corrida_model import corrida_document

broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672/")
app = FastStream(broker)

# Nome da fila que o main.py publica
queue = RabbitQueue("corridas_finalizadas")

@app.subscriber(queue)
async def processar_corrida(evento: dict):

    print("\n Evento recebido:", evento)

    # 1 — Salvar corrida no MongoDB
    doc = corrida_document(evento)
    corridas_collection.insert_one(doc)
    print(" Corrida salva no MongoDB")

    # 2 — Atualizar saldo no Redis
    motorista = evento["motorista"]["nome"].lower()
    valor = float(evento["valor_corrida"])

    redis_key = f"saldo:{motorista}"

    # Atomicidade com WATCH + MULTI + EXEC
    with redis_client.pipeline() as pipe:
        while True:
            try:
                pipe.watch(redis_key)
                saldo_atual = pipe.get(redis_key)
                if saldo_atual is None:
                    saldo_atual = 0.0
                else:
                    saldo_atual = float(saldo_atual)

                novo_saldo = saldo_atual + valor

                pipe.multi()
                pipe.set(redis_key, novo_saldo)
                pipe.execute()
                break
            except redis_client.WatchError:
                continue

    print(f" Saldo atualizado → {motorista}: +{valor}")

    return {"status": "processado"}
