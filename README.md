<p align="center">
  <img width="180" src="./logo.svg" alt="ChatGPT TODO List">
  <h1 align="center">chat-todo-plugin</h1>
  <p align="center">ChatGPT Plugin for managing a TODO list</p>
</p>

- [ChatGPT plugins](https://openai.com/blog/chatgpt-plugins)
- [ChatGPT plugins Doc](https://platform.openai.com/docs/plugins/introduction)
- [OpenAPI Specification](https://swagger.io/specification)

---

- [开发指南：ChatGPT 插件开发（上）](https://mp.weixin.qq.com/s/AmNkiLOqJo7tEJZPX34oeg)
- [开发指南：ChatGPT 插件开发（下）](https://mp.weixin.qq.com/s/8EE3y4hU5Rp0rCCDPBEL2w)

## Plugin development

```bash
[plugin-repo]
|- main.py
|- manifest.json
|- openapi.yaml
|- logo.png
`- ... # other
```

### manifest.json

[plugin-manifest](https://platform.openai.com/docs/plugins/getting-started/plugin-manifest): Every plugin requires a ai-plugin.json file, which needs to be hosted on the API’s domain.

```json
{
  "schema_version": "v1",
  "name_for_human": "TODO Plugin (service http)",
  "name_for_model": "todo",
  "description_for_human": "Plugin for managing a TODO list, you can add, remove and view your TODOs.",
  "description_for_model": "Plugin for managing a TODO list, you can add, remove and view your TODOs.",
  "auth": {
    "type": "service_http",
    "authorization_type": "bearer",
    "verification_tokens": {
      "openai": "<YOUR_OPENAI_KEY>"
    }
  },
  "api": {
    "type": "openapi",
    "url": "https://<YOUR_REPO>.<YOUR_OWNER>.repl.co/openapi.yaml",
    "is_user_authenticated": false
  },
  "logo_url": "https://<YOUR_REPO>.<YOUR_OWNER>.repl.co/logo.png",
  "contact_email": "<YOUR_EMAIL>",
  "legal_info_url": "http://www.example.com/legal"
}
```

- `<YOUR_OPENAI_KEY>`: your OpenAI API key
- `<YOUR_REPO>`: your replit app name
- `<YOUR_OWNER>`: your replit username
- `<YOUR_EMAIL>`: your email

### openapi.yaml

[openapi-definition](https://platform.openai.com/docs/plugins/getting-started/openapi-definition): OpenAPI specification to document the API. The model in ChatGPT does not know anything about your API other than what is defined in the OpenAPI specification and manifest file. This means that if you have an extensive API, you need not expose all functionality to the model and can choose specific endpoints.

```yaml
openapi: 3.0.1
info:
  title: TODO Plugin
  description: A plugin that allows the user to create and manage a TODO list using ChatGPT. If you do not know the user's username, ask them first before making queries to the plugin. Otherwise, use the username "global".
  version: 'v1'
servers:
  # product: http://www.example.com
  - url: http://localhost:5002
paths:
  /todos/{username}:
    get:
      operationId: getTodos
      summary: Get the list of todos
      parameters:
      - in: path
        name: username
        schema:
            type: string
        required: true
        description: The name of the user.
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/getTodosResponse'
# ...
```

### main.py

```py
import os
import quart
import quart_cors
from quart import Quart, jsonify, request

PORT = 5002
TODOS = {}
# Get authentication key from environment variable
SERVICE_AUTH_KEY = os.environ.get("SERVICE_AUTH_KEY")


# Create a Quart app and enable CORS
app = quart_cors.cors(
  Quart(__name__),
  allow_origin=[
    f"http://localhost:{PORT}",
    "https://chat.openai.com",
  ]
)


# Add a before_request hook to check for authorization header
@app.before_request
def assert_auth_header():
  auth_header = request.headers.get("Authorization")
  print(auth_header)
  # check if the header is missing or incorrect, and return an error if needed
  if not auth_header or auth_header != f"Bearer {SERVICE_AUTH_KEY}":
        return jsonify({"error": "Unauthorized"}), 401


# Add a route to get all todos
@app.route("/todos", methods=["GET"])
async def get_todos():
  return jsonify(TODOS)


# Add a route to get all todos for a specific user
@app.route("/todos/<string:username>", methods=["GET"])
async def get_todo_user(username):
    todos = TODOS.get(username, [])
    return jsonify(todos)


# Add a route to add a todo for a specific user
@app.route("/todos/<string:username>", methods=["POST"])
async def add_todo(username):
    request_data = await request.get_json()
    todo = request_data.get("todo", "")
    TODOS.setdefault(username, []).append(todo)
    return jsonify({"status": "success"})


# Add a route to delete a todo for a specific user
@app.route("/todos/<string:username>", methods=["DELETE"])
async def delete_todo(username):
    request_data = await request.get_json()
    todo_idx = request_data.get("todo_idx", -1)
    if 0 <= todo_idx < len(TODOS.get(username, [])):
        TODOS[username].pop(todo_idx)
    return jsonify({"status": "success"})


@app.get("/logo.png")
async def plugin_logo():
  filename = 'logo.png'
  return await quart.send_file(filename, mimetype='image/png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
  host = request.headers['Host']
  with open("manifest.json") as f:
    text = f.read()
    text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
    return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
  host = request.headers['Host']
  with open("openapi.yaml") as f:
    text = f.read()
    text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
    return quart.Response(text, mimetype="text/yaml")


def main():
  app.run(debug=True, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
  main()
```

## Plugin Deploy (Replit)

- Open [Replit](https://replit.com) and click the `Create Repl` button.
- When the pop-up window appears, click the `Import from GitHub` button in the top right corner.
- In the GitHub URL field, enter `https://github.com/lencx/chat-todo-plugin` and select `Python` as the language.
- Then click the `Import from GitHub` button in the bottom right corner and wait for the initialization to complete.
- Click the `Run` button and wait for the execution to finish.

<!-- ## Local Development

```bash
# install dependencies
poetry install

# run the service
poetry run python main.py
``` -->

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
