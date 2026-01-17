import copy
from textual.screen import ModalScreen
from textual.widgets import TextArea, OptionList, Checkbox, Label, Button, Input, Static
from textual.containers import HorizontalGroup, ScrollableContainer
from textual.widgets.option_list import Option
from pathlib import Path

from models import Note

class EditModal(ModalScreen[Note]):
    BINDINGS = [("escape", "dismiss", "Close")]

    note: Note
    oldNote: Note

    def __init__(self, note: Note, **kwargs):
        self.note = note
        self.oldNote = copy.deepcopy(note)
        super().__init__(**kwargs)

    def compose(self):
        with ScrollableContainer(id="editModalContainer"):
            yield Label("Enter title")
            yield TextArea(text=self.note.noteTitle, id="title")

            yield Label("Enter Content")
            yield TextArea(text=self.note.content, id="content")

            yield Label("Enter tags")
            yield Input(value=self.note.tags, id="tags")

            yield Label("Priority")
            option_list = OptionList(
                Option("⚪ Trivial", id="0"),
                Option("🔵 Low", id="1"),
                Option("🟡 Medium", id="2"),
                Option("🟠 High", id="3"),
                Option("🔴 Critical", id="4"),
                id="priority"
            )
            if 0 <= self.note.priority <= 4:
                option_list.highlighted = self.note.priority
            yield option_list

            yield Checkbox("📌 Pinned", value=self.note.pinned, id="pinned")

            # Display attachments if any
            if hasattr(self.note, 'attachments') and self.note.attachments:
                yield Label(f"\n📎 Attachments ({len(self.note.attachments)}):")
                for attachment in self.note.attachments:
                    icon = self.get_file_icon(attachment)
                    name = Path(attachment).name
                    size = self.get_file_size_str(attachment)
                    yield Static(f"{icon} {name} ({size})", classes="attachment-display")

            # Display timestamps (read-only)
            if hasattr(self.note, 'created_at') and self.note.created_at:
                from datetime import datetime
                try:
                    created_dt = datetime.fromisoformat(self.note.created_at)
                    created_str = created_dt.strftime("%b %d, %Y at %I:%M %p")
                    yield Static(f"\n📅 Created: {created_str}", classes="timestamp-info")
                except:
                    pass

            if hasattr(self.note, 'updated_at') and self.note.updated_at:
                try:
                    from datetime import datetime
                    updated_dt = datetime.fromisoformat(self.note.updated_at)
                    updated_str = updated_dt.strftime("%b %d, %Y at %I:%M %p")
                    yield Static(f"⏱️  Updated: {updated_str}", classes="timestamp-info")
                except:
                    pass

            with HorizontalGroup():
                yield Button("Save", variant="success", id="save")
                yield Button("Cancel", variant="primary", id="cancel")

        return super().compose()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.note.noteTitle = self.query_one("#title", TextArea).text
            self.note.content = self.query_one("#content", TextArea).text
            self.note.tags = self.query_one("#tags", Input).value
            self.note.pinned = self.query_one("#pinned", Checkbox).value

            priority_list = self.query_one("#priority", OptionList)
            if priority_list.highlighted is not None:
                self.note.priority = int(priority_list.get_option_at_index(priority_list.highlighted).id)

            # Update timestamp on save
            if hasattr(self.note, 'updated_at'):
                from datetime import datetime
                self.note.updated_at = datetime.now().isoformat()

            self.dismiss(self.note)
        else:
            self.dismiss(self.oldNote)

    def action_dismiss(self):
        self.dismiss()

    def get_file_icon(self, filepath):
        """Get emoji icon based on file type"""
        if not filepath:
            return "📎"

        ext = Path(filepath).suffix.lower()

        if ext in ['.pdf']:
            return "📄"
        elif ext in ['.doc', '.docx', '.txt', '.rtf']:
            return "📝"
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
            return "🖼️"
        elif ext in ['.xlsx', '.xls', '.csv']:
            return "📊"
        elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return "📦"
        elif ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h']:
            return "💻"
        else:
            return "📎"

    def get_file_size_str(self, filepath):
        """Get human-readable file size"""
        try:
            path = Path(filepath)
            if not path.exists():
                return "?"

            size = path.stat().st_size

            for unit in ['B', 'KB', 'MB']:
                if size < 1024.0:
                    return f"{size:.1f}{unit}"
                size /= 1024.0
            return f"{size:.1f}GB"
        except:
            return "?"
