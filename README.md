# 🌐 Flask Public IP Logger with pyngrok

A lightweight Flask application that logs the **public IP addresses** of users who visit your site. It uses `pyngrok` to securely expose the app to the internet — no need to download or configure the ngrok binary manually.

> ✅ For **ethical use only** — great for demonstrations, education, and research purposes.

---

## 🔧 Features

- 🔍 Logs **public IP addresses** (even behind NAT)
- 🌐 Uses **pyngrok** for secure WAN exposure
- 🕵️ Captures User-Agent and timestamp
- 📁 Saves logs to `ip/data.txt`
- 🎨 Clean CLI with colorized logs using `colorama`
- 🛡️ Basic security headers included

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ip-logger.git
cd ip-logger
2. Install Dependencies
bash
Copy
Edit
pip install flask pyngrok colorama
3. Run the App
bash
Copy
Edit
python app.py
🔑 You'll be asked for your ngrok auth token if it's not already saved.
Get it from your ngrok dashboard

🗂️ Project Structure
bash
Copy
Edit
.
├── app.py                 # Main Flask app
├── ip/
│   └── data.txt           # Logged IPs
├── config/
│   └── ngrok_config.json  # Stores ngrok auth token
├── templates/
│   └── index.html         # Simple frontend (optional)
└── README.md              # This file
📋 API Endpoints
GET / — Main page

POST /save-ip — Accepts { ip: "x.x.x.x" } and logs it

GET /status — Shows current ngrok and local URLs

🛡️ Disclaimer
This tool is provided for educational and lawful purposes only.

Do not use it without consent from users. Respect privacy laws like GDPR and CCPA.

📜 License
MIT License
```

## 💰 Donations

Support the project with Bitcoin donations:

```bash
bc1qlpw590fkykfdd9v92g9snfmx8hc8vwxvkz5npm
```

## Contact / Issues

For help or issues, please open an issue on GitHub or contact the maintainer.

---

Thank you for using this tool responsibly!

```
