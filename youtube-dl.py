import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
   return "<h1>Test</h1>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT") or 5000)
    app.run(port=port)