import os
from flask import Flask

app = Flask(__name__)
port = int(os.environ.get("PORT") or 5000)

@app.route('/')
def index():
   return f"<h1>Test port: {port}</h1>"

if __name__ == '__main__':
    app.run(port=port)