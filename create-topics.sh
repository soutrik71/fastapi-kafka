#!/bin/bash

# List of topics to create
TOPICS="topic_A_to_B topic_B_to_C topic_C_to_D"

# Kafka binary location in the container
KAFKA_BIN_DIR="/opt/kafka/bin"

# Kafka bootstrap server
BOOTSTRAP_SERVER="localhost:29092"

# Loop through topics
for topic in $TOPICS; do
    echo "Creating topic: $topic"
    ${KAFKA_BIN_DIR}/kafka-topics.sh --create \
        --bootstrap-server ${BOOTSTRAP_SERVER} \
        --replication-factor 1 \
        --partitions 1 \
        --topic $topic
done

echo "Verifying topics..."
${KAFKA_BIN_DIR}/kafka-topics.sh --bootstrap-server ${BOOTSTRAP_SERVER} --list

echo "All topics created and verified successfully."
