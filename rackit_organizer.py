#!/usr/bin/env python3
import os
import re
import shutil
import zipfile
import subprocess
import platform
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk

# ------------------------------
# Default patterns
# ------------------------------
default_patterns = [
    r"^(20\d{2})(0[1-9]|1[0-2])\d{2}_\d+",      # YYYYMMDD_HHMMSS
    r"^IMG_(20\d{2})(0[1-9]|1[0-2])\d{2}.*"    # IMG_YYYYMMDD_...
]

month_names = {
    "01": "jan", "02": "feb", "03": "mar", "04": "apr",
    "05": "may", "06": "jun", "07": "jul", "08": "aug",
    "09": "sep", "10": "oct", "11": "nov", "12": "dec"
}

# Supported media extensions
media_exts = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".heic",
              ".mp4", ".mov", ".avi", ".3gp", ".mkv"]

# ------------------------------
# Organize a single file
# ------------------------------
def organize_file(file_path, target_folder, patterns, move_files=False):
    filename = file_path.name
    year = "others"
    month = "others"

    for pattern in patterns:
        m = re.match(pattern, filename)
        if m:
            year = m.group(1)
            month = month_names.get(m.group(2), "others")
            break

    year_folder = Path(target_folder) / year
    month_folder = year_folder / month
    month_folder.mkdir(parents=True, exist_ok=True)

    dest = month_folder / filename
    if move_files:
        shutil.move(str(file_path), str(dest))
    else:
        shutil.copy2(str(file_path), str(dest))

# ------------------------------
# Organize folder with progress
# ------------------------------
def organize_folder(root_folder, output_folder, patterns, progress_var, move_files=False, only_media=True):
    all_files = [f for f in Path(root_folder).rglob("*") if f.is_file()]

    # Filter only media if checkbox is checked
    if only_media:
        all_files = [f for f in all_files if f.suffix.lower() in media_exts]

    total = len(all_files)
    if total == 0:
        messagebox.showwarning("No files", "No files to organize!")
        return

    progress_var.set(0)
    progress_bar.update()

    for idx, file in enumerate(all_files, 1):
        organize_file(file, output_folder, patterns, move_files)
        progress_var.set(int((idx / total) * 100))
        progress_bar.update()
    
    # Optional: remove non-media files from temp folder if only_media
    if only_media:
        for f in Path(root_folder).rglob("*"):
            if f.is_file() and f.suffix.lower() not in media_exts:
                try:
                    f.unlink()
                except:
                    pass

# ------------------------------
# Extract multiple ZIPs
# ------------------------------
def extract_zips(zip_paths):
    temp_folder = Path(zip_paths[0]).parent / "rackit_temp_extracted"
    temp_folder.mkdir(exist_ok=True)
    for zip_path in zip_paths:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_folder)
    return temp_folder

# ------------------------------
# Open folder cross-platform
# ------------------------------
def open_folder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", path])
    else:  # Linux
        subprocess.Popen(["xdg-open", path])

# ------------------------------
# Browse multiple ZIP files
# ------------------------------
def browse_zips():
    browse_btn.config(state="disabled")  # disable after choosing files
    zip_paths = filedialog.askopenfilenames(
        title="Select Google Takeout ZIP files",
        filetypes=[("ZIP files", "*.zip")]
    )
    if not zip_paths:
        browse_btn.config(state="normal")
        return

    zip_paths = [Path(p) for p in zip_paths]

    # Extract all ZIPs
    root_folder = extract_zips(zip_paths)

    # Ask for additional patterns
    user_patterns_str = simpledialog.askstring(
        "Patterns",
        "Enter additional regex patterns separated by comma (or leave empty to use defaults):"
    )
    user_patterns = []
    if user_patterns_str:
        user_patterns = [p.strip() for p in user_patterns_str.split(",")]

    all_patterns = default_patterns + user_patterns

    # Output folder
    output_folder = Path(zip_paths[0]).parent / "rackit_organized"

    if output_folder.exists():
        proceed = messagebox.askokcancel("Folder Exists", f"{output_folder} already exists. Proceed and overwrite?")
        if not proceed:
            root.destroy()
            return
    else:
        output_folder.mkdir(exist_ok=True)

    # Move or copy
    move_files_choice = messagebox.askyesno("Move or Copy", "Do you want to move files instead of copying?")

    # Only organize media?
    only_media_choice = media_checkbox_var.get()

    # Organize files with progress
    organize_folder(root_folder, output_folder, all_patterns, progress_var,
                    move_files=move_files_choice, only_media=only_media_choice)

    # Open folder
    open_folder(output_folder)

    # Done
    messagebox.showinfo("Done", f"All files organized in: {output_folder}")
    root.destroy()  # close GUI automatically

# ------------------------------
# GUI Setup
# ------------------------------
root = tk.Tk()
root.title("RackIt Organizer")
root.geometry("600x320")

# Instructions / Example patterns
instructions = ("Example Patterns:\n"
                "1. 20191202_112505.jpg → YYYYMMDD_HHMMSS\n"
                "2. IMG_20181230_084218805_2.jpg → IMG_YYYYMMDD_...\n"
                "You can add additional regex patterns below (comma-separated).")
label = tk.Label(root, text=instructions, bg="lightyellow", justify="left", padx=10, pady=10)
label.pack(expand=False, fill="x", padx=20, pady=5)

# Browse button
browse_btn = tk.Button(root, text="Browse ZIP files", command=browse_zips, padx=10, pady=5)
browse_btn.pack(pady=5)

# Checkbox: Only organize media files
media_checkbox_var = tk.BooleanVar(value=True)
media_checkbox = tk.Checkbutton(root, text="Ignore non-media files (e.g., JSON) and organize only photos/videos",
                                variable=media_checkbox_var)
media_checkbox.pack(pady=5)

# Progress bar
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, length=550, variable=progress_var, maximum=100)
progress_bar.pack(pady=10)

root.mainloop()

