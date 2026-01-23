# 🎨 SVG Master Pro

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt-6.0+-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-important?style=for-the-badge)](#)

[한국어 문서 (README_ko.md)](./README_ko.md)

**SVG Master Pro** is a powerful and intuitive vector graphics editing tool based on Python (PyQt6). Easily import complex SVG files to edit individual elements, group them, and extract specific parts for saving.

Experience professional SVG editing with an elegant dark mode interface.

---

## ✨ Key Features

*   **📂 Perfect SVG Compatibility**: Powered by the `svgelements` engine to accurately parse and render complex SVG paths and attributes.
*   **🖼️ Intuitive Canvas**: High-performance canvas supporting grid systems, mouse drag movement, and wheel zoom/pan.
*   **📦 Smart Group Management**:
    *   Group multiple objects together (`Ctrl+G`)
    *   Ungroup for individual modifications (`Ctrl+U`)
*   **🎨 Real-time Style Editing**: Change fill colors of selected elements instantly and preview them.
*   **📤 Powerful Export System**:
    *   **Export Selected**: Save only specific objects as separate SVG files.
    *   **Bulk Split Export**: Automatically decompose entire designs into individual component files (`Name_1.svg`, `Name_2.svg`...).
*   **🔍 Flexible Visualization**: Precision editing with zoom in/out (`Ctrl++`, `Ctrl+-`) and fit-to-screen (`Ctrl+0`) functions.
*   **🖱️ Convenient Context Menu**: Quick access to all major functions via right-click.

## 📦 Distribution (GitHub Releases)

This project automatically builds single executables for **Linux, Windows, and macOS** via GitHub Actions.
Download the appropriate file for your OS from the Releases page to run immediately without installation.
Also available as a Docker image via `ghcr.io`.

---

## 🛠️ Installation & Execution

Python 3.12 or higher is recommended.

### 1. Environment Setup

Open a terminal, navigate to the project directory, and use the provided script for easy execution.

```bash
# Navigate to project folder
cd svgedit/app

# Grant execution permission (first time only)
chmod +x run.sh

# Run program
./run.sh
```

### 2. Manual Installation (For Developers)

To set up a virtual environment manually:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install PyQt6 svgelements lxml

# Run
python main.py
```

## 🎮 Usage Guide

| Action | Shortcut / Method | Description |
| :--- | :--- | :--- |
| **Move** | Mouse Drag | Freely move selected objects. |
| **Multi-select** | `Ctrl` + Click | Select multiple objects simultaneously. |
| **Pan** | Middle-click Drag | Move the canvas view (panning). |
| **Group** | `Ctrl` + `G` | Group selected objects into one. |
| **Ungroup** | `Ctrl` + `U` | Separate a selected group into individual elements. |
| **Delete** | `Delete` | Remove selected elements from the canvas. |
| **Context Menu** | Right-click | Call the editing menu. |

---

## 📝 License

This project is distributed under the **GNU GPL v3** license. See the [LICENSE](./LICENSE) file for more details.

Copyright (c) 2026 Rhee Works.
