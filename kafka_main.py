import asyncio
import json
import os
from typing import List
from random import shuffle

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, HTTPException
from loguru import logger

# Load environment variables
load_dotenv(find_dotenv(".env"))

# Environment Variables with Default Values
SPIDEY_NAMES = os.environ.get("SPIDEY_NAMES", "").split(",")
SPIDERWEB_TOPIC = os.environ.get("SPIDERWEB_TOPIC", "spiderweb")
MY_NAME = os.environ.get("MY_NAME", "Tom Holland")

ENV = os.environ.get("ENV", "local")
if ENV == "local":
    KAFKA_BOOTSTRAP_SERVERS = "localhost:9093"
elif ENV == "docker":
    KAFKA_BOOTSTRAP_SERVERS = "kafka:29092"
else:
    raise ValueError("Invalid environment. Set ENV to either 'local' or 'docker'.")

# logger.info(f"SPIDEY_NAMES: {SPIDEY_NAMES}")
# logger.info(f"KAFKA_BOOTSTRAP_SERVERS: {KAFKA_BOOTSTRAP_SERVERS}")
# logger.info(f"SPIDERWEB_TOPIC: {SPIDERWEB_TOPIC}")
# logger.info(f"MY_NAME: {MY_NAME}")

# Validate environment variables
if not SPIDEY_NAMES or not KAFKA_BOOTSTRAP_SERVERS or not SPIDERWEB_TOPIC:
    raise ValueError(
        "Environment variables SPIDEY_NAMES, KAFKA_BOOTSTRAP_SERVERS, and SPIDERWEB_TOPIC must be set."
    )

# Create a FastAPI app
app = FastAPI(
    title="Spiderweb", version="0.1.0", description="A simple spiderweb service"
)

# Kafka Producer Initialization
producer = None
consumer_task = None


async def initialize_producer():
    """Initialize Kafka producer."""
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()


async def shutdown_producer():
    """Shutdown Kafka producer."""
    global producer
    if producer:
        await producer.stop()
        producer = None


def spidey_random(spidey_list: List) -> List:
    """Randomize the list of spideys."""
    if not spidey_list:
        raise ValueError("Spidey list cannot be empty.")
    shuffle(spidey_list)
    return spidey_list


def kafka_serializer(value):
    """Serialize the value to JSON."""
    return json.dumps(value).encode()


def encode_json(msg):
    """Decode the JSON message."""
    return json.loads(msg.value.decode("utf-8"))


async def send_one(topic: str, msg: List):
    """Send a message to Kafka."""
    try:
        await initialize_producer()
        await producer.send_and_wait(topic, kafka_serializer(msg))
        logger.info(f"Message sent to topic {topic}: {msg}")
    except Exception as err:
        logger.error(f"Kafka producer error: {err}")
        raise HTTPException(status_code=500, detail="Error sending message to Kafka")


async def spiderweb_turn(msg):
    """Handle a Kafka message."""
    try:
        finalists = encode_json(msg)
        if MY_NAME == finalists[0]:
            logger.info(f"{MY_NAME} is the winner!")
        else:
            logger.info(f"{MY_NAME} did not win this turn.")

        if len(finalists) > 1:
            finalists.pop(0)
            await send_one(SPIDERWEB_TOPIC, finalists)
    except Exception as e:
        logger.error(f"Error processing spiderweb turn: {e}")


async def consume():
    """Consume Kafka messages."""
    try:
        consumer = AIOKafkaConsumer(
            SPIDERWEB_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        )
        await consumer.start()
        logger.info("Kafka consumer started.")
        async for msg in consumer:
            logger.info(f"Received message from topic {msg.topic}: {msg.value}")
            await spiderweb_turn(msg)
    except Exception as err:
        logger.error(f"Kafka consumer error: {err}")
    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup_event():
    """Startup event for the FastAPI app."""
    global consumer_task
    logger.info("Starting Kafka consumer...")
    consumer_task = asyncio.create_task(consume())


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event for the FastAPI app."""
    global consumer_task
    if consumer_task:
        consumer_task.cancel()
    await shutdown_producer()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"status": "Spiderweb service running"}


@app.post("/start")
async def start_game():
    """Start the game."""
    try:
        spidey_order = spidey_random(SPIDEY_NAMES)
        await send_one(SPIDERWEB_TOPIC, spidey_order)
        return {"order": spidey_order}
    except ValueError as ve:
        logger.error(ve)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error starting game: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
