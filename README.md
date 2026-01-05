# Sticky Notes TUI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Textual](https://img.shields.io/badge/Textual-TUI-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**Sticky Notes TUI** is a modern, keyboard-centric terminal-based application designed to manage your thoughts, tasks, and reminders efficiently. Built with Textual, it offers a seamless graphical experience directly within your console, featuring rich colors, priority management, and persistent storage.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage & Keybindings](#usage--keybindings)
- [Priority & Organization](#priority--organization)
- [Configuration & Storage](#configuration--storage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Features

* **Keyboard-First Navigation:** Navigate, create, edit, and delete notes without ever leaving your keyboard.
* **Rich Color Coding:** Organize notes visually using 9 distinct colors with simple hotkeys.
* **Priority Management:** Assign 5 levels of priority (from Trivial to Critical) with visual indicators.
* **Pinning System:** Pin important notes to keep them highlighted and distinguished.
* **Advanced Search:** Filter notes instantly by title, content, or tags via a dedicated modal.
* **Persistent Storage:** Automatically saves your notes to your OS-specific application data directory (supports Linux, macOS, and Windows).
* **Dark/Light Mode:** Toggle between themes to suit your environment.
* **Responsive Layout:** Grid layout automatically adjusts columns based on your terminal width.

---
#GIF
![Demo](assets/tutorial.gif)

## Installation

### Prerequisites

- Python 3.8 or higher
- A terminal emulator with TrueColor support (most modern terminals support this).

### Steps

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/sticky-notes-tui.git](https://github.com/yourusername/sticky-notes-tui.git)
    cd sticky-notes-tui
    ```

2.  **Set up a Virtual Environment (Recommended)**
    ```bash
    python -m venv .venv
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install textual
    ```

4.  **Run the Application**
    ```bash
    python main.py
    ```

---

## Usage & Keybindings

Once the application is running, you can use the following keys to interact with the interface.

### Global Controls

| Key | Action | Description |
| :--- | :--- | :--- |
| **`a`** | **Add Note** | Create a new sticky note. |
| **`e`** | **Edit Note** | Edit the content, title, priority, or pin status of the focused note. |
| **`r`** | **Remove Note** | Delete the currently focused note (triggers a confirmation modal). |
| **`s`** | **Search** | Open the search modal to find specific notes. |
| **`o`** | **Sort** | Sort notes automatically (Pinned first, then by Priority). |
| **`d`** | **Toggle Theme** | Switch between Dark and Light mode. |
| **`Ctrl+s`** | **Save** | Manually force save to disk. |
| **`Ctrl+c`** | **Quit** | Force quit the application. |

### Navigation

| Key | Action |
| :--- | :--- |
| **`Arrow Keys`** | Move focus between notes (Left, Right, Up, Down). |

### Styling (When a note is focused)

| Key | Action |
| :--- | :--- |
| **`1` - `9`** | Change the border color of the selected note. |

---

## Priority & Organization

Sticky Notes TUI allows you to categorize the urgency of your tasks. When editing a note (`e`), you can select one of the following levels:

1.  **Trivial** (Default)
2.  **Low**
3.  **Medium**
4.  **High**
5.  **Critical**

### Icons & Visuals
Notes display visual icons corresponding to their priority level and pin status.
* **Pinned Notes:** Display a heavier border and a pin icon in the title.
* **Priority Icons:** Higher priorities display distinct glyphs in the header.

---

## Configuration & Storage

The application uses an intelligent storage system that respects your operating system's standards. You do not need to configure anything; it just works.

**Data Location:**
* **Linux:** `~/.local/share/sticky-notes/notes.json` (XDG Base Directory)
* **macOS:** `~/Library/Application Support/StickyNotes/notes.json`
* **Windows:** `%APPDATA%\StickyNotes\notes.json`

The data is saved in a human-readable JSON format, allowing for easy backup or manual inspection if necessary.

---

## Project Structure

```text
sticky-notes-tui/
├── app.py                  # Main application logic (StickyNotesApp)
├── main.py                 # Entry point
├── models.py               # Data models (Note class)
├── storage.py              # JSON storage handler (Cross-platform)
├── style.css               # Textual CSS styling
└── components/             # UI Components
    ├── stickyNote.py       # Individual Note widget
    ├── editModal.py        # Edit/Create popup
    ├── searchModal.py      # Search functionality
    └── deleteModal.py      # Confirmation popup
```


