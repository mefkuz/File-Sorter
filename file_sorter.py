#!/usr/bin/env python3
import os
import shutil
import sys
import subprocess
from pathlib import Path
import urllib.request

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
        "use_categories": "Sort by Categories (image,videos etc.)",
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
        "use_categories": "Kategorilere Göre Sırala (resimler, videolar vs.)",
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

def check_for_update(current_version, version_url, script_url, changelog_url, script_path, gui=False, lang="EN"):
    """Güvenli güncelleme kontrolü"""
    try:
        with urllib.request.urlopen(version_url, timeout=5) as response:
            latest_version = response.read().decode("utf-8").strip()
    except Exception as e:
        log(f"[Update] Version check failed: {e}" if lang == "EN" else f"[Güncelleme] Versiyon kontrolü başarısız: {e}", level="ERROR")
        return False

    if not latest_version or latest_version == current_version:
        log("✅ Your application is up to date." if lang == "EN" else "✅ Uygulamanız güncel.", level="INFO")
        return False

    try:
        with urllib.request.urlopen(changelog_url, timeout=5) as response:
            full_changelog = response.read().decode("utf-8")
            changelog_text = extract_changelog_text(full_changelog, lang)
    except Exception as e:
        log(f"[Update] Changelog load failed: {e}", level="WARNING")
        changelog_text = "(Change details unavailable.)" if lang == "EN" else "(Değişiklik bilgisi alınamadı.)"

    log(f"🆕 New version available: v{latest_version} (current: v{current_version})" if lang == "EN"
        else f"🆕 Yeni sürüm mevcut: v{latest_version} (şu an: v{current_version})", level="WARNING")

    try:
        if gui:
            msg = (
                f"New version found (v{latest_version}).\n\nChanges:\n{changelog_text}\n\nWould you like to update?"
                if lang == "EN"
                else f"Yeni sürüm bulundu (v{latest_version}).\n\nDeğişiklikler:\n{changelog_text}\n\nGüncellemek ister misiniz?"
            )
            if not messagebox.askyesno("Update" if lang == "EN" else "Güncelleme", msg):
                return False
        else:
            print(f"\n🆕 {'New version found' if lang == 'EN' else 'Yeni sürüm bulundu'}: v{latest_version} (current: v{current_version})")
            print(f"\n--- {'Changes' if lang == 'EN' else 'Değişiklikler'} ---\n{changelog_text}\n")
            choice = input("Update now? (y/n): " if lang == "EN" else "Güncellemek ister misiniz? (y/n): ").strip().lower()
            if choice != "y":
                return False
    except Exception as e:
        log(f"[Update prompt error] {e}", level="ERROR")
        return False

    try:
        with urllib.request.urlopen(script_url, timeout=10) as f:
            new_code = f.read().decode("utf-8")

        with open(script_path, "w", encoding="utf-8") as file:
            file.write(new_code)

        msg = "✅ Update complete. Restarting..." if lang == "EN" else "✅ Güncelleme tamamlandı. Program yeniden başlatılıyor..."
        log(msg, level="ACTION")

        try:
            import tkinter
            for w in getattr(tkinter, "_default_root", {}).children.values():
                try:
                    w.destroy()
                except:
                    pass
            if getattr(tkinter, "_default_root", None):
                tkinter._default_root.destroy()
        except Exception:
            pass

        os.execv(sys.executable, [sys.executable] + sys.argv)

    except Exception as e:
        import traceback
        log(f"Update failed: {e}" if lang == "EN" else f"Güncelleme başarısız: {e}", level="ERROR")
        print(traceback.format_exc())
        return False

# -------------------------
# (Diğer ana kodun - kategori, dosya taşıma, GUI fonksiyonları vs.)
# -------------------------
# Buraya senin mevcut File Sorter fonksiyonlarının tamamı değişmeden gelecek
# (örneğin get_category_for_extension, run_gui, run_cli, vb.)

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    is_cli = len(sys.argv) > 1 and sys.argv[1].lower() == "cli"

    if LANG is None:
        try:
            lang_choice = input("Select language / Dil seçin (EN/TR): ").strip().upper()
            LANG = "TR" if lang_choice == "TR" else "EN"
        except Exception:
            LANG = "EN"

    check_for_update(
        __version__,
        VERSION_URL,
        SCRIPT_URL,
        CHANGELOG_URL,
        __file__,
        gui=not is_cli,
        lang=LANG
    )

    if is_cli:
        run_cli()
    else:
        run_gui()