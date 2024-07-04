import os
import shutil
import logging
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

import os
import shutil
import logging
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

def sync_folders(source_folder, replica_folder):
    try:
        # Ensure replica folder exists
        if not os.path.exists(replica_folder):
            os.makedirs(replica_folder)

        # Sync logic
        for root, _, files in os.walk(source_folder):
            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(replica_folder, os.path.relpath(source_file_path, source_folder))
                try:
                    if not os.path.exists(replica_file_path) or \
                       os.stat(source_file_path).st_mtime > os.stat(replica_file_path).st_mtime:
                        # Create directories in replica folder if they don't exist
                        os.makedirs(os.path.dirname(replica_file_path), exist_ok=True)
                        shutil.copy2(source_file_path, replica_file_path)
                        logging.info(f"Copied {source_file_path} to {replica_file_path}")
                except FileNotFoundError as e:
                    logging.error(f"File not found error: {e}, Source file: {source_file_path}")

    except Exception as e:
        logging.error(f"Error during synchronization: {e}")

def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

class FolderSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Synchronization")
        self.is_running = False
        self.thread = None

        self.source_folder = ""
        self.replica_folder = ""
        self.interval = 30

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Source Folder:").grid(row=0, column=0, padx=10, pady=10)
        self.source_entry = tk.Entry(self.root, width=50)
        self.source_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self.root, text="Replica Folder:").grid(row=1, column=0, padx=10, pady=10)
        self.replica_entry = tk.Entry(self.root, width=50)
        self.replica_entry.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_replica).grid(row=1, column=2, padx=10, pady=10)

        tk.Label(self.root, text="Sync Interval (seconds):").grid(row=2, column=0, padx=10, pady=10)
        self.interval_entry = tk.Entry(self.root, width=10)
        self.interval_entry.grid(row=2, column=1, padx=10, pady=10)
        self.interval_entry.insert(0, "30")

        self.start_button = tk.Button(self.root, text="Start Sync", command=self.start_sync)
        self.start_button.grid(row=3, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(self.root, text="Stop Sync", command=self.stop_sync)
        self.stop_button.grid(row=3, column=1, padx=10, pady=10)
        self.stop_button.config(state=tk.DISABLED)

    def browse_source(self):
        self.source_folder = filedialog.askdirectory()
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, self.source_folder)

    def browse_replica(self):
        self.replica_folder = filedialog.askdirectory()
        self.replica_entry.delete(0, tk.END)
        self.replica_entry.insert(0, self.replica_folder)

    def start_sync(self):
        try:
            self.interval = int(self.interval_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Interval", "Please enter a valid number for the interval.")
            return

        self.source_folder = self.source_entry.get()
        self.replica_folder = self.replica_entry.get()

        if not self.source_folder or not self.replica_folder:
            messagebox.showerror("Missing Folders", "Please select both source and replica folders.")
            return

        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        setup_logging("sync_log.txt")
        self.thread = threading.Thread(target=self.sync_loop)
        self.thread.start()

    def stop_sync(self):
        self.is_running = False
        if self.thread:
            self.thread.join()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        logging.info("Synchronization stopped by user.")
        messagebox.showinfo("Sync Stopped", "Folder synchronization has been stopped.")

    def sync_loop(self):
        while self.is_running:
            logging.info(f"Synchronizing folders: {self.source_folder} -> {self.replica_folder}")
            sync_folders(self.source_folder, self.replica_folder)
            time.sleep(self.interval)


if __name__ == "__main__":
    root = tk.Tk()
    app = FolderSyncApp(root)
    root.mainloop()
