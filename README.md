# Folder Synchronization Project

This project implements a Python program to synchronize two folders: a source folder (`source`) and a replica folder (`replica`). The program maintains an identical copy of the source folder in the replica folder, performing synchronization periodically.

---

## Features

- **One-Way Synchronization**:
  - The replica folder is updated to exactly match the content of the source folder.
  - New files are copied, modified files are updated, and obsolete files are removed.

- **Periodic Synchronization**:
  - Synchronization is performed at user-defined intervals.

- **Operation Logging**:
  - All operations (copy, removal, etc.) are logged to a file and displayed in the terminal.

- **Integrity Check**:
  - The program compares files using MD5 hash to ensure only modified files are copied.

---

## How to Use

### Prerequisites

- Python 3.x installed.
- Required Python modules: `os`, `hashlib`, `shutil`, `argparse`, `logging`, `time`.

### Running the Program

1. Clone the repository**:
   ```bash
   git clone https://github.com/tonythecoder1/folder_project_v1.git
   

2. Navigate to the project folder:
   Example: cd repository-name
   
4. Run the program:
   
  Example:

         python folder_project.py <source_folder> <replica_folder> <interval> <log_file>

  Where:
   
      <source_folder>: Full path to the source folder.

      <replica_folder>: Full path to the replica folder.

      <interval>: Synchronization interval in seconds.

      <log_file>: Full path to the log file.
  
