# Folder Synchronization Program

This program synchronizes files between a source folder and a replica folder.

## Functionality:

The program iterates through the files in the source folder and checks if they exist in the replica folder. If a file is missing in the replica folder or if it's different, it copies the file. It also removes files from the replica folder that don't exist in the source folder.

## Dependencies:

- Python 3.x
- No third-party libraries are required. The program utilizes built-in Python libraries:
  - os
  - shutil
  - logging
  - time
  - threading
  - tkinter

## Usage:

1. Run the program by executing the Python script.
2. Use the "Browse" button to select the source folder.
3. Use the "Browse" button to select the replica folder.
4. Set the synchronization interval in seconds (default is 30 seconds).
5. Click the "Start Sync" button to begin synchronization.
6. The program will sync the folders initially and then periodically based on the specified interval.
7. Click the "Stop Sync" button to stop synchronization.

## Logging:

The program logs the synchronization actions to a log file.

### Log Format:

- Each log entry includes a timestamp and the action taken (e.g., file copied or removed).

## Example Usage:

Open a terminal in the folder where the program is located and run:

```
python main.py
```
