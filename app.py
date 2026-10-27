import os

from flask import Flask, jsonify, render_template, request

# 예약 규칙은 웹에 따로 만들지 않고 solution.py의 RoomBooking을 그대로 불러 쓴다.
from solution import RoomBooking

app = Flask(__name__)

# 서버가 켜져 있는 동안 예약을 기억하는 하나의 RoomBooking
rb = RoomBooking()


@app.after_request
def add_cors(resp):
    # GitHub Pages(다른 주소)에서 이 서버의 API를 부를 수 있게 허용
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp


@app.route("/api/<path:_p>", methods=["OPTIONS"])
def api_options(_p):
    return ("", 204)


def _body():
    return request.get_json(silent=True) or {}


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/book")
def api_book():
    d = _body()
    ok = rb.book(d.get("room"), d.get("day"), d.get("start"), d.get("end"), d.get("name"))
    return jsonify(ok=ok)


@app.post("/api/cancel")
def api_cancel():
    d = _body()
    ok = rb.cancel(d.get("room"), d.get("day"), d.get("start"), d.get("name"))
    return jsonify(ok=ok)


@app.get("/api/schedule")
def api_schedule():
    items = rb.get_schedule(request.args.get("room"), request.args.get("day"))
    return jsonify(items=[list(x) for x in items])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
