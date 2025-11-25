# RackIt Organizer

RackIt Organizer is a **cross-platform Python GUI tool** to organize your Google Photos Takeout files (or any collection of photos/videos) into **Year → Month** folders automatically. It supports multiple ZIP files, handles various file name patterns, and can optionally ignore non-media files like JSON.  

This tool is perfect for cleaning up messy photo/video exports from Google Takeout or similar sources, making them easy to browse and manage.

---

## Features

- Automatically organizes photos and videos into **Year → Month** folders based on filename patterns.
- Supports **default patterns**:
  - `YYYYMMDD_HHMMSS` (e.g., `20191202_112505.jpg`)
  - `IMG_YYYYMMDD_...` (e.g., `IMG_20181230_084218805_2.jpg`)
- Users can **add custom regex patterns** for file names.
- Organize files by **copying or moving**.
- Supports **multiple Google Takeout ZIP files** at once.
- Optional **checkbox** to ignore non-media files (e.g., JSON).
- **Progress bar** shows organizing progress.
- Warns if the output folder already exists.
- Automatically **opens the organized output folder** when done.
- Fully **dependency-free GUI** using `tkinter`.

---

## Requirements

- Python 3.x
- Cross-platform: Windows, Linux, macOS
- No additional Python libraries required (all standard libraries used)

---

## Installation

1. Clone this repository or download the Python script:

```bash
git clone https://github.com/yourusername/rackit-organizer.git
cd rackit-organizer
