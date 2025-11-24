from fastapi import FastAPI
from src.database.mongo_client import corridas_collection
from src.models.corrida_model import corrida_document
from src.producer import broker
from producer import get_broker

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    global broker
    broker = await get_broker()


@app.post("/corridas")
async def cadastrar_corrida(corrida: dict):
    # publica evento
    await broker.publish(
        mensagem=corrida,
        queue="corridas_finalizadas"
    )

    return {"mensagem": "Corrida enviada para processamento!"}

@app.get("/corridas")
def listar_corridas():
    results = list(corridas_collection.find({}, {"_id": 0}))
    return results

@app.get("/corridas/{forma_pagamento}")
def filtrar_por_pagamento(forma_pagamento: str):
    results = list(corridas_collection.find(
        {"forma_pagamento": forma_pagamento},
        {"_id": 0}
    ))
    return results
