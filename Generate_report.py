from datetime import datetime
from analyze_metadata import analyze_metadata
import os

def generate_report(device_type, case_id, investigator, hidden_count=0, deleted_count=0):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = f"reports/report_{device_type}_{now}.txt"

    with open(report_path, "w") as f:
        f.write("FORENSCOPE - Forensic Extraction Report\n")
        f.write("=========================================\n")
        f.write(f"Date/Time       : {now}\n")
        f.write(f"Case ID         : {case_id}\n")
        f.write(f"Investigator    : {investigator}\n")
        f.write(f"Device Type     : {device_type}\n\n")

        if os.path.exists("logs/hash.txt"):
            f.write("SHA256 Hash:\n")
            with open("logs/hash.txt", "r") as h:
                f.write(h.read() + "\n")

        if os.path.exists("metadata/metadata.txt"):
            f.write("\nMetadata Extracted:\n")
            with open("metadata/metadata.txt", "r") as m:
                f.write(m.read())

        f.write(f"\nHidden Files Detected: {hidden_count}")
        f.write(f"\nDeleted-Like Files Detected: {deleted_count}")

        f.write("\n\n🔍 Metadata Pattern Analysis:\n")
        analysis = analyze_metadata("metadata/metadata.txt")
        for line in analysis:
            f.write(line + "\n")

        f.write("\nReport Status   : COMPLETED ✅\n")
        f.write("=========================================\n")

    print(f"✅ Report saved at: {report_path}")
