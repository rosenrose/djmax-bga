import os
from flask import Flask, Response

app = Flask(__name__)
port = int(os.environ.get("PORT") or 5000)

@app.route('/')
def index():
    response = Response(f"<h1>Test port: {port}</h1>")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == '__main__':
    app.run(port=port)