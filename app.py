import os
from flask import Flask, jsonify

app = Flask(__name__)

MESSAGE = "Hello! Version 1 - deployed with CI/CD"   # change this and push to show an update


@app.get("/")
def home():
    return f"<h1>{MESSAGE}</h1><p>Commit: {os.getenv('GIT_SHA', 'local')}</p>"


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/info")
def info():
    return jsonify(message=MESSAGE, commit=os.getenv("GIT_SHA", "local"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
