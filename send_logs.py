import requests

LOG_FILE = "/home/pi/forenscope/logs/forenscope_log.txt"
SERVER_URL = "http://192.168.52.221:5000/upload"  # Replace this

def send_log():
    with open(LOG_FILE, "r") as file:
        data = file.read()
    
    try:
        response = requests.post(SERVER_URL, data=data)
        print("✅ Log sent successfully:", response.status_code)
    except Exception as e:
        print("❌ Failed to send log:", str(e))

if __name__ == "__main__":
    send_log()
