import time
import json
import os
from datetime import datetime

LOG_FILE = "barcode_scans.json"
STATUS_FILE = "reset_status.json"

def get_reset_status():
    try:
        with open(STATUS_FILE, 'r') as f:
            return json.load(f).get('active', True)
    except:
        return True

def ensure_files_exist():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as file:
            file.write("")
        print(f"Created {LOG_FILE}")
    
    if not os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "w") as file:
            json.dump({"active": True}, file)
        print(f"Created {STATUS_FILE}")

def reset_json_file():
    while True:
        if get_reset_status():
            now = datetime.now()
            if now.hour == 20 and now.minute == 0:  # 8:00 PM
                print("Resetting JSON file at 8 PM...")
                # Properly initialize/reset the file
                with open(LOG_FILE, "w") as file:
                    file.write("")  # Create empty file
                time.sleep(60)
        time.sleep(1)

if __name__ == "__main__":
    ensure_files_exist()
    print("JSON reset process is running...")
    reset_json_file()
