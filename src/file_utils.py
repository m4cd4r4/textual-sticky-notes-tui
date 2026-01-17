"""
File utilities for handling attachments
"""
import shutil
import os
from pathlib import Path
from datetime import datetime
import platform

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def get_attachments_dir() -> Path:
    """Get the attachments storage directory"""
    if platform.system() == "Linux":
        xdg_data_home = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share'))
        storage_dir = xdg_data_home / 'sticky-notes'
    elif platform.system() == "Darwin":  # macOS
        storage_dir = Path.home() / 'Library' / 'Application Support' / 'StickyNotes'
    else:  # Windows
        app_data = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
        storage_dir = app_data / 'StickyNotes'

    attachments_dir = storage_dir / 'attachments'
    attachments_dir.mkdir(parents=True, exist_ok=True)
    return attachments_dir

def validate_file(file_path: str) -> tuple[bool, str]:
    """
    Validate file for attachment
    Returns: (is_valid, error_message)
    """
    path = Path(file_path)

    if not path.exists():
        return False, "File does not exist"

    if not path.is_file():
        return False, "Path is not a file"

    file_size = path.stat().st_size
    if file_size > MAX_FILE_SIZE:
        size_mb = file_size / (1024 * 1024)
        return False, f"File too large ({size_mb:.1f}MB). Maximum size is 10MB"

    if file_size == 0:
        return False, "File is empty"

    return True, ""

def copy_attachment(source_path: str, note_id: str) -> tuple[bool, str]:
    """
    Copy file to attachments directory
    Returns: (success, attachment_path_or_error)
    """
    is_valid, error = validate_file(source_path)
    if not is_valid:
        return False, error

    try:
        source = Path(source_path)
        attachments_dir = get_attachments_dir()

        # Create note-specific subdirectory
        note_dir = attachments_dir / note_id
        note_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_filename = f"{timestamp}_{source.name}"
        dest_path = note_dir / dest_filename

        # Copy file
        shutil.copy2(source, dest_path)

        return True, str(dest_path)
    except Exception as e:
        return False, f"Error copying file: {e}"

def delete_attachment(attachment_path: str) -> bool:
    """Delete an attachment file"""
    try:
        path = Path(attachment_path)
        if path.exists():
            path.unlink()
            # Try to remove parent directory if empty
            try:
                path.parent.rmdir()
            except OSError:
                pass  # Directory not empty, that's fine
        return True
    except Exception as e:
        print(f"Error deleting attachment: {e}")
        return False

def get_file_info(file_path: str) -> dict:
    """Get file information for display"""
    try:
        path = Path(file_path)
        if not path.exists():
            return {
                "name": Path(file_path).name,
                "size": "missing",
                "exists": False
            }

        size = path.stat().st_size
        size_str = format_file_size(size)

        return {
            "name": path.name,
            "size": size_str,
            "path": str(path),
            "exists": True
        }
    except Exception:
        return {
            "name": Path(file_path).name,
            "size": "error",
            "exists": False
        }

def format_file_size(bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB']:
        if bytes < 1024.0:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024.0
    return f"{bytes:.1f}GB"

def open_file(file_path: str) -> bool:
    """Open file with default system application"""
    try:
        path = Path(file_path)
        if not path.exists():
            return False

        if platform.system() == 'Windows':
            os.startfile(path)
        elif platform.system() == 'Darwin':  # macOS
            os.system(f'open "{path}"')
        else:  # Linux
            os.system(f'xdg-open "{path}"')
        return True
    except Exception as e:
        print(f"Error opening file: {e}")
        return False
