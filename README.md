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
