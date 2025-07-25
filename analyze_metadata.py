# === analyze_metadata.py ===
import os
from datetime import datetime, timedelta

def analyze_metadata(meta_file):
    report_lines = []
    suspicious_files = []
    recent_files = []
    hidden_files = []

    if not os.path.exists(meta_file):
        return ["No metadata file found."]

    with open(meta_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        lower_line = line.lower()

        if "filename" in lower_line and "/." in lower_line:
            hidden_files.append(line.strip())

        if any(ext in lower_line for ext in [".exe", ".bat", ".sh", ".apk", ".tmp", ".scr"]):
            suspicious_files.append(line.strip())

        if "modify date" in lower_line or "file modification date" in lower_line:
            try:
                date_str = line.split(":")[-1].strip()
                file_date = datetime.strptime(date_str[:19], "%Y-%m-%d %H:%M:%S")
                if file_date > datetime.now() - timedelta(days=7):
                    recent_files.append(line.strip())
            except:
                pass

    report_lines.append("🕵 Metadata Pattern Analysis\n")
    total_flags = len(hidden_files) + len(suspicious_files) + len(recent_files)
    if hidden_files:
        report_lines.append(f"🔸 Hidden Files Detected: {len(hidden_files)}")
        report_lines += hidden_files
    if suspicious_files:
        report_lines.append(f"\n🔸 Suspicious File Types Found: {len(suspicious_files)}")
        report_lines += suspicious_files
    if recent_files:
        report_lines.append(f"\n🔸 Recently Modified Files (7 days): {len(recent_files)}")
        report_lines += recent_files

    if not (hidden_files or suspicious_files or recent_files):
        report_lines.append("✅ No suspicious patterns found in metadata.")

    report_lines.append("\n📊 Risk Evaluation:")
    if total_flags == 0:
        risk_level = "✅ Low Risk"
    elif total_flags <= 3:
        risk_level = "⚠ Medium Risk"
    else:
        risk_level = "❌ High Risk"

    report_lines.append(f"Total Flags Detected: {total_flags}")
    report_lines.append(f"Assigned Risk Level: {risk_level}")
    return report_lines
