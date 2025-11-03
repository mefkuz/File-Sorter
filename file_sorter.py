#!/usr/bin/env python3
import os
import shutil
import sys

USER_BIN = os.path.expanduser("~/bin")
TARGET = os.path.join(USER_BIN, "file_sorter")

def install_self():
    os.makedirs(USER_BIN, exist_ok=True)
    src = os.path.abspath(__file__)
    shutil.copy(src, TARGET)
    os.chmod(TARGET, 0o755)
    print(f"Installed file_sorter to {TARGET}. You can now run 'file_sorter' from terminal.")

def sort_files_terminal(folder):
    if not os.path.exists(folder):
        print(f"{folder} not found.")
        return
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            ext = filename.split('.')[-1].lower()
            target_folder = os.path.join(folder, ext)
            os.makedirs(target_folder, exist_ok=True)

            # Dosya çakışmasını önlemek ve hata kontrolü
            base, extension = os.path.splitext(filename)
            new_name = filename
            counter = 1
            while os.path.exists(os.path.join(target_folder, new_name)):
                new_name = f"{base}_{counter}{extension}"
                counter += 1

            try:
                shutil.move(file_path, os.path.join(target_folder, new_name))
            except Exception as e:
                print(f"Failed to move {filename}: {e}")

    print("Files have been sorted by their extensions.")

def run_gui():
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
    except ImportError:
        print("Tkinter is required for GUI. Install it using your package manager.")
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
    root.title("File Sorter")
    root.geometry("400x150")

    tk.Label(root, text="Select Folder:").pack(pady=5)
    entry_folder = tk.Entry(root, width=50)
    entry_folder.pack(pady=5)

    tk.Button(root, text="Browse Folder", command=browse_folder).pack(pady=5)
    tk.Button(root, text="Sort Files", command=sort_files).pack(pady=10)

    root.mainloop()

def main():
    # Self-install: Eğer ilk kez çalıştırılıyorsa ve hedef yoksa kopyala
    if not os.path.exists(TARGET):
        install_self()

    if len(sys.argv) > 1:
        folder = sys.argv[1]
        sort_files_terminal(folder)
    else:
        run_gui()

if __name__ == "__main__":
    main()