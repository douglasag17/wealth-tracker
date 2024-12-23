# wealth-tracker backend

[Docker image FastAPI](https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi)

```shell
cd backend

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

fastapi dev main.py --port 8000

pytest

deactivate
```

or with Docker

```shell
cd backend

docker compose watch

docker compose down
```

Go to: http://127.0.0.1:8000/docs. You should see something like this:

![FastAPI Swagger UI](../docs/images/fastapi-swagger-ui.png)


### TODO:
- [ ] Dockerize FastAPI + Database
- [ ] [How to Set Relationship Cascade Options in SQLModel](https://jacob-t-graham.com/2024/05/23/how-to-set-relationship-cascade-options-in-sqlmodel/)
