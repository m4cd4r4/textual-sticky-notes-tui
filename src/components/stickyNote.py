from textual.widgets import Static
from textual.reactive import reactive
from models import Note

class StickyNote(Static):
    can_focus = True
    note: Note 
    color = reactive("white")
    user_color = reactive(None) 
    priority_level = reactive(0)
    is_pinned = reactive(False,init=False)

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

    def __init__(self, note: Note, **kwargs):
        super().__init__(**kwargs)
        self.note = note
        self.priority_level = note.priority
        self.is_pinned = note.pinned

    def on_mount(self, event):
        self.update_title()
        self.update_border_color()

    def compose(self):
        yield Static(self.note.content, id="noteContent")

    def update_title(self):
        """Update border title with pin and priority indicators"""
        pin_icon = "📌 " if self.is_pinned else ""
        priority_name = self.PRIORITY_NAMES.get(self.priority_level, "")
        priority_icon = self.get_priority_icon()
        
        self.border_title = f"{pin_icon}{self.note.noteTitle} {priority_icon}"

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