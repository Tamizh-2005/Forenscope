import requests

LOG_FILE = "logs/forenscope_log.txt"
SERVER_URL = "http://<YOUR_IP>:5000/upload"  # replace with actual Flask server

def send_log():
    with open(LOG_FILE, "r") as file:
        data = file.read()
    try:
        response = requests.post(SERVER_URL, data=data)
        print("✅ Log sent:", response.status_code)
    except Exception as e:
        print("❌ Error sending log:", str(e))

if __name__ == "__main__":
    send_log()
