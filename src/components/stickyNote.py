from textual.widgets import Static
from textual.reactive import reactive
from models import Note
from datetime import datetime
from pathlib import Path

class StickyNote(Static):
    can_focus = True
    note: Note
    color = reactive("white")
    user_color = reactive(None)
    priority_level = reactive(0)
    is_pinned = reactive(False,init=False)
    show_timestamps = reactive(True)

    PRIORITY_COLORS = {
        0: "white",      # trivial
        1: "#a0c4ff",      # low
        2: "#fdffb6",    # medium
        3: "#ffd6a5",    # high
        4: "#ffadad"        # critical
    }

    PRIORITY_NAMES = {
        0: "Trivial",
        1: "Low",
        2: "Medium",
        3: "High",
        4: "Critical"
    }

    def __init__(self, note: Note, show_timestamps=True, **kwargs):
        super().__init__(**kwargs)
        self.note = note
        self.show_timestamps = show_timestamps
        self.priority_level = note.priority
        self.is_pinned = note.pinned

    def on_mount(self, event):
        self.update_title()
        self.update_border_color()

    def compose(self):
        # Main content
        yield Static(self.note.content, id="noteContent")

        # Show attachments if any
        if hasattr(self.note, 'attachments') and self.note.attachments:
            yield Static("", classes="attachment-divider")
            for attachment in self.note.attachments:
                icon = self.get_file_icon(attachment)
                name = Path(attachment).name
                size = self.get_file_size_str(attachment)
                yield Static(f"{icon} {name} ({size})",
                           classes="attachment-item")

    def update_title(self):
        """Update border title with pin, priority, and attachment indicators"""
        pin_icon = "📌 " if self.is_pinned else ""
        priority_icon = self.get_priority_icon()

        # Add attachment count indicator
        attachment_count = len(getattr(self.note, 'attachments', []))
        attach_icon = f" 📎{attachment_count}" if attachment_count > 0 else ""

        self.border_title = f"{pin_icon}{self.note.noteTitle} {priority_icon}{attach_icon}"

        # Add timestamp subtitle
        if self.show_timestamps and hasattr(self.note, 'created_at') and self.note.created_at:
            created = self.format_timestamp(self.note.created_at)
            updated = self.format_relative_time(self.note.updated_at) if hasattr(self.note, 'updated_at') else ""

            if updated:
                self.border_subtitle = f"📅 {created}  ⏱️  {updated}"
            else:
                self.border_subtitle = f"📅 {created}"

    def format_timestamp(self, iso_timestamp):
        """Format ISO timestamp to readable form"""
        if not iso_timestamp:
            return ""

        try:
            dt = datetime.fromisoformat(iso_timestamp)
            return dt.strftime("%b %d, %I:%M %p")
        except:
            return ""

    def format_relative_time(self, iso_timestamp):
        """Format timestamp as relative time (e.g., '2h ago')"""
        if not iso_timestamp:
            return ""

        try:
            dt = datetime.fromisoformat(iso_timestamp)
            now = datetime.now()
            diff = now - dt

            seconds = diff.total_seconds()

            if seconds < 60:
                return "just now"
            elif seconds < 3600:
                mins = int(seconds / 60)
                return f"{mins}m ago"
            elif seconds < 86400:
                hours = int(seconds / 3600)
                return f"{hours}h ago"
            elif seconds < 604800:
                days = int(seconds / 86400)
                return f"{days}d ago"
            elif seconds < 2592000:
                weeks = int(seconds / 604800)
                return f"{weeks}w ago"
            else:
                months = int(seconds / 2592000)
                return f"{months}mo ago"
        except:
            return ""

    def get_file_icon(self, filepath):
        """Get emoji icon based on file type"""
        if not filepath:
            return "📎"

        ext = Path(filepath).suffix.lower()

        # Documents
        if ext in ['.pdf']:
            return "📄"
        elif ext in ['.doc', '.docx', '.txt', '.rtf']:
            return "📝"

        # Images
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
            return "🖼️"

        # Spreadsheets
        elif ext in ['.xlsx', '.xls', '.csv']:
            return "📊"

        # Archives
        elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return "📦"

        # Code
        elif ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h']:
            return "💻"

        # Audio
        elif ext in ['.mp3', '.wav', '.ogg', '.m4a']:
            return "🎵"

        # Video
        elif ext in ['.mp4', '.avi', '.mkv', '.mov']:
            return "🎬"

        # Default
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

    def get_priority_icon(self):
        """Get icon based on priority level"""
        icons = {
            0: "",           # trivial  - no icon
            1: "🔵",         # low
            2: "🟡",         # medium
            3: "🟠",         # high
            4: "🔴"          # critical
        }
        return icons.get(self.priority_level, "")

    def update_border_color(self):
        if self.user_color is not None:
            self.color = self.user_color
        else:
            self.color = self.PRIORITY_COLORS.get(self.priority_level, "white")

    def watch_color(self, color: str):
        """React to color changes"""
        self.styles.border = ("heavy" if self.is_pinned else "solid", color)

    def watch_priority_level(self, priority: int):
        """React to priority changes"""
        self.note.priority = priority
        self.update_title()
        self.update_border_color()

    def watch_is_pinned(self, pinned: bool):
        """React to pin status changes"""
        self.note.pinned = pinned
        self.update_title()
        self.styles.border = ("heavy" if pinned else "solid", self.color)
