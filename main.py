import subprocess
import sys
import os
import signal
import time

def run_processes():
    try:
        # Start barcode scanner process
        scanner = subprocess.Popen([sys.executable, 'scanner_recipient.py'])
        print("Started barcode scanner process")

        # Start reset scheduler process
        reset_scheduler = subprocess.Popen([sys.executable, 'reset_json.py'])
        print("Started reset scheduler process")

        # Start web server
        webapp = subprocess.Popen([sys.executable, 'webapp.py'])
        print("Started web server")

        # Keep the main process running and monitor child processes
        while True:
            if scanner.poll() is not None:
                print("Scanner process died, restarting...")
                scanner = subprocess.Popen([sys.executable, 'test2.py'])

            if reset_scheduler.poll() is not None:
                print("Reset scheduler died, restarting...")
                reset_scheduler = subprocess.Popen([sys.executable, 'reset_json.py'])

            if webapp.poll() is not None:
                print("Web server died, restarting...")
                webapp = subprocess.Popen([sys.executable, 'webapp.py'])

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nShutting down all processes...")
        for proc in [scanner, reset_scheduler, webapp]:
            if proc:
                proc.terminate()
                proc.wait()
        print("All processes terminated")

if __name__ == "__main__":
    # Ensure we're in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_processes()
