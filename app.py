from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>🚀 Мой первый DevOps проект!</h1><p>Версия 2.0</p>"


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
