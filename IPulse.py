from flask import Flask, render_template, request, jsonify
from pyngrok import ngrok, conf
from colorama import Fore, Style, init
import os, json, sys, atexit, signal
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Initialize colorama
init(autoreset=True)

app = Flask(__name__)

# Paths
IP_DIR = 'ip'
CONFIG_DIR = 'config'
IP_FILE = os.path.join(IP_DIR, 'data.txt')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'ngrok_config.json')

for folder in [IP_DIR, CONFIG_DIR]:
    os.makedirs(folder, exist_ok=True)

executor = ThreadPoolExecutor(max_workers=10)
ngrok_tunnel = None
ngrok_url = None

def save_ngrok_config(token):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'auth_token': token, 'saved_at': datetime.now().isoformat()}, f, indent=2)

def load_ngrok_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f).get('auth_token')
    return None

def setup_ngrok(token):
    try:
        conf.get_default().auth_token = token
        return True
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to configure ngrok: {e}")
        return False

def start_ngrok():
    global ngrok_tunnel, ngrok_url
    try:
        ngrok_tunnel = ngrok.connect(5000, bind_tls=True)
        ngrok_url = ngrok_tunnel.public_url
        print(Fore.GREEN + f"[INFO] Ngrok tunnel started: {ngrok_url}")
        return ngrok_url
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to start ngrok tunnel: {e}")
        return None

def stop_ngrok():
    if ngrok_tunnel:
        print(Fore.YELLOW + "[INFO] Stopping ngrok tunnel...")
        ngrok.disconnect(ngrok_tunnel.public_url)
        ngrok.kill()

def log_ip(ip, user_agent=None, method=None):
    try:
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"{ts} - {ip}"
        if method:
            entry += f" ({method})"
        if user_agent:
            entry += f" - {user_agent[:80]}"
        with open(IP_FILE, 'a') as f:
            f.write(entry + "\n")
        print(Fore.BLUE + f"[LOG] {entry}")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to log IP: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save-ip', methods=['POST'])
def save_ip():
    try:
        data = request.get_json()
        if not data or 'ip' not in data:
            return jsonify({'error': 'No IP provided'}), 400
        executor.submit(log_ip, data['ip'], request.headers.get('User-Agent'), 'client')
        return jsonify({'status': 'success'})
    except Exception as e:
        print(Fore.RED + f"[ERROR] /save-ip failed: {e}")
        return jsonify({'error': 'Server error'}), 500

@app.route('/status')
def status():
    return jsonify({
        'public_url': ngrok_url,
        'local': 'http://localhost:5000',
        'status': 'running'
    })

@app.after_request
def secure_headers(resp):
    resp.headers['X-Frame-Options'] = 'DENY'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['X-XSS-Protection'] = '1; mode=block'
    return resp

def cleanup():
    stop_ngrok()
    executor.shutdown(wait=False)

def signal_handler(sig, frame):
    print(Fore.RED + "\n[SHUTDOWN] Interrupted. Cleaning up...")
    cleanup()
    sys.exit(0)

def main():
    global ngrok_url
    print(Fore.CYAN + Style.BRIGHT + "\nFlask IP Logger with pyngrok")
    print(Fore.MAGENTA + "=" * 60)

    atexit.register(cleanup)
    signal.signal(signal.SIGINT, signal_handler)

    token = load_ngrok_config()
    if not token:
        print(Fore.YELLOW + "[WARNING] Ngrok auth token not found.")
        print("Get your token from: https://dashboard.ngrok.com/get-started/your-authtoken")
        token = input(Fore.CYAN + "Enter your ngrok auth token: ").strip()
        if not token:
            print(Fore.RED + "[ERROR] No token provided. Exiting.")
            sys.exit(1)
        if setup_ngrok(token):
            save_ngrok_config(token)
            print(Fore.GREEN + "[INFO] Ngrok token saved.")
    else:
        if not setup_ngrok(token):
            print(Fore.RED + "[ERROR] Invalid token in config.")
            sys.exit(1)
        print(Fore.GREEN + "[INFO] Ngrok token loaded from config.")

    ngrok_url = start_ngrok()
    if not ngrok_url:
        sys.exit(1)

    if os.path.exists(IP_FILE):
        with open(IP_FILE) as f:
            print(Fore.LIGHTWHITE_EX + f"Previous IP logs: {len(f.readlines())}")

    print(Fore.YELLOW + f"Public URL: {ngrok_url}")
    print(Fore.CYAN + f"Local URL:  http://localhost:5000")
    print(Fore.GREEN + Style.BRIGHT + "Server is running. Press Ctrl+C to stop.")
    print(Fore.MAGENTA + "=" * 60)

    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    main()
