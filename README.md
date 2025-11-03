# File Sorter

**File Sorter** is a simple Python application that automatically organizes files based on their extensions.  
It supports both **terminal-based operation** and a **graphical user interface (GUI)**.  

This version allows you to run a single command and automatically installs itself for future use. After the first run, you can use `file_sorter` directly from the terminal.



## Features

- Automatically sorts files into folders by **extension** (e.g., `jpg`, `pdf`, `odf`).  
- Works in **terminal** or via a **GUI** (Tkinter).  
- **Self-installing CLI**: After the first run, you can type `file_sorter` directly.  
- Cross-platform: Linux and macOS.  
- Minimal and user-friendly interface.


## Installation & First Run

1. Clone the repository:

```bash
git clone https://github.com/username/file_sorter.git
cd file_sorter
```

## Make sure Python 3 is installed
   
```bash
python3 --version
```

##  Install Tkinter for GUI


* On Ubuntu/Debian:
 ```bash
sudo apt install python3-tk
```

## Run the program for the first time

python3 file_sorter.py
During the first run, the program will automatically copy itself to ~/bin/file_sorter and set the proper permissions.
After this, you can simply type file_sorter from the terminal to run it.



## Usage

* 1. Terminal Usage

You can run the program and specify a folder:

file_sorter /home/user/Downloads

This will sort all files in the specified folder into subfolders based on their extensions.


* 2. GUI Usage

Run the program without any arguments:

file_sorter

A graphical window will open.

Click Browse Folder to select a folder.

Click Sort Files to organize files.

A confirmation message will appear when the operation is complete.


