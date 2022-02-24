import os
import re
import json
import random
import subprocess
# from yt_dlp import YoutubeDL
# from flask import Flask, Response, make_response
from static_ffmpeg import run

ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()
print(dir(ffmpeg))

# app = Flask(__name__)
# port = int(os.environ.get("PORT") or 5000)

# def get_info(id):
#     result = {}

#     if re.match(r"[0-9a-zA-Z_\-]{11}", id):
#         with YoutubeDL({"simulate": True}) as ydl:
#             result = ydl.extract_info(f"https://youtu.be/{id}")

#     return result

# def get_url(info):
#     src = {"video": None, "audio": None}

#     if "requested_formats" in info:
#         for format in info["requested_formats"]:
#             if format["vcodec"] != "none":
#                 src["video"] = format["url"]
#             elif format["acodec"] != "none":
#                 src["audio"] = format["url"]

#     return src

# @app.route('/')
# def index():
#     response = Response(f"<h1>Test port: {port}</h1>")
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     return response

# @app.route('/url/<id>')
# def url(id):
#     response = Response(json.dumps(get_url(get_info(id))))
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     return response

# @app.route('/frame/<id>')
# def frame(id):
#     info = get_info(id)
#     duration = info["duration"]
#     videoUrl = get_url(info)["video"]

#     if not videoUrl:
#         response = Response("no video")
#         response.headers["Access-Control-Allow-Origin"] = "*"
#         return response

#     p = subprocess.run([], capture_output=True)
#     out, err = (
#         ffmpeg
#         .input(videoUrl, ss=random.randrange(duration))
#         .output("pipe:", format="image2", vcodec="png", frames=1, s="1920x1080")
#         .run(capture_stdout=True)
#     )
#     # print(type(out))
#     # open("a.png", "wb").write(out)
#     response = make_response(out)
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     response.headers["Content-Type"] = "image/png"
#     return response

# if __name__ == "__main__":
#     app.run(port=port)