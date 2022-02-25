import os
import re
import json
import subprocess
from yt_dlp import YoutubeDL
from flask import Flask, Response, make_response, request
from static_ffmpeg import run

ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()

app = Flask(__name__)
port = int(os.environ.get("PORT") or 5000)

def get_info(id):
    result = {}

    if re.match(r"[0-9a-zA-Z_\-]{11}", id):
        with YoutubeDL({"simulate": True}) as ydl:
            result = ydl.extract_info(f"https://youtu.be/{id}")

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
    vidoeInfo = get_info(id)

    if "part" in request.args:
        parts = request.args["part"].split(",")
        for part in parts:
            if part == "url":
                res |= get_url(vidoeInfo)
            else:
                res[part] = vidoeInfo[part]

        return create_response(json.dumps(res))

    return create_response(json.dumps(vidoeInfo))    

@app.route('/frame/<id>')
def frame(id):
    # params = list(request.args.items())
    info = get_info(id)
    duration = float(info["duration"])
    videoUrl = get_url(info)["video"]
    print(videoUrl, duration)
    if not videoUrl:
        return create_response("no video")

    ss = min(float(request.args["ss"]), duration) if "ss" in request.args else 0
    p = subprocess.run([
        ffmpeg,
        "-ss", str(ss),
        "-i", videoUrl,
        "-frames", "1",
        # "-s", "1920x1080",
        "-f", "image2",
        "-vcodec", "png",
        "pipe:1"
        ], capture_output=True)
    output = p.stdout
    # print(output)
    # open("a.png", "wb").write(output)
    return create_response(output, {"Content-Type": "image/png"})

if __name__ == "__main__":
    app.run(port=port)