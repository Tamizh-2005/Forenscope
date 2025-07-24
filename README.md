#Forenscope – Portable Digital Forensics Kit 🕵️‍♂️🧪

Forenscope is a portable, Raspberry Pi-based forensic toolkit designed for digital evidence extraction in the field. It supports forensic imaging, mobile data extraction, IoT sensor capture, and camera snapshot acquisition — all from a single device.

It also performs hidden file detection, hash verification, pattern-based metadata analysis, and generates structured forensic reports. Logs can be sent to a centralized dashboard for investigation team review.

---

## 🚀 Features

* 🔌 USB pendrive imaging with SHA256 hash verification
* 📱 Android phone data extraction via ADB (with hidden/deleted file detection)
* 📸 CCTV/IP camera snapshot capture via HTTP
* 🌐 IoT sensor data collection via serial interface
* 🧠 Pattern-based metadata analysis using ExifTool
* 🧾 Structured report generation with risk evaluation
* 🖥 Flask-based dashboard support (log upload & display)
* 🛡 Designed for field use by forensic teams or law enforcement

---

## 🔧 Components Used

| Component            | Description                                  |
| -------------------- | -------------------------------------------- |
| Raspberry Pi 4       | Main controller (32-bit OS used)             |
| USB Pendrive (32 GB) | For OS boot and temporary image storage      |
| Power Bank           | Portable power source                        |
| Breadboard & Cables  | Optional for GPIO/IOT sensor integration     |
| Android Phone        | Target for mobile data extraction (with ADB) |
| IoT Sensor           | Any device with serial output (e.g. UART)    |
| CCTV Camera          | Must support HTTP image snapshot             |

---

## 📁 Folder Structure

| Folder         | Purpose                              |
| -------------- | ------------------------------------ |
| /images/       | Stores disk images of USB devices    |
| /logs/         | Logs, hash outputs, and session tags |
| /metadata/     | Extracted metadata using ExifTool    |
| /reports/      | Final forensic report files          |
| /mobile\_data/ | Extracted Android data               |
| /iot/          | IoT sensor serial logs               |
| /camera/       | CCTV snapshot images                 |

---

## ⚙️ Installation

1. Flash Raspberry Pi OS (32-bit) to a USB pendrive or SD card.
2. Enable SSH & Wi-Fi:

   * Create a file named ssh (no extension) in /boot
   * Add a wpa\_supplicant.conf file with your Wi-Fi config
3. Connect Raspberry Pi via SSH or monitor.
4. Install dependencies:

   ```bash
   sudo apt update && sudo apt install -y exiftool adb dcfldd python3-pip
   pip3 install flask
   ```
5. Clone this repo:

   ```bash
   git clone https://github.com/your-username/forenscope.git
   cd forenscope
   ```

---

## 💻 Usage

1. Launch the forensic tool:

   ```bash
   python3 forenscope.py
   ```
2. Enter:

   * Case ID
   * Investigator name
   * Select the device type:

     * USB Pendrive
     * Android Phone
     * CCTV Camera
     * IoT Sensor
3. Tool performs extraction + metadata + hash + hidden file scan
4. Report saved to /reports/, logs in /logs/

📍 USB imaging uses dcfldd
📍 Android uses adb pull and detects hidden/deleted-like files
📍 IP camera requires snapshot URL
📍 IoT sensor reads from serial port (e.g. /dev/ttyUSB0)

---

## 📊 Forensic Report

Each report includes:

* 🔐 SHA256 hash (from imaging)
* 🕵️ Metadata summary
* 👁️ Hidden files detected
* 🗑️ Simulated deleted file patterns
* 📅 Timestamps of extraction
* ⚠ Risk level (Low/Medium/High)

Saved at:
📁 /home/pi/forenscope/reports/

---

## 📡 Flask Dashboard (Optional Feature)

To send logs to a remote dashboard:

1. On your investigator laptop:

   * Run the Flask dashboard (example: flask\_dashboard.py)
2. On Raspberry Pi:

   * Set SERVER\_URL in send\_logs.py to your laptop IP
3. Use:

   ```bash
   python3 send_logs.py
   ```

Logs will be sent and saved in the host dashboard folder.

---

## 📦 Future Enhancements

* PDF or HTML report generation
* Remote device connection detection
* GUI interface on Pi
* Real deleted file recovery (if rooted device)
* Pi camera integration for photo evidence

---

## 🔒 Legal Disclaimer

This project is intended strictly for academic, forensic, and lawful investigative use. Unauthorized or unethical use is prohibited.

Always ensure consent or a valid legal warrant is obtained when using Forenscope on external devices.

---

## 👨‍💻 Contributors

* Investigator & Developer: Your Name
* Advisor: \[Professor or Guide Name]

---

🧠 Project Type: Final Year Project (B.E/B.Tech CSE, Cybersecurity Track)

📍 Location: On-field investigation tool for quick digital triage

📌 Upload screenshots, flow diagrams, and sample reports in the /docs folder (optional for GitHub)

—

Would you like me to create a ZIP of this README.md and any other file so you can download it directly? Or generate sample report/log/metadata files for testing your GitHub repo?
