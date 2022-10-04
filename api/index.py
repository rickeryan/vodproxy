from flask import Flask, request, Response, abort
from flask_cors import CORS
import requests

app = Flask(__name__)
# cors config
CORS(app)


@app.route('/')
def index():
    # get source url from query param url
    url = request.args.get("url")
    if url is None:
        abort(404)
    # use $ replace & in source ul,replace before using
    url = url.replace("$", "&")
    # get source host for redirect header
    host = url.replace("https://", "")
    host = host.replace("http://", "")
    host = host[0:host.index("/")]
    # user agent for redirect
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47"
    headers = {"Host": host, "User-Agent": user_agent}
    # get data from source
    res = requests.get(url, headers=headers)
    # return data
    if res.status_code == 200:
        # transfer_res = Response(res.content,
        #                         mimetype=res.headers["content-type"])
        transfer_res = Response(res.content, mimetype="Application/json")
        return transfer_res
    # return 404
    abort(404)
