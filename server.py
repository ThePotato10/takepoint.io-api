from flask import Flask, jsonify, send_file
from scraper import get_stats

app = Flask(__name__)

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/stats/<user>")
def stats(user):
    try:
        return jsonify(get_stats(user))
    except(IndexError):
        return jsonify({"error": "User doesn't exist"})

if __name__ == "__main__":
    app.run(port=5500, debug=True)
