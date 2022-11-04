# Todo App

### Create environment variables:

Rename sample.env to .env

```
mv sample.env .env
```

### Run docker compose

```
docker-compose up --build
```

## Login API:

```
POST: localhost:9090/api/v1/login/
{
    "email": <email>,
    "password": <password>
}

Response: {
    "token": <user_token>
}
```

## Task API:

get task

```
GET: localhost:9090/api/v1/task/?task_id=e20781b0-b954-4bf6-a5b0-7bcf55428fb7
{
    "title": "Do this",
    "description": "hello",
    "priority": false
}
Response: 
{
    "task_id": "e20781b0-b954-4bf6-a5b0-7bcf55428fb7",
    "title": "do that",
    "description": "hello",
    "priority": true,
    "status": "COMPLETE"
}
```

create tasks

```
POST: localhost:9090/api/v1/task/
{
    "title": "Do this",
    "description": "hello",
    "priority": false
}
Response: 
{
    "task_uid": "e20781b0-b954-4bf6-a5b0-7bcf55428fb7"
}
```

update tasks:

```
PUT: localhost:9090/api/v1/task/
{
    "task_id": "e20781b0-b954-4bf6-a5b0-7bcf55428fb7",
    "title": "do that",
    "priority": true,
    "status": "completed"
}
Response: 
{
    "task_id": "e20781b0-b954-4bf6-a5b0-7bcf55428fb7",
    "title": "do that",
    "description": "hello",
    "priority": true,
    "status": "COMPLETE"
}
```

delete tasks:

```
DELETE: localhost:9090/api/v1/task/
{
    "task_id": "e20781b0-b954-4bf6-a5b0-7bcf55428fb7",
}
Response: 
{
    "msg": "Successfully Deleted"
}
```
