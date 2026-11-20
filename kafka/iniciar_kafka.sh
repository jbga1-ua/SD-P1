#!/bin/bash
# Uso: ./iniciar_kafka.sh [IP_ANUNCIADA]
# Sin argumento usa localhost (desarrollo en tu PC).
# En AWS se pasa la IP pública de la máquina.

HOST=${1:-localhost}
BIN=/opt/bitnami/kafka/bin
TOPICS="fo_a_central ws_a_central central_a_fo central_a_ws"

# Si el contenedor ya existe lo arranca; si no, lo crea
if docker ps -a --format '{{.Names}}' | grep -qx kafka; then
  docker start kafka
else
  docker run -d --name kafka --restart unless-stopped -p 9092:9092 \
    -e KAFKA_CFG_NODE_ID=0 \
    -e KAFKA_CFG_PROCESS_ROLES=controller,broker \
    -e KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
    -e KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
    -e KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@localhost:9093 \
    -e KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER \
    -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://$HOST:9092 \
    bitnamilegacy/kafka:3.7.0
fi

# Esperar a que Kafka responda
echo "Esperando a Kafka..."
until docker exec kafka $BIN/kafka-topics.sh --bootstrap-server localhost:9092 --list >/dev/null 2>&1; do
  sleep 2
done

# Crear los topics (si ya existen, no pasa nada)
for t in $TOPICS; do
  docker exec kafka $BIN/kafka-topics.sh --create --if-not-exists --topic $t --bootstrap-server localhost:9092
done

echo "Topics disponibles:"
docker exec kafka $BIN/kafka-topics.sh --list --bootstrap-server localhost:9092