import logging
import os
import shutil
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox

class SyncFolderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Synchronization")

        self.source_folder = ""
        self.replica_folder = ""
        self.interval = 0
        self.stop_sync_event = threading.Event()

        # GUI elements
        tk.Label(root, text="Source Folder:").grid(row=0, column=0)
        self.source_entry = tk.Entry(root, width=50)
        self.source_entry.grid(row=0, column=1)
        tk.Button(root, text="Browse", command=self.browse_source).grid(row=0, column=2)

        tk.Label(root, text="Replica Folder:").grid(row=1, column=0)
        self.replica_entry = tk.Entry(root, width=50)
        self.replica_entry.grid(row=1, column=1)
        tk.Button(root, text="Browse", command=self.browse_replica).grid(row=1, column=2)

        tk.Label(root, text="Sync Interval (seconds):").grid(row=2, column=0)
        self.interval_entry = tk.Entry(root, width=10)
        self.interval_entry.grid(row=2, column=1)

        self.log_text = tk.Text(root, state='disabled', width=60, height=15)
        self.log_text.grid(row=3, column=0, columnspan=3, pady=10)

        self.start_button = tk.Button(root, text="Start Synchronization", command=self.start_sync)
        self.start_button.grid(row=4, column=0, columnspan=3)

        self.stop_button = tk.Button(root, text="Stop Synchronization", command=self.stop_sync, state=tk.DISABLED)
        self.stop_button.grid(row=5, column=0, columnspan=3)

        self.setup_logging("sync_log.txt")

    def setup_logging(self, log_file):
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)

        text_handler = TextHandler(self.log_text)
        text_handler.setLevel(logging.INFO)
        text_handler.setFormatter(formatter)
        logging.getLogger().addHandler(text_handler)

    def browse_source(self):
        self.source_folder = filedialog.askdirectory()
        self.source_entry.insert(0, self.source_folder)

    def browse_replica(self):
        self.replica_folder = filedialog.askdirectory()
        self.replica_entry.insert(0, self.replica_folder)

    def start_sync(self):
        try:
            self.source_folder = self.source_entry.get()
            self.replica_folder = self.replica_entry.get()
            self.interval = int(self.interval_entry.get())

            if not os.path.exists(self.source_folder) or not os.path.exists(self.replica_folder):
                messagebox.showerror("Error", "Both source and replica folders must exist.")
                return

            self.stop_sync_event.clear()
            self.sync_thread = threading.Thread(target=self.sync_folders_periodically)
            self.sync_thread.start()
            self.log_message("Synchronization started.")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        except ValueError:
            messagebox.showerror("Error", "Sync interval must be an integer.")

    def stop_sync(self):
        self.stop_sync_event.set()
        self.sync_thread.join()
        self.log_message("Synchronization stopped.")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def sync_folders_periodically(self):
        while not self.stop_sync_event.is_set():
            sync_folders(self.source_folder, self.replica_folder)
            time.sleep(self.interval)

    def log_message(self, message):
        logging.info(message)

class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.config(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.config(state='disabled')
            self.text_widget.see(tk.END)
        self.text_widget.after(0, append)

def sync_folders(source_folder, replica_folder):
    # Sync source to replica
    for root, dirs, files in os.walk(source_folder):
        relative_path = os.path.relpath(root, source_folder)
        replica_dir = os.path.join(replica_folder, relative_path)
        try:
            if not os.path.exists(replica_dir):
                os.makedirs(replica_dir)
                logging.info(f"Created directory {replica_dir}")

            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(replica_dir, file)
                try:
                    if not os.path.exists(replica_file_path) or \
                       os.path.getmtime(source_file_path) > os.path.getmtime(replica_file_path):
                        shutil.copy2(source_file_path, replica_file_path)
                        logging.info(f"Copied {source_file_path} to {replica_file_path}")
                except PermissionError as e:
                    logging.error(f"Permission error copying file {source_file_path}: {e}")
                    continue
        except PermissionError as e:
            logging.error(f"Permission error creating directory {replica_dir}: {e}")
            continue

    # Sync deletions from source to replica
    for root, dirs, files in os.walk(replica_folder):
        relative_path = os.path.relpath(root, replica_folder)
        source_dir = os.path.join(source_folder, relative_path)
        try:
            if not os.path.exists(source_dir):
                shutil.rmtree(root)
                logging.info(f"Deleted directory {root}")

            for file in files:
                replica_file_path = os.path.join(root, file)
                source_file_path = os.path.join(source_dir, file)
                try:
                    if not os.path.exists(source_file_path):
                        os.remove(replica_file_path)
                        logging.info(f"Deleted file {replica_file_path}")
                except PermissionError as e:
                    logging.error(f"Permission error deleting file {replica_file_path}: {e}")
                    continue
                except FileNotFoundError as e:
                    logging.error(f"File not found error deleting file {replica_file_path}: {e}")
                    continue
        except PermissionError as e:
            logging.error(f"Permission error deleting directory {root}: {e}")
            continue
if __name__ == "__main__":
    root = tk.Tk()
    app = SyncFolderGUI(root)
    root.mainloop()
