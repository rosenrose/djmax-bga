import os
import re
import json
import subprocess
from random import random
from yt_dlp import YoutubeDL
from flask import Flask, Response, make_response, request
from static_ffmpeg import run

ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()

app = Flask(__name__)
port = int(os.environ.get("PORT") or 5000)

# try:
#     with YoutubeDL({"simulate": True, "cookiesfrombrowser": ("chrome", )}) as ydl:
#         result = ydl.extract_info(f"https://www.youtube.com/watch?v=vQ_ibsHzmxk")
# except Exception as e:
#     print(e)

def get_info(id):
    result = {}

    if re.match(r"[0-9a-zA-Z_\-]{11}", id):
        with YoutubeDL({"simulate": True, "sleep_interval": 1}) as ydl:
            result = ydl.extract_info(f"https://www.youtube.com/watch?v={id}")
    return result

def get_url(info):
    src = {"video": None, "audio": None}

    if "requested_formats" in info:
        for format in info["requested_formats"]:
            if format["vcodec"] != "none":
                src["video"] = format["url"]
            elif format["acodec"] != "none":
                src["audio"] = format["url"]
    return src

def create_response(message, heads={}):
    if type(message) is str:
        response = Response(message)
    else:
        response = make_response(message)

    response.headers["Access-Control-Allow-Origin"] = "*"
    for key in heads:
        response.headers[key] = heads[key]
    return response

@app.route('/')
def index():
    return create_response(f"<h1>Test port: {port}</h1>")

@app.route('/info/<id>')
def info(id):
    res = {}
    videoInfo = get_info(id)

    if "part" in request.args:
        parts = request.args["part"].split(",")
        for part in parts:
            if part == "url":
                res |= get_url(videoInfo)
            else:
                res[part] = videoInfo[part]
        return create_response(json.dumps(res))
    return create_response(json.dumps(videoInfo))

@app.route('/frame/<id>')
def frame(id):
    # params = list(request.args.items())
    print(id, "request")

    if "static" in request.args:
        duration = int(request.args["duration"])
        videoUrl = f"https://d2l1b145ht03q6.cloudfront.net/djmax/bga/{id}"
    else:
        info = get_info(id)
        duration = int(info["duration"])
        videoUrl = get_url(info)["video"]
        print(id, "extract")
        if not videoUrl:
            return create_response("no video")

    ss = min(request.args.get("ss", round(random() * duration, 1), type=float), duration)
    p = subprocess.run([
        ffmpeg,
        "-ss", str(ss),
        "-i", videoUrl,
        "-frames", "1",
        # "-s", "1920x1080",
        "-q:v", "5",
        "-f", "image2",
        "-vcodec", "mjpeg",
        "pipe:1"
        ], capture_output=True)
    output = p.stdout
    # print(output)
    # open("a.png", "wb").write(output)
    return create_response(output, heads={"Content-Type": "image/jpeg"})

if __name__ == "__main__":
    app.run(port=port)