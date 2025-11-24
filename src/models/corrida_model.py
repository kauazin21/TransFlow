def corrida_document(data: dict) -> dict:
    return {
        "id_corrida": data["id_corrida"],
        "passageiro": {
            "nome": data["passageiro"]["nome"],
            "telefone": data["passageiro"]["telefone"]
        },
        "motorista": {
            "nome": data["motorista"]["nome"],
            "nota": data["motorista"]["nota"]
        },
        "origem": data["origem"],
        "destino": data["destino"],
        "valor_corrida": data["valor_corrida"],
        "forma_pagamento": data["forma_pagamento"]
    }
