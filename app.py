from flask import Flask, render_template, request, jsonify, redirect
from detector import detect_scam

app = Flask(__name__)


@app.route("/")
def home():
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json()
    message = data.get("message", "")

    if not message.strip():
        return jsonify({
            "error": "Please enter a message."
        }), 400

    result = detect_scam(message)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)