import os
from yt_dlp import YoutubeDL
from flask import Flask, Response

app = Flask(__name__)
port = int(os.environ.get("PORT") or 5000)

@app.route('/')
def index():
    response = Response(f"<h1>Test port: {port}</h1>")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/<id>')
def video_url(id):
    video_src = ""
    with YoutubeDL({"simulate": True}) as ydl:
        info = ydl.extract_info(f"https://youtu.be/{id}")
        for format in info["requested_formats"]:
            if format["vcodec"] != "none":
                video_src = format["url"]
                break
    response = Response(video_src)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == "__main__":
    app.run(port=port)