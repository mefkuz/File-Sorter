# 🗂️ File Sorter v2.0

**File Sorter** is a lightweight Python application that automatically organizes your files by extension.  
It supports both **terminal (CLI)** and **graphical user interface (GUI)** modes.  

This version includes a modern **CustomTkinter GUI**, optional **subfolder inclusion**, and enhanced logging with progress updates.  

Once you run it for the first time, it installs required packages automatically and can be used directly via terminal or GUI.



## Features

- 📁 Automatically sorts files into folders by **file type** (e.g., `jpg`, `pdf`, `txt` or `music`, `video`).  
- 💻 Works via **terminal (CLI)** or **GUI (CustomTkinter)**.  
- ⚙️ **Self-installing dependencies** – missing packages are automatically installed on first run.  
- 🧩 Handles duplicate filenames and files **without extensions**.  
- ✔️ Option to **include subfolders** when sorting.  
- 🪟 Cross-platform: **Linux**, **macOS**, and **Windows**.  
- 🧼 Clean and modern **GUI interface** with live logs.  
- 💡 Shows progress bar and detailed **file statistics** before sorting.  


## Installation & First Run


###  Clone the repository in linux

```bash
git clone https://github.com/username/file_sorter.git
cd file_sorter
```


### Make sure Python 3 is installed
   
```bash
python3 --version
```

### Run the program for the first time

 On first run, the app installs itself automatically to:

`~/bin/file_sorter` on Linux/macOS

`%USERPROFILE\AppData\Local\Programs\file_sorter` on Windows


After installation, you can use it directly from the terminal:

 ```bash
file_sorter
 ```

## Usage

* **1. Terminal Mode**

Run File Sorter and specify a folder to organize:

file_sorter /home/user/Downloads

This will sort all files in the specified folder into subfolders named after their extensions.



* **2. GUI Mode**

If you run the program without any arguments:

file_sorter

A graphical window will appear:

1. Click Browse Folder to select a folder.

2. Click Sort Files to organize them.

3. A success message will appear once sorting is complete.


## Supported Languages

- English (EN)

- Turkish (TR)

*You will be prompted to select the language on first run.*

