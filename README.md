# Folder Synchronization Program

This program synchronizes files between a source folder and a replica folder, ensuring both folders are identical.

## Functionality

The program performs the following actions:

- Iterates through the files in the source folder and checks if they exist in the replica folder.
- Copies missing or modified files from the source to the replica folder.
- Removes files from the replica folder that don't exist in the source folder.

## Dependencies

- Python 3.x
- No third-party libraries are required. The program utilizes the following built-in Python libraries:
  - `os`
  - `shutil`
  - `logging`
  - `time`
  - `threading`
  - `tkinter`

## Usage

1. **Run the Program**:

   - Execute the Python script by running `python main.py` in your terminal or command prompt.
   - [Alternatively, download the executable version of the program and double-click to open it](https://drive.google.com/file/d/16nSsnr7xPNorEcxgBDULsji75jmmrPUs/view?usp=sharing)

2. **Select Folders**:

   - Use the "Browse" button to select the source folder.
   - Use the "Browse" button to select the replica folder.

3. **Set Synchronization Interval**:

   - Enter the synchronization interval in seconds.

4. **Start and Stop Synchronization**:
   - Click the "Start Sync" button to begin synchronization.
   - The program will sync the folders initially and then periodically based on the specified interval.
   - Click the "Stop Sync" button to stop synchronization.

## Logging

The program logs synchronization actions to a log file, providing a record of all synchronization events.

### Log Format

- Each log entry includes a timestamp and the action taken (e.g., file copied or removed).

## Example Usage

To run the program from the terminal:

```
python main.py
```

[Or for easier use, download the executable version and double-click to open it!](https://drive.google.com/file/d/16nSsnr7xPNorEcxgBDULsji75jmmrPUs/view?usp=sharing)
