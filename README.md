# fastapi-kafka
A demo project on application of Fastapi with Kafka

#### Procedure to run the project
Docker commands to run the project
```bash
docker-compose up -d build
docker-compose logs -f
```
Sql terminal commands to check the services
```bash
docker exec -it postgres_db psql -U postgres_user -d postgres_db -c "\l"
docker exec -it redis_stack redis-cli ping
```
alembic migration commands
```bash
alembic init -t async migrations
# add base.metadata and db_url in env.py
alembic revision --autogenerate -m 'adds user and post tables'
alembic upgrade head
```
check if tables are created
```bash
docker exec -it postgres_db psql -U postgres_user -d postgres_db -c "\dt"
docker exec -it postgres_db psql -U postgres_user -d postgres_db -c "\dt *"
```
Kafka commands to check the services
```bash
# get into the kafka container
docker exec -it kafka /bin/bash
# create a topic
kafka-topics --create --topic test.events --bootstrap-server kafka:29092 --partitions 4 --replication-factor 1
# check the topic
kafka-topics --describe --topic test.events --bootstrap-server kafka:29092
# produce and consume messages
kafka-console-producer --bootstrap-server kafka:29092 --topic test.events # enter some messages and exit
kafka-console-consumer --bootstrap-server kafka:29092 --topic test.events --from-beginning # check the messages
``` 

