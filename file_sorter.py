#!/usr/bin/env python3
import os
import shutil
import sys
import subprocess
from pathlib import Path

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
        "confirm_text": "Total items: {}\nFiles to sort: {}\nFile types:\n{}\n\nDo you want to proceed with sorting?",
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
        "error_title": "Error",
        
        # CLI Specific Prompts
        "enter_folder_path": "Enter folder path: ",
        "include_subfolders_cli": "Include subfolders? (y/n): ",
        "use_categories_cli": "Sort by categories? (y/n): ",
        "proceed_confirmation": "Proceed? (y/n): "
    },
    "TR": {
        "select_language": "Dil seçin / Select language (TR/EN): ",
        "folder_not_found": "Klasör bulunamadı: {}",
        "no_files": "Seçilen klasörde dosya bulunamadı.",
        "confirm_text": "Toplam öğe: {}\nSıralanacak dosyalar: {}\nDosya türleri:\n{}\n\nSıralama işlemine devam etmek istiyor musunuz?",
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
        "error_title": "Hata",

        # CLI Specific Prompts
        "enter_folder_path": "Klasör yolunu girin: ",
        "include_subfolders_cli": "Alt klasörleri dahil et? (e/h): ",
        "use_categories_cli": "Kategorilere göre sırala? (e/h): ",
        "proceed_confirmation": "Devam edilsin mi? (e/h): "
    }
}

def log_msg(key, *args, level="INFO", gui_widget=None):
    msg = MESSAGES[LANG].get(key, key).format(*args)
    log(msg, level, gui_widget)

# -------------------------
# Kategori tanımları (çok dilli)
# -------------------------
CATEGORIES = {
    "TR": {
        "Resimler": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
        "Videolar": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
        "Müzikler": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "Belgeler": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
        "Arşivler": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Programlar": [".exe", ".msi", ".apk", ".bat", ".sh", ".app"],
        "Diğer": []
    },
    "EN": {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
        "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Programs": [".exe", ".msi", ".apk", ".bat", ".sh", ".app"],
        "Others": []
    }
}

def get_category_for_extension(ext: str, lang: str) -> str:
    ext = ext.lower()
    for category, exts in CATEGORIES[lang].items():
        if ext in exts:
            return category
    # Eğer eşleşme yoksa “Diğer” / “Others”
    return "Diğer" if lang == "TR" else "Others"

# -------------------------
# Dil seçimi
# -------------------------
def choose_language():
    global LANG
    if LANG is None:
        lang_choice = input(MESSAGES.get(None, {}).get("select_language", "Select language / Dil seçin (EN/TR): ")).strip().upper()
        LANG = "TR" if lang_choice == "TR" else "EN"

# -------------------------
# Dosya istatistikleri
# -------------------------
def get_file_stats(folder: str, include_subfolders: bool = False):
    all_items = []
    files = []
    extensions = {}

    if not os.path.exists(folder):
        return [], [], {}

    walker = os.walk(folder) if include_subfolders else [(folder, [], os.listdir(folder))]
    for root_dir, _, filenames in walker:
        for f in filenames:
            file_path = os.path.join(root_dir, f)
            if os.path.isfile(file_path):
                files.append(file_path)
                all_items.append(file_path)
                ext = os.path.splitext(f)[1].lstrip('.').lower() or "no_extension"
                extensions[ext] = extensions.get(ext, 0) + 1

    return all_items, files, extensions

# -------------------------
# Dosya taşıma fonksiyonu
# -------------------------
def move_files_with_progress(folder: str, include_subfolders: bool = False, use_categories: bool = False, gui_widget=None, progress_bar_widget=None):
    if not os.path.exists(folder):
        log_msg("folder_not_found", folder, level="ERROR", gui_widget=gui_widget)
        return

    all_items, files, extensions = get_file_stats(folder, include_subfolders)
    if not files:
        log_msg("no_files", level="INFO", gui_widget=gui_widget)
        return

    log(f"Folder: {folder}", level="INFO", gui_widget=gui_widget)
    log(f"Total items: {len(all_items)} | Files to move: {len(files)}", level="INFO", gui_widget=gui_widget)

    moved_count = 0
    error_count = 0
    total_files = len(files)

    for idx, file_path in enumerate(files, start=1):
        # Eğer progress bar varsa, her 50 dosyada bir GUI log'a yazma işlemini yavaşlat
        if gui_widget and progress_bar_widget and idx % 50 != 0:
            pass # Log yazma atlanıyor, sadece progress bar güncellenecek
        else:
            log(f"Processing: {os.path.basename(file_path)}...", level="INFO", gui_widget=gui_widget)


        folder_path, filename = os.path.split(file_path)
        base, extension = os.path.splitext(filename)
        ext = extension.lower()

        if use_categories:
            target_folder_name = get_category_for_extension(ext, LANG)
        else:
            target_folder_name = ext.lstrip('.') or ("no_extension" if LANG == "EN" else "uzantısız")

        target_folder = os.path.join(folder, target_folder_name)
        os.makedirs(target_folder, exist_ok=True)

        dest = Path(target_folder) / filename
        counter = 1
        while dest.exists():
            dest = Path(target_folder) / f"{dest.stem}_{counter}{dest.suffix}"
            counter += 1

        try:
            shutil.move(file_path, dest)
            moved_count += 1
            if gui_widget and (idx % 50 == 0 or idx == total_files):
                # GUI'de sadece belli aralıklarla veya sonda ACTION log yaz
                log(f"{filename} → {target_folder_name} (Moved {moved_count}/{total_files})", level="ACTION", gui_widget=gui_widget)

        except Exception as e:
            error_count += 1
            log(f"Could not move {filename}: {e}", level="ERROR", gui_widget=gui_widget)
            if gui_widget:
                messagebox.showerror(MESSAGES[LANG]["error_title"], f"{filename} taşınamadı: {e}")

        # İlerleme çubuğu güncellemesi
        progress_value = idx / total_files
        if progress_bar_widget:
            progress_bar_widget.set(progress_value)
            # GUI'nin güncellenmesini zorla (görsel akıcılık için kritik)
            progress_bar_widget.master.update_idletasks()
        
        # İlerleme çubuğu sadece CLI'da gösterilsin (GUI_widget yoksa)
        if not gui_widget:
            progress = int(progress_value * 30)
            bar = "█" * progress + "-" * (30 - progress)
            print(f"\r[{bar}] {idx}/{total_files} files moved/attempted", end="", flush=True)

    if not gui_widget:
        print() # CLI progress bar satır sonu

    log_msg("sorting_complete", level="INFO", gui_widget=gui_widget)
    log_msg("files_moved", moved_count, level="INFO", gui_widget=gui_widget)
    log_msg("errors", error_count, level="INFO", gui_widget=gui_widget)
    log_msg("skipped", len(all_items) - len(files), level="INFO", gui_widget=gui_widget)
    
    # İşlem bitince progress barı tam (1.0) yap
    if progress_bar_widget:
        progress_bar_widget.set(1.0)


# -------------------------
# GUI
# -------------------------
def run_gui():
    choose_language()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title(f"File Sorter v{__version__}")
    root.geometry("600x480") # Progress bar için biraz yer açıldı
    root.resizable(False, False)

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

    include_var = ctk.BooleanVar(value=False)
    include_cb = ctk.CTkCheckBox(root, text=MESSAGES[LANG]["include_subfolders"], variable=include_var)
    include_cb.pack(pady=(5, 5), padx=20, anchor="w")

    category_var = ctk.BooleanVar(value=True)
    category_cb = ctk.CTkCheckBox(root, text=MESSAGES[LANG]["use_categories"], variable=category_var)
    category_cb.pack(pady=(0, 10), padx=20, anchor="w")

    # YENİ EKLEME: İlerleme Çubuğu Widget'ı
    progress_bar = ctk.CTkProgressBar(root, orientation="horizontal")
    progress_bar.set(0) # Başlangıç değeri
    progress_bar.pack(pady=(0, 15), padx=20, fill="x")

    log_frame = ctk.CTkFrame(root)
    log_text = ctk.CTkTextbox(log_frame, width=560, height=150)
    log_text.pack(fill="both", expand=True)

    def sort_files_gui():
        folder = entry_folder.get()
        if not folder:
            messagebox.showwarning(MESSAGES[LANG]["error_title"], MESSAGES[LANG]["select_folder_error"])
            return
            
        # Önceden bulunan dosyaları temizle ve progress barı sıfırla
        log_text.delete("1.0", "end") 
        progress_bar.set(0)

        include_subfolders = include_var.get()
        use_categories = category_var.get()
        confirm = messagebox.askyesno(MESSAGES[LANG]["confirm_title"], MESSAGES[LANG]["confirm_gui_sort"])
        
        if confirm:
            log_frame.pack(pady=5, padx=20, fill="both", expand=True)
            # Progress bar'ı parametre olarak gönder
            move_files_with_progress(folder, include_subfolders, use_categories, gui_widget=log_text, progress_bar_widget=progress_bar)
            messagebox.showinfo(MESSAGES[LANG]["result_title"], MESSAGES[LANG]["result_sorted"])

    sort_btn = ctk.CTkButton(root, text=MESSAGES[LANG]["sort_button"], command=sort_files_gui,
                             fg_color="white", text_color="black")
    sort_btn.pack(pady=(0, 10))

    footer = ctk.CTkLabel(root, text="made by mefkuz", fg_color=None, text_color="gray")
    footer.pack(side="bottom", anchor="e", padx=10, pady=5)

    root.mainloop()

# -------------------------
# CLI
# -------------------------
def run_cli():
    choose_language()
    
    # Klasör yolu ve seçenekleri al
    folder = input(MESSAGES[LANG]["enter_folder_path"]).strip()
    if not folder:
        log_msg("select_folder_error", level="ERROR")
        return
    
    if not os.path.exists(folder):
        log_msg("folder_not_found", folder, level="ERROR")
        return

    include_subfolders = input(MESSAGES[LANG]["include_subfolders_cli"]).strip().lower() in ("y", "e")
    use_categories = input(MESSAGES[LANG]["use_categories_cli"]).strip().lower() in ("y", "e")

    # Dosya istatistiklerini topla
    all_items, files, extensions = get_file_stats(folder, include_subfolders)

    if not files:
        log_msg("no_files", level="INFO")
        return

    # Uzantıları okunabilir hale getir
    ext_list = "\n".join([f"  .{ext}: {count}" for ext, count in extensions.items()])
    
    # Onay mesajını hazırla
    confirm_message = MESSAGES[LANG]["confirm_text"].format(
        len(all_items), 
        len(files),     
        ext_list        
    )

    # Onay iste
    print("-" * 50)
    print(confirm_message)
    confirmation = input(MESSAGES[LANG]["proceed_confirmation"]).strip().lower()

    # Onayı kontrol et ('y' veya 'e' kabul)
    if confirmation in ["y", "e"]:
        # İşleme devam et
        print("-" * 50)
        # CLI'da progress bar widget'ı göndermeye gerek yok
        move_files_with_progress(folder, include_subfolders, use_categories) 
        print("-" * 50)
    else:
        # İptal et
        log_msg("sorting_canceled", level="INFO")

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        run_cli()
    else:
        run_gui()