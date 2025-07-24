import os
import subprocess
from datetime import datetime
from generate_report import generate_report
from analyze_metadata import analyze_metadata

LOG_FILE = "logs/forenscope_log.txt"
IMAGE_PATH = "images/usb_evidence.img"
HASH_FILE = "logs/hash.txt"
METADATA_FILE = "metadata/metadata.txt"

def log(msg):
    time = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{time} {msg}\n")
    print(f"{time} {msg}")

def scan_hidden_files(path):
    hidden = []
    for root, dirs, files in os.walk(path):
        for name in files + dirs:
            if name.startswith("."):
                hidden.append(os.path.join(root, name))
    return hidden

def simulate_deleted_file_detection(path):
    matches = []
    keywords = ["deleted", "trash", "tmp", "temp", "recover", "bak"]
    for root, _, files in os.walk(path):
        for f in files:
            if any(k in f.lower() for k in keywords):
                matches.append(os.path.join(root, f))
    return matches

def extract_metadata(case_id, investigator):
    log("Extracting metadata from USB image...")
    os.system(f"exiftool {IMAGE_PATH} > {METADATA_FILE}")
    with open("logs/session_tag.txt", "w") as f:
        f.write(f"Device Type: USB\nExtraction Time: {datetime.now()}\n")
    log("Metadata extraction completed.")
    generate_report("USB", case_id, investigator)

def extract_mobile(case_id, investigator):
    log("Starting Android extraction...")
    os.system("adb devices")
    pull_path = input("Enter Android path (e.g., /sdcard/DCIM): ").strip()
    extract_path = "mobile_data/"
    os.system(f"adb pull {pull_path} {extract_path}")
    os.system("adb shell getprop > mobile_data/device_info.txt")

    hidden = scan_hidden_files(extract_path)
    deleted = simulate_deleted_file_detection(extract_path)

    with open("logs/session_tag.txt", "w") as f:
        f.write(f"Device Type: ANDROID\nExtraction Time: {datetime.now()}\n")

    generate_report("ANDROID", case_id, investigator, len(hidden), len(deleted))

def extract_camera(case_id, investigator):
    url = input("Enter camera snapshot URL: ")
    os.system(f"wget -O camera/snapshot.jpg {url}")
    with open("logs/session_tag.txt", "w") as f:
        f.write(f"Device Type: CAMERA\nExtraction Time: {datetime.now()}\n")
    generate_report("CAMERA", case_id, investigator)

def extract_iot(case_id, investigator):
    port = input("Enter serial port (e.g. /dev/ttyUSB0): ")
    os.system(f"timeout 10s cat {port} > iot/sensor_log.txt")
    with open("logs/session_tag.txt", "w") as f:
        f.write(f"Device Type: IOT\nExtraction Time: {datetime.now()}\n")
    generate_report("IOT", case_id, investigator)

def main():
    case_id = input("Enter Case ID: ")
    investigator = input("Enter Investigator Name: ")

    print("1. USB")
    print("2. Android Phone")
    print("3. CCTV Camera")
    print("4. IoT Sensor")
    choice = input("Choose option: ").strip()

    if choice == "1":
        device = input("Enter device (e.g., sda): ")
        os.system(f"sudo dcfldd if=/dev/{device} of={IMAGE_PATH} hash=sha256 hashlog={HASH_FILE}")
        extract_metadata(case_id, investigator)
    elif choice == "2":
        extract_mobile(case_id, investigator)
    elif choice == "3":
        extract_camera(case_id, investigator)
    elif choice == "4":
        extract_iot(case_id, investigator)
    else:
        print("Invalid option.")
        return

    log("=== Forensic session complete ===")

if __name__ == "__main__":
    main()
