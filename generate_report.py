# === generate_report.py ===
from datetime import datetime
from analyze_metadata import analyze_metadata
import os

def generate_report(device_type, case_id, investigator, hidden_count=0, deleted_like_count=0):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = f"/home/pi/forenscope2/forenscope/reports/report_{device_type}_{now}.txt"

    with open(report_path, "w") as f:
        f.write("FORENSCOPE - Forensic Extraction Report\n")
        f.write("=========================================\n")
        f.write(f"Date/Time       : {now}\n")
        f.write(f"Case ID         : {case_id}\n")
        f.write(f"Investigator    : {investigator}\n")
        f.write(f"Device Type     : {device_type}\n\n")

        # SHA256 Hash
        hash_path = "/home/pi/forenscope2/forenscope/logs/hash.txt"
        if os.path.exists(hash_path):
            with open(hash_path, "r") as h:
                f.write("SHA256 Hash:\n" + h.read() + "\n")

        # Metadata
        meta_path = "/home/pi/forenscope2/forenscope/metadata/metadata.txt"
        if os.path.exists(meta_path):
            f.write("\nMetadata Extracted:\n")
            with open(meta_path, "r") as m:
                f.write(m.read() + "\n")

        # Pattern analysis section
        analysis = analyze_metadata(meta_path)
        f.write("\n🔍 Pattern-Based Analysis:\n")
        for line in analysis:
            f.write(line + "\n")

        # Additional findings
        f.write(f"\nHidden Files Detected   : {hidden_count}")
        f.write(f"\nDeleted-like Files Found: {deleted_like_count}\n")

        # Image size
        img_dir = "/home/pi/forenscope2/forenscope/images/"
        for file in os.listdir(img_dir):
            if file.endswith(".img"):
                file_path = os.path.join(img_dir, file)
                size_gb = round(os.path.getsize(file_path) / (1024**3), 2)
                f.write(f"\nImage File: {file} ({size_gb} GB)\n")

        f.write("\nReport Status   : COMPLETED ✅\n")
        f.write("=========================================\n")

    print(f"✅ Report saved at: {report_path}")
