import os
import sys
import time
import hashlib
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from colorama import init, Fore, Style

# 📁 CONFIGURATION
MONITOR_FOLDER = os.path.join(os.environ["USERPROFILE"], "Desktop", "CODTECH SOLUTIONS", "test_folder")
LOG_DIR = os.path.join(os.environ["USERPROFILE"], "Desktop","CODTECH SOLUTIONS", "FileIntegrityChecker")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "integrity_log.txt")
DB_FILE = os.path.join(LOG_DIR, "file_hashes.json")
ERROR_LOG = os.path.join(LOG_DIR, "error_log.txt")

# ==========================
# 🔐 HELPER FUNCTIONS
# ==========================
def calculate_hash(file_path):
    """Generate SHA256 hash of a file"""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        log_error(f"Error hashing {file_path}: {e}")
        return None

def log_event(message):
    """Write normal event to log file and print to terminal"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"

    # Print to terminal
    print(entry)

    # Write plain text to log file (remove color codes)
    import re
    plain_entry = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(plain_entry + "\n")

def log_error(message):
    """Write error to separate file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(entry)

def load_db():
    """Load file hashes or create empty DB if missing"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    else:
        # Create empty JSON file
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
        return {}

def save_db(db):
    """Save file hashes"""
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

# 👁 EVENT HANDLER
init(autoreset=True)

class IntegrityChecker(FileSystemEventHandler):
    def __init__(self):
        self.db = load_db()
        # Initial scan of existing files
        for root, dirs, files in os.walk(MONITOR_FOLDER):
            for f in files:
                full_path = os.path.join(root, f)
                file_hash = calculate_hash(full_path)
                if file_hash and full_path not in self.db:
                    self.db[full_path] = file_hash
                    save_db(self.db)
                    file_name = os.path.basename(full_path)
                    colored_name = f"{Style.BRIGHT}{Fore.BLUE}{file_name}{Style.RESET_ALL}"
                    log_event(f" '{colored_name}' EXISTING FILE DETECTED | Path: {full_path}")

    def on_created(self, event):
        if not event.is_directory:
            file_hash = calculate_hash(event.src_path)
            if file_hash:
                self.db[event.src_path] = file_hash
                save_db(self.db)
                file_name = os.path.basename(event.src_path)
                colored_name = f"{Style.BRIGHT}{Fore.GREEN}{file_name}{Style.RESET_ALL}"
                log_event(f"🟢 '{colored_name}' SEEMS TO BE CREATED | Path: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            if event.src_path in self.db:
                del self.db[event.src_path]
                save_db(self.db)
                file_name = os.path.basename(event.src_path)
                colored_name = f"{Style.BRIGHT}{Fore.RED}{file_name}{Style.RESET_ALL}"
                log_event(f"🔴 '{colored_name}' FILE SEEMS TO BE DELETED | Path: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            new_hash = calculate_hash(event.src_path)
            old_hash = self.db.get(event.src_path)
            if new_hash and old_hash and new_hash != old_hash:
                self.db[event.src_path] = new_hash
                save_db(self.db)
                file_name = os.path.basename(event.src_path)
                colored_name = f"{Style.BRIGHT}{Fore.YELLOW}{file_name}{Style.RESET_ALL}"
                log_event(f"🟡 '{colored_name}' FILE SEEMS TO BE MODIFIED | Path: {event.src_path}")

# ==========================
# 🚀 MAIN
# ==========================
if __name__ == "__main__":
    try:
        log_event(f"🔍 Started monitoring: {MONITOR_FOLDER}")
        event_handler = IntegrityChecker()
        observer = Observer()
        observer.schedule(event_handler, MONITOR_FOLDER, recursive=True)
        observer.start()

        while True:
            time.sleep(1)

    except Exception as e:
        log_error(f"Main loop error: {e}")
        observer.stop()
        observer.join()
