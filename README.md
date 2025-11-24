# TransFlow – Sistema de Processamento Assíncrono com FastAPI, RabbitMQ, MongoDB e Redis

Este projeto demonstra uma arquitetura completa baseada em mensageria usando **FastAPI**, **RabbitMQ**, **MongoDB** e **Redis**, com **producer/consumer** totalmente funcionais dentro de containers Docker.

---

## 🚀 **1. Passos de Instalação**

### **Pré-requisitos**

* Docker
* Docker Compose
* Python 3.11+ (somente se quiser rodar localmente)

### **Instalando e executando o projeto (via Docker)**

```bash
docker compose up --build -d
```

Isso irá subir automaticamente:

* API FastAPI (porta 8000)
* RabbitMQ + painel (portas 5672 / 15672)
* MongoDB (porta 27017)
* Redis (porta 6379)
* Consumer (processador assíncrono)

Após subir, verifique os containers:

```bash
docker ps
```

Para ver logs da API:

```bash
docker logs transflow_api
```

Para ver logs do consumer:

```bash
docker logs transflow_consumer
```

---

## 🔧 **2. Variáveis de Ambiente Necessárias**

Crie um arquivo `.env` na raiz com:

```env
RABBIT_URL=amqp://guest:guest@rabbitmq:5672/
MONGO_URL=mongodb://mongo:27017/
REDIS_HOST=redis
```

* `RABBIT_URL`: conexão com o RabbitMQ
* `MONGO_URL`: conexão com o MongoDB
* `REDIS_HOST`: host do Redis dentro do Docker Compose

> Caso não exista `.env`, valores padrão já serão utilizados.

---

## 🧪 **3. Instruções de Uso e Testes**

### **Acessar a API (Swagger UI)**

Acesse:

```
http://localhost:8000/docs
```

### **Rotas disponíveis**

#### **POST /corridas**

Envia uma corrida para processamento.
Exemplo:

```json
{
  "motorista": {"nome": "João"},
  "valor_corrida": 25.5,
  "forma_pagamento": "pix"
}
```

#### **GET /corridas**

Retorna todas as corridas salvas no MongoDB.

#### **GET /corridas/{forma_pagamento}**

Filtra corridas por forma de pagamento.

### **Fluxo Interno**

1. A API publica uma mensagem no RabbitMQ.
2. O Consumer recebe a mensagem.
3. A corrida é salva no MongoDB.
4. O saldo do motorista é atualizado no Redis.

---

## 📸 **4. Captura de Tela do Sistema em Execução**


```md
![TransFlow rodando](./screenshot_transflow.png)
```

---

## 📦 Estrutura do Projeto

```
project/
├── docker-compose.yml
├── Dockerfile
├── src/
│   ├── main.py
│   ├── producer.py
│   ├── consumer.py
│   ├── database/
│   ├── models/
│   └── ...
├── requirements.txt
└── README.md
```

---