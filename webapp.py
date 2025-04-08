from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import json
import os
import time

# File to read the logged data
LOG_FILE = "barcode_scans.json"
STATUS_FILE = "reset_status.json"  # Add this with other constants

app = Flask(__name__)
# app.secret_key = "your_secret_key"  # Secret key for session management

TARGET = 200
LINE_NAME = "Production Line 1"  # Default line name
RESET_SCRIPT_ACTIVE = True  # Track reset script status

# Route to serve the main web page
@app.route("/")
def index():
    return render_template("index.html", target=TARGET, line_name=LINE_NAME)

# Function to preprocess data
def preprocess_data():
    processed_data = []
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        with open(LOG_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                try:
                    entry = json.loads(line)
                    if entry.get("complete"):
                        processed_data.append(entry)
                except json.JSONDecodeError:
                    continue

    if not processed_data:
        return [0, 0]

    percentage = round(len(processed_data) / TARGET * 100, 2) if TARGET > 0 else 0
    return [len(processed_data), percentage]

# Function to reset the JSON file
def reset_json():
    with open(LOG_FILE, "w") as file:
        file.write("")  # Create empty file

def save_reset_status(status):
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump({"active": status}, f)
    except Exception as e:
        print(f"Error saving reset status: {e}")

def get_reset_status():
    try:
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, 'r') as f:
                return json.load(f).get('active', True)
        return True
    except Exception as e:
        print(f"Error reading reset status: {e}")
        return True

# Route to fetch the processed scanned data dynamically
@app.route("/data")
def get_data():
    processed_data = preprocess_data()  # Preprocess the data before sending
    return jsonify({
        "count": processed_data[0],
        "percentage": processed_data[1],
        "line_name": LINE_NAME,
        "target": TARGET
    })

# Route for admin panel (no login required)
@app.route("/admin", methods=["GET", "POST"])
def admin():
    global TARGET, LINE_NAME, RESET_SCRIPT_ACTIVE
    if request.method == "POST":
        if "target" in request.form:
            try:
                TARGET = int(request.form["target"])
            except ValueError:
                return "Invalid target value", 400
        if "line_name" in request.form:
            LINE_NAME = request.form["line_name"]
        if "reset_script_active" in request.form:
            status = request.form["reset_script_active"] == "true"
            RESET_SCRIPT_ACTIVE = status
            save_reset_status(status)
            return jsonify({"status": "success"})
        if "reset_now" in request.form:
            reset_json()
        return redirect(url_for("admin"))
    return render_template("admin.html", 
                         target=TARGET, 
                         line_name=LINE_NAME, 
                         reset_active=get_reset_status())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
