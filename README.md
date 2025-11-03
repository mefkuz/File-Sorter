# 🗂️ File Sorter

**File Sorter** is a lightweight Python application that automatically organizes your files by extension.  
It supports both **terminal (CLI)** and **graphical user interface (GUI)** modes.

Once you run it for the first time, it installs itself automatically, allowing you to use `file_sorter` directly from the terminal anytime.



## ✨ Features

- 📁 Automatically sorts files into folders by **file type** (e.g., `jpg`, `pdf`, `txt`).
- 💻 Works via **terminal** or **GUI (Tkinter)**.
- ⚙️ **Self-installing CLI** – after the first run, you can use `file_sorter` directly.
- 🧩 Handles duplicate filenames and files without extensions.
- 🪟 Cross-platform: **Linux**, **macOS**, and **Windows**.
- 🧼 Clean and simple interface.



## ⚙️ Installation & First Run

###  Clone the repository in linux

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

* On macOS (if using Homebrew):
 ```bash
brew install python-tk
 ```

* On Windows:
Tkinter is included by default with Python.


## Run the program for the first time

 On first run, the app installs itself automatically to:

~/bin/file_sorter on Linux/macOS

%USERPROFILE%\AppData\Local\Programs\file_sorter on Windows


After installation, you can use it directly from the terminal:

 ```bash
file_sorter
 ```



## Usage

* 1. Terminal Mode

Run File Sorter and specify a folder to organize:

file_sorter /home/user/Downloads

This will sort all files in the specified folder into subfolders named after their extensions.

**Example result:**

Downloads/
├── jpg/
│   ├── photo1.jpg
│   └── photo2.jpg
├── pdf/
│   └── document.pdf
└── no_extension/
    └── README



* 2. GUI Mode

If you run the program without any arguments:

file_sorter

A graphical window will appear:

1. Click Browse Folder to select a folder.


2. Click Sort Files to organize them.


3. A success message will appear once sorting is complete.


