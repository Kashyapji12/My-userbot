from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "🔥 Userbot Dashboard Running"

@app.route("/status")
def status():
    return {"status":"online"}

app.run(port=5000)