import json
import os
from pathlib import Path
from typing import List
from models import Note
import platform

class NoteStorage:    
    def __init__(self, filename: str = "notes.json"):
        if platform.system() == "Linux":
            # XDG Base Directory Specification
            xdg_data_home = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share'))
            self.storage_dir = xdg_data_home / 'sticky-notes'
        elif platform.system() == "Darwin":  # macOS
            self.storage_dir = Path.home() / 'Library' / 'Application Support' / 'StickyNotes'
        else:  # Windows
            app_data = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
            self.storage_dir = app_data / 'StickyNotes'
        
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.filepath = self.storage_dir / filename
    
    def save_notes(self, notes_with_colors: List[tuple]) -> bool:
        try:
            notes_data = []
            for note, color in notes_with_colors:
                notes_data.append({
                    'noteTitle': note.noteTitle,
                    'content': note.content,
                    'tags': note.tags,
                    'priority': note.priority,
                    'pinned': note.pinned,
                    'note_id': note.note_id,
                    'color': color
                })
            
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(notes_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving notes: {e}")
            return False
    
    def load_notes(self) -> List[tuple]:
        try:
            if not self.filepath.exists():
                return []
            
            with open(self.filepath, 'r', encoding='utf-8') as f:
                notes_data = json.load(f)
            
            notes_with_colors = []
            for data in notes_data:
                note = Note(
                    noteTitle=data.get('noteTitle', ''),
                    content=data.get('content', ''),
                    tags=data.get('tags', ''),
                    priority=data.get('priority', 0),
                    pinned=data.get('pinned', False),
                    note_id=data.get('note_id', '')
                )
                color = data.get('color', 'white')
                notes_with_colors.append((note, color))
            
            return notes_with_colors
        except Exception as e:
            print(f"Error loading notes: {e}")
            return []