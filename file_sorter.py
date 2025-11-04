#!/usr/bin/env python3
import os
import shutil
import sys
import subprocess
from pathlib import Path
import urllib.request
import threading

__version__ = "2.3"

# -------------------------
# Paket kontrolü
# -------------------------
def install_and_import(package_name, import_name=None):
    import_name = import_name or package_name
    try:
        return __import__(import_name)
    except ImportError:
        print(f"⚠️ {package_name} bulunamadı, yükleniyor...")
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
        "update_available": "New version available: v{}",
        "update_prompt_gui": "New version found (v{}).\n\nChanges:\n{}\n\nPlease restart the app to update.",
        "update_prompt_cli": "New version found (v{}).\n\nChanges:\n{}\nUpdate now? (y/n): ",
        "update_complete": "Update complete. Please restart the program.",
        # ... diğer mesajlar ...
    },
    "TR": {
        "update_available": "Yeni sürüm mevcut: v{}",
        "update_prompt_gui": "Yeni sürüm bulundu (v{}).\n\nDeğişiklikler:\n{}\n\nGüncellemek için uygulamayı yeniden başlatın.",
        "update_prompt_cli": "Yeni sürüm bulundu (v{}).\n\nDeğişiklikler:\n{}\nŞimdi güncellemek ister misiniz? (y/n): ",
        "update_complete": "Güncelleme tamamlandı. Lütfen programı yeniden başlatın.",
        # ... diğer mesajlar ...
    }
}

def log_msg(key, *args, level="INFO", gui_widget=None):
    msg = MESSAGES[LANG].get(key, key).format(*args)
    log(msg, level, gui_widget)

# -------------------------
# Güncelleme sistemi
# -------------------------
VERSION_URL = "https://raw.githubusercontent.com/mefkuz/File-Sorter/main/Versiyon.txt"
SCRIPT_URL = "https://raw.githubusercontent.com/mefkuz/File-Sorter/main/file_sorter.py"
CHANGELOG_URL = "https://raw.githubusercontent.com/mefkuz/File-Sorter/main/Changelog.txt"

def extract_changelog_text(changelog_content, lang="EN"):
    sections = {"TR": "", "EN": ""}
    current = None
    for line in changelog_content.splitlines():
        if line.strip() == "---TR---":
            current = "TR"; continue
        elif line.strip() == "---EN---":
            current = "EN"; continue
        elif current:
            sections[current] += line + "\n"
    return sections.get(lang, "").strip() or "(No changelog available.)"

def safe_update_check(gui=False):
    """GUI ve CLI için güvenli güncelleme kontrolü, crash-proof"""
    try:
        with urllib.request.urlopen(VERSION_URL, timeout=5) as response:
            latest_version = response.read().decode("utf-8").strip()
        if latest_version == __version__:
            return
        try:
            with urllib.request.urlopen(CHANGELOG_URL, timeout=5) as response:
                changelog_full = response.read().decode("utf-8")
                changelog_text = extract_changelog_text(changelog_full, LANG)
        except:
            changelog_text = "(Change details unavailable.)" if LANG=="EN" else "(Değişiklik bilgisi alınamadı.)"

        if gui:
            msg = MESSAGES[LANG]["update_prompt_gui"].format(latest_version, changelog_text)
            # GUI’de otomatik restart yok, sadece uyarı
            try:
                messagebox.showinfo("Update" if LANG=="EN" else "Güncelleme", msg)
            except:
                print(msg)
        else:
            msg = MESSAGES[LANG]["update_prompt_cli"].format(latest_version, changelog_text)
            choice = input(msg).strip().lower()
            if choice != "y":
                return
            # CLI modunda otomatik güncelleme ve restart
            try:
                with urllib.request.urlopen(SCRIPT_URL, timeout=10) as f:
                    new_code = f.read().decode("utf-8")
                with open(__file__, "w", encoding="utf-8") as file:
                    file.write(new_code)
                print(MESSAGES[LANG]["update_complete"])
                os.execv(sys.executable, [sys.executable] + sys.argv)
            except Exception as e:
                print(f"[Update failed] {e}")
    except Exception as e:
        print(f"[Update check failed] {e}")

# -------------------------
# Ana kodun (kategori, move_files_with_progress, run_gui, run_cli, vb.)
# -------------------------
# Burada mevcut kodun değişmeden gelecek
# get_category_for_extension, move_files_with_progress, run_gui, run_cli vs.

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    is_cli = len(sys.argv) > 1 and sys.argv[1].lower() == "cli"

    if LANG is None:
        try:
            lang_choice = input("Select language / Dil seçin (EN/TR): ").strip().upper()
            LANG = "TR" if lang_choice == "TR" else "EN"
        except:
            LANG = "EN"

    # GUI için ayrı thread’de güvenli güncelleme
    if not is_cli:
        threading.Thread(target=safe_update_check, args=(True,), daemon=True).start()
    else:
        safe_update_check(gui=False)

    if is_cli:
        run_cli()
    else:
        run_gui()