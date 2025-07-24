import os
from datetime import datetime, timedelta

def analyze_metadata(meta_file):
    if not os.path.exists(meta_file):
        return ["No metadata file found."]

    hidden = []
    recent = []
    suspicious = []
    output = []

    with open(meta_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        lower = line.lower()
        if "filename" in lower and "/." in lower:
            hidden.append(line.strip())
        if any(ext in lower for ext in [".exe", ".bat", ".apk", ".sh", ".tmp"]):
            suspicious.append(line.strip())
        if "modify date" in lower:
            try:
                date_str = line.split(":")[-1].strip()[:19]
                file_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                if file_time > datetime.now() - timedelta(days=7):
                    recent.append(line.strip())
            except:
                pass

    output.append("\n📊 Pattern Analysis Summary:")
    if hidden: output += ["🔸 Hidden Files:", *hidden]
    if suspicious: output += ["🔸 Suspicious Files:", *suspicious]
    if recent: output += ["🔸 Recently Modified Files:", *recent]

    risk = len(hidden) + len(suspicious) + len(recent)
    output.append(f"\nTotal Flags: {risk}")
    output.append(f"Risk Level: {'✅ Low' if risk == 0 else '⚠ Medium' if risk <= 3 else '❌ High'}")
    return output
