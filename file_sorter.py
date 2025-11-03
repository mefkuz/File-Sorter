#!/usr/bin/env python3
import os
import shutil
import sys
import logging

__version__ = "1.0.0"

# Configure logging (optional)
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Determine user bin path (cross-platform)
if os.name == 'nt':
    # Windows path (for manual use)
    USER_BIN = os.path.join(os.getenv('USERPROFILE', ''), 'AppData', 'Local', 'Programs', 'file_sorter')
else:
    # Default for Linux/macOS
    USER_BIN = os.path.expanduser("~/bin")

TARGET = os.path.join(USER_BIN, "file_sorter")

def install_self():
    """Copy the script to ~/bin (or Windows equivalent) and make it executable."""
    try:
        os.makedirs(USER_BIN, exist_ok=True)
        src = os.path.abspath(__file__)
        shutil.copy(src, TARGET)
        if os.name != 'nt':
            os.chmod(TARGET, 0o755)
        logging.info(f"Installed file_sorter to {TARGET}")
        logging.info("You can now run 'file_sorter' from the terminal.")
    except Exception as e:
        logging.error(f"Failed to install self to {TARGET}. You might need manual setup: {e}")

def sort_files_terminal(folder):
    """Sort files in the given folder by extension."""
    if not os.path.exists(folder):
        logging.error(f"{folder} not found.")
        return

    logging.info(f"Starting sort in: {folder}")

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        if os.path.isfile(file_path):
            # Use splitext for safer extension extraction
            base, extension = os.path.splitext(filename)
            ext = extension.lstrip('.').lower()

            # Handle files with no extension
            if not ext:
                target_folder_name = "no_extension"
            else:
                target_folder_name = ext

            target_folder = os.path.join(folder, target_folder_name)
            os.makedirs(target_folder, exist_ok=True)

            # Avoid filename conflicts
            new_name = filename
            counter = 1
            while os.path.exists(os.path.join(target_folder, new_name)):
                new_name = f"{base}_{counter}{extension}"
                counter += 1

            try:
                shutil.move(file_path, os.path.join(target_folder, new_name))
            except Exception as e:
                logging.error(f"Failed to move {filename}: {e}")

    logging.info("✅ Files have been sorted by their extensions.")

def run_gui():
    """Launch a simple Tkinter-based GUI."""
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
    except ImportError:
        logging.error("Tkinter is required for the GUI. Install it using your package manager.")
        return

    def browse_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            entry_folder.delete(0, tk.END)
            entry_folder.insert(0, folder_selected)

    def sort_files():
        folder = entry_folder.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder.")
            return
        sort_files_terminal(folder)
        messagebox.showinfo("Result", "Files have been sorted!")

    root = tk.Tk()
    root.title(f"File Sorter v{__version__}")
    root.geometry("400x160")

    tk.Label(root, text="Select Folder:").pack(pady=5)
    entry_folder = tk.Entry(root, width=50)
    entry_folder.pack(pady=5)

    tk.Button(root, text="Browse Folder", command=browse_folder).pack(pady=5)
    tk.Button(root, text="Sort Files", command=sort_files).pack(pady=10)

    root.mainloop()

def main():
    """Main program entry point."""
    if not os.path.exists(TARGET):
        install_self()

    if len(sys.argv) > 1:
        folder = sys.argv[1]
        sort_files_terminal(folder)
    else:
        run_gui()

if __name__ == "__main__":
    main()