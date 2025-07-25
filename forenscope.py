# === forenscope.py ===
import os
import subprocess
from datetime import datetime
from generate_report import generate_report

# Paths
LOG_FILE = "/home/pi/forenscope2/forenscope/logs/forenscope_log.txt"
IMAGE_PATH = "/home/pi/forenscope2/forenscope/images/usb_evidence.img"
HASH_FILE = "/home/pi/forenscope2/forenscope/logs/hash.txt"
METADATA_FILE = "/home/pi/forenscope2/forenscope/metadata/metadata.txt"


def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")


def scan_hidden_files(extract_path):
    hidden_items = []
    for root, dirs, files in os.walk(extract_path):
        for name in files + dirs:
            if name.startswith("."):
                full_path = os.path.join(root, name)
                hidden_items.append(full_path)
    return hidden_items


def simulate_deleted_file_detection(extract_path):
    simulated_deleted = []
    keywords = ["recover", "deleted", "trash", "tmp", "temp", "old", "bak", "backup"]
    for root, dirs, files in os.walk(extract_path):
        for name in files:
            if any(keyword in name.lower() for keyword in keywords):
                simulated_deleted.append(os.path.join(root, name))
    return simulated_deleted


def list_devices():
    print("\n🔍 Detecting connected storage devices...\n")
    result = subprocess.run(["lsblk", "-o", "NAME,SIZE,TYPE,MOUNTPOINT"], capture_output=True, text=True)
    print(result.stdout)


def get_user_device():
    list_devices()
    device = input("Enter the device name to image (e.g., sda, sdb): ").strip()
    return f"/dev/{device}"


def image_device(device_path):
    log(f"Starting forensic imaging of {device_path}")
    cmd = f"sudo dcfldd if={device_path} of={IMAGE_PATH} hash=sha256 hashlog={HASH_FILE} status=on"
    os.system(cmd)
    log("Imaging completed.")


def extract_metadata(case_id, investigator):
    log("Extracting metadata from image...")
    cmd = f"exiftool {IMAGE_PATH} > {METADATA_FILE}"
    os.system(cmd)
    with open("/home/pi/forenscope2/forenscope/logs/session_tag.txt", "w") as f:
        f.write("Device Type: USB\n")
        f.write("Extraction Time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log("Metadata extraction completed.")
    generate_report("USB", case_id, investigator)


def extract_mobile(case_id, investigator):
    log("Starting Android extraction...")
    print("Make sure USB debugging is enabled on the phone.")
    os.system("adb devices")
    pull_path = input("Enter Android folder path to pull (e.g. /sdcard/DCIM): ").strip()
    extract_path = "/home/pi/forenscope2/forenscope/mobile_data/"
    os.system(f"adb pull {pull_path} {extract_path}")
    log("ADB pull completed.")
    os.system("adb shell getprop > /home/pi/forenscope2/forenscope/mobile_data/device_info.txt")
    log("Android device info captured.")

    hidden_files = scan_hidden_files(extract_path)
    deleted_like_files = simulate_deleted_file_detection(extract_path)

    if hidden_files:
        log(f"{len(hidden_files)} hidden files/folders found.")
    else:
        log("No hidden files found.")

    if deleted_like_files:
        log(f"{len(deleted_like_files)} deleted-looking files found.")
    else:
        log("No deleted-looking files found.")

    with open("/home/pi/forenscope2/forenscope/logs/session_tag.txt", "w") as f:
        f.write("Device Type: Android\n")
        f.write("Extraction Time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    generate_report("ANDROID", case_id, investigator, hidden_count=len(hidden_files), deleted_like_count=len(deleted_like_files))


def extract_camera(case_id, investigator):
    log("Starting camera extraction...")
    url = input("Enter snapshot URL (e.g. http://192.168.1.100/image.jpg): ").strip()
    os.system(f"wget -O /home/pi/forenscope2/forenscope/camera/snapshot.jpg {url}")
    log(f"Snapshot saved from {url}")
    with open("/home/pi/forenscope2/forenscope/logs/session_tag.txt", "w") as f:
        f.write("Device Type: Camera\n")
        f.write("Extraction Time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    generate_report("CAMERA", case_id, investigator)


def extract_iot(case_id, investigator):
    log("Starting IoT sensor serial extraction...")
    port = input("Enter serial port (e.g. /dev/ttyUSB0): ").strip()
    os.system(f"timeout 10s cat {port} > /home/pi/forenscope2/forenscope/iot/sensor_log.txt")
    log("Sensor data captured.")
    with open("/home/pi/forenscope/logs/session_tag.txt", "w") as f:
        f.write("Device Type: IOT\n")
        f.write("Extraction Time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    generate_report("IOT", case_id, investigator)


def main():
    log("=== Forenscope Forensic Session Started ===")
    case_id = input("Enter Case ID: ")
    investigator = input("Enter Investigator Name: ")
    print("\nSelect the device to extract from:")
    print("1. USB Pendrive")
    print("2. Mobile Phone (Android)")
    print("3. CCTV / IP Camera")
    print("4. IoT Sensor (Serial/Log)")
    choice = input("Enter option [1-4]: ").strip()

    if choice == "1":
        device_path = get_user_device()
        image_device(device_path)
        extract_metadata(case_id, investigator)
    elif choice == "2":
        extract_mobile(case_id, investigator)
    elif choice == "3":
        extract_camera(case_id, investigator)
    elif choice == "4":
        extract_iot(case_id, investigator)
    else:
        print("❌ Invalid option. Exiting.")
        return

    log("=== Session Completed ===")

if __name__ == "__main__":
    main()
