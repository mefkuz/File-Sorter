#!/usr/bin/env python3
import os
import shutil
import sys
import subprocess
from pathlib import Path

__version__ = "2.0"

# -------------------------
# Paket kontrolü
# -------------------------
def install_and_import(package_name, import_name=None):
    import_name = import_name or package_name
    try:
        return __import__(import_name)
    except ImportError:
        print(⚠️ f"{package_name} bulunamadı, yükleniyor...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            return __import__(import_name)
        except subprocess.CalledProcessError as e:
            print(f"{package_name} yüklenemedi: {e}")
            sys.exit(1)

colorama = install_and_import("colorama")
from colorama import Fore, Style, init
init(autoreset=True)

ctk = install_and_import("customtkinter", "customtkinter")
import tkinter.messagebox as messagebox
from tkinter import filedialog

# -------------------------
# Terminal renkleri ve log
# -------------------------
class TermColors:
    RESET = "\033[0m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BRIGHT = "\033[1m"

def log(msg: str, level: str = "INFO", gui_widget=None):
    colors = {
        "INFO": TermColors.CYAN + TermColors.BRIGHT,
        "WARNING": TermColors.YELLOW + TermColors.BRIGHT,
        "ERROR": TermColors.RED + TermColors.BRIGHT,
        "ACTION": TermColors.GREEN + TermColors.BRIGHT,
    }
    color = colors.get(level, "")
    if gui_widget:
        gui_widget.insert("end", f"{msg}\n")
        gui_widget.see("end")
    else:
        print(f"{color}{msg}{TermColors.RESET}")

# -------------------------
# Dil ve mesajlar
# -------------------------
LANG = None

MESSAGES = {
    "EN": {
        "select_language": "Select language / Dil seçin (EN/TR): ",
        "folder_not_found": "Folder not found: {}",
        "no_files": "No files found in the selected folder.",
        "confirm_text": "Total items: {}\nFiles: {}\nFile types:\n{}\nDo you want to sort these files?",
        "sorting_canceled": "Sorting canceled by user.",
        "sorting_complete": "Sorting complete.",
        "files_moved": "Files moved: {}",
        "errors": "Errors: {}",
        "skipped": "Skipped: {}",
        "include_subfolders": "Include Subfolders",
        "select_folder_error": "Please select a folder.",
        "confirm_gui_sort": "Are you sure you want to sort the files?",
        "result_sorted": "Files have been sorted!",
        "browse_button": "Browse Folder",
        "sort_button": "Sort Files",
        "confirm_title": "Confirm Sorting",
        "result_title": "Result",
        "error_title": "Error"
    },
    "TR": {
        "select_language": "Dil seçin / Select language (TR/EN): ",
        "folder_not_found": "Klasör bulunamadı: {}",
        "no_files": "Seçilen klasörde dosya bulunamadı.",
        "confirm_text": "Toplam öğe: {}\nDosyalar: {}\nDosya türleri:\n{}\nBu dosyaları sıralamak istiyor musunuz?",
        "sorting_canceled": "Sıralama kullanıcı tarafından iptal edildi.",
        "sorting_complete": "Sıralama tamamlandı.",
        "files_moved": "Taşınan dosya sayısı: {}",
        "errors": "Hata sayısı: {}",
        "skipped": "Atlanan: {}",
        "include_subfolders": "Alt Klasörleri Dahil Et",
        "select_folder_error": "Lütfen bir klasör seçin.",
        "confirm_gui_sort": "Dosyaları sıralamak istediğinizden emin misiniz?",
        "result_sorted": "Dosyalar sıralandı!",
        "browse_button": "Klasör Seç",
        "sort_button": "Dosyaları Sırala",
        "confirm_title": "Sıralamayı Onayla",
        "result_title": "Sonuç",
        "error_title": "Hata"
    }
}

def log_msg(key, *args, level="INFO", gui_widget=None):
    msg = MESSAGES[LANG].get(key, key).format(*args)
    log(msg, level, gui_widget)

# -------------------------
# Dil seçimi
# -------------------------
def choose_language():
    global LANG
    if LANG is None:
        lang_choice = input("Select language / Dil seçin (EN/TR): ").strip().upper()
        if lang_choice in ("EN", "TR"):
            LANG = lang_choice
        else:
            LANG = "EN"

# -------------------------
# Dosya istatistikleri
# -------------------------
def get_file_stats(folder: str, include_subfolders: bool = False):
    all_items = []
    files = []
    extensions = {}

    if include_subfolders:
        for root_dir, _, filenames in os.walk(folder):
            for f in filenames:
                file_path = os.path.join(root_dir, f)
                files.append(file_path)
                all_items.append(file_path)
                ext = os.path.splitext(f)[1].lstrip('.').lower() or "no_extension"
                extensions[ext] = extensions.get(ext, 0) + 1
    else:
        all_items = os.listdir(folder)
        files = [os.path.join(folder, f) for f in all_items if os.path.isfile(os.path.join(folder, f))]
        for f in files:
            ext = os.path.splitext(f)[1].lstrip('.').lower() or "no_extension"
            extensions[ext] = extensions.get(ext, 0) + 1

    return all_items, files, extensions

# -------------------------
# Dosya taşıma ve ilerleme çubuğu
# -------------------------
def move_files_with_progress(folder: str, include_subfolders: bool = False, auto_confirm: bool = False, gui_widget=None):
    if not os.path.exists(folder):
        log_msg("folder_not_found", folder, level="ERROR", gui_widget=gui_widget)
        return

    all_items, files, extensions = get_file_stats(folder, include_subfolders)
    if not files:
        log_msg("no_files", level="INFO", gui_widget=gui_widget)
        return

    log(f"Folder: {folder}", level="INFO", gui_widget=gui_widget)
    log(f"Total items: {len(all_items)} | Files: {len(files)}", level="INFO", gui_widget=gui_widget)
    log("File types:", level="INFO", gui_widget=gui_widget)
    for ext, count in extensions.items():
        log(f"  • {ext}: {count}", level="INFO", gui_widget=gui_widget)

    if not auto_confirm:
        confirm_text = MESSAGES[LANG]["confirm_text"].format(len(all_items), len(files),
                                                            "\n".join([f"  • {k}: {v}" for k, v in extensions.items()]))
        confirm = input(f"{confirm_text} (y/n): ").strip().lower()
        if confirm not in ('y', 'e'):
            log_msg("sorting_canceled", level="WARNING", gui_widget=gui_widget)
            return

    moved_count = 0
    error_count = 0
    total_files = len(files)

    log("\nSorting files:", level="INFO", gui_widget=gui_widget)
    for idx, file_path in enumerate(files, start=1):
        folder_path, filename = os.path.split(file_path)
        base, extension = os.path.splitext(filename)
        ext = extension.lstrip('.').lower() or "no_extension"
        target_folder = os.path.join(folder, ext)
        os.makedirs(target_folder, exist_ok=True)

        dest = Path(target_folder) / filename
        counter = 1
        while dest.exists():
            dest = Path(target_folder) / f"{dest.stem}_{counter}{dest.suffix}"
            counter += 1

        try:
            shutil.move(file_path, dest)
            moved_count += 1
            log(f"{filename} → {target_folder}", level="ACTION", gui_widget=gui_widget)
        except Exception as e:
            error_count += 1
            log(f"Could not move {filename}: {e}", level="ERROR", gui_widget=gui_widget)
            if gui_widget:
                messagebox.showerror(MESSAGES[LANG]["error_title"], f"{filename} taşınamadı: {e}")

        progress = int((idx / total_files) * 30)
        bar = "█" * progress + "-" * (30 - progress)
        if not gui_widget:
            print(f"\r[{bar}] {idx}/{total_files} files", end="", flush=True)

    if not gui_widget:
        print()

    log_msg("sorting_complete", level="INFO", gui_widget=gui_widget)
    log_msg("files_moved", moved_count, level="INFO", gui_widget=gui_widget)
    log_msg("errors", error_count, level="INFO", gui_widget=gui_widget)
    log_msg("skipped", len(all_items) - len(files), level="INFO", gui_widget=gui_widget)

# -------------------------
# GUI
# -------------------------
def run_gui():
    choose_language()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title(f"File Sorter v{__version__}")
    root.geometry("600x400")
    root.resizable(False, False)

    # Klasör seçimi
    folder_frame = ctk.CTkFrame(root)
    folder_frame.pack(pady=20, padx=20, fill="x")

    label = ctk.CTkLabel(folder_frame, text=MESSAGES[LANG]["browse_button"])
    label.pack(anchor="w", pady=(0, 5))

    entry_folder = ctk.CTkEntry(folder_frame, width=400)
    entry_folder.pack(side="left", expand=True, fill="x", pady=5)

    def browse_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            entry_folder.delete(0, "end")
            entry_folder.insert(0, folder_selected)

    browse_btn = ctk.CTkButton(folder_frame, text=MESSAGES[LANG]["browse_button"],
                               command=browse_folder, fg_color="white", text_color="black")
    browse_btn.pack(side="left", padx=(5, 0))

    # Alt klasörleri dahil et seçeneği
    include_var = ctk.BooleanVar(value=False)
    include_cb = ctk.CTkCheckBox(root, text=MESSAGES[LANG]["include_subfolders"], variable=include_var)
    include_cb.pack(pady=(5, 10), padx=20, anchor="w")

    # Dosyaları Sırala butonu
    sort_btn = ctk.CTkButton(root, text=MESSAGES[LANG]["sort_button"], command=lambda: sort_files_gui(),
                             fg_color="white", text_color="black")
    sort_btn.pack(pady=(0, 10))

    # Log alanı
    log_frame = ctk.CTkFrame(root)
    log_frame.pack(pady=5, padx=20, fill="both", expand=True)
    log_frame.pack_forget()

    log_text = ctk.CTkTextbox(log_frame, width=560, height=150)
    log_text.pack(fill="both", expand=True)

    def sort_files_gui():
        folder = entry_folder.get()
        if not folder:
            messagebox.showwarning(MESSAGES[LANG]["error_title"], MESSAGES[LANG]["select_folder_error"])
            return
        include_subfolders = include_var.get()
        confirm = messagebox.askyesno(MESSAGES[LANG]["confirm_title"], MESSAGES[LANG]["confirm_gui_sort"])
        if confirm:
            log_frame.pack(pady=5, padx=20, fill="both", expand=True)
            move_files_with_progress(folder, include_subfolders=include_subfolders, gui_widget=log_text)
            messagebox.showinfo(MESSAGES[LANG]["result_title"], MESSAGES[LANG]["result_sorted"])

    # Footer - sağ alt köşede
    footer = ctk.CTkLabel(root, text="made by mefkuz", fg_color=None, text_color="gray")
    footer.pack(side="bottom", anchor="e", padx=10, pady=5)

    root.mainloop()

# -------------------------
# CLI
# -------------------------
def run_cli():
    choose_language()
    folder = input("Enter folder path: ").strip()
    if not folder:
        log_msg("select_folder_error", level="ERROR")
        return
    include_subfolders = input("Include subfolders? (y/n): ").strip().lower() in ("y", "e")
    move_files_with_progress(folder, include_subfolders=include_subfolders)

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        run_cli()
    else:
        run_gui()
