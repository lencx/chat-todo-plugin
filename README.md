# chat-todo-plugin

> ChatGPT Plugin for managing a TODO list

- [ChatGPT plugins](https://openai.com/blog/chatgpt-plugins)
- [ChatGPT plugins Doc](https://platform.openai.com/docs/plugins/introduction)

## Usage

```bash
# install dependencies
poetry install

# run the service
poetry run python main.py
```

## TODO API

### all list

```bash
curl -X GET http://0.0.0.0:5002/todos \
 -H 'Content-Type: application/json' \
 -H 'Authorization: Bearer $SERVICE_AUTH_KEY'
```

### specific user

```bash
curl -X GET http://0.0.0.0:5002/todos/lencx \
 -H 'Content-Type: application/json' \
 -H 'Authorization: Bearer $SERVICE_AUTH_KEY'
```

### specific user: add

```bash
curl -X POST http://0.0.0.0:5002/todos/lencx \
 -H 'Content-Type: application/json' \
 -H 'Authorization: Bearer $SERVICE_AUTH_KEY' \
 -d '{ "todo": "hello" }'
```

### specific user: delete

```bash
curl -X DELETE http://0.0.0.0:5002/todos/lencx \
 -H 'Content-Type: application/json' \
 -H 'Authorization: Bearer $SERVICE_AUTH_KEY' \
 -d '{ "todo_idx": 0 }'
```
