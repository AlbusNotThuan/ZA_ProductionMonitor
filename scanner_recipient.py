import json
import time
import os
from pynput import keyboard
from multiprocessing import Process
import threading
from collections import deque

# File to store the logged data
LOG_FILE = "barcode_scans.json"

# Initialize an empty list to store scanned data
scanned_data = []

# Threshold in seconds to differentiate barcode scanner input from keyboard input
BARCODE_THRESHOLD = 0.02  # Increased from 0.001 to 0.05

# Variable to track the time of the last key press
last_key_time = None

# Rolling buffer to store the last few key press intervals
TIMING_BUFFER_SIZE = 5
timing_buffer = deque(maxlen=TIMING_BUFFER_SIZE)

# Function to save data to JSON file
def save_to_json(entry):
    try:
        # Only save if the entry is from barcode scanner
        if entry.get("source") == "barcode":
            entry["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Create file if it doesn't exist or append to existing
            if not os.path.exists(LOG_FILE):
                with open(LOG_FILE, "w") as file:
                    file.write("")

            # Append the entry
            with open(LOG_FILE, "a") as file:
                file.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

# Function to handle key presses
def on_press(key):
    global last_key_time, scanned_data, timing_buffer
    try:
        current_time = time.time()
        is_barcode = False

        # Calculate time difference between key presses
        if last_key_time is not None:
            time_diff = current_time - last_key_time
            timing_buffer.append(time_diff)  # Add the time difference to the buffer
            print(f"Time since last key: {time_diff:.4f} seconds")

            # Classify as barcode if all recent intervals are below the threshold
            if len(timing_buffer) == TIMING_BUFFER_SIZE and all(t < BARCODE_THRESHOLD for t in timing_buffer):
                is_barcode = True
                # Also mark the previous entry as barcode if it exists
                if scanned_data and not 'complete' in scanned_data[-1]:
                    scanned_data[-1]['source'] = 'barcode'
        
        last_key_time = current_time

        # Append the character to the last entry or create a new one
        if hasattr(key, 'char') and key.char is not None:
            if not scanned_data or 'complete' in scanned_data[-1]:
                # Use is_barcode flag to set the source
                new_entry = {"barcode": key.char, "source": "barcode" if is_barcode else "keyboard"}
                scanned_data.append(new_entry)
            else:
                scanned_data[-1]["barcode"] += key.char
                # Update source if it's detected as barcode input
                if is_barcode:
                    scanned_data[-1]["source"] = "barcode"
                print(f"Current state: {scanned_data[-1]['source']}")
        elif key == keyboard.Key.enter:
            # Mark the current barcode as complete
            if scanned_data and 'barcode' in scanned_data[-1]:
                scanned_data[-1]["complete"] = True
                save_to_json(scanned_data[-1])  # Save only the completed entry
                print("========================================")
    except Exception as e:
        print(f"Error: {e}")

# Function to handle key releases (optional, can be omitted)
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener on 'Esc' key
        return False

# Function to start the barcode scanner logger
def barcode_logger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Main entry point to run the logger as a process
if __name__ == "__main__":
    process = Process(target=barcode_logger)
    process.start()
    print(f"Barcode scanner logger is running as a process with PID: {process.pid}")
    process.join()
