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