import copy
from dataclasses import replace
from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Header, Footer,Static
from textual.containers import ScrollableContainer
from textual import work
from components.deleteModal import DeleteModal
from components.editModal import EditModal
from components.searchModal import SearchModal
from components.stickyNote import StickyNote
from models import Note


class StickyNotesApp(App):
    """Basit bir Textual uygulaması."""
    column_count = 3;

    default_note:Note = Note("New title",content="New")

    BINDINGS = [("d", "toggle_dark_mode", "toggle dark mode"),
                ("right", "focus_next", "Next"),
                ("left", "focus_previous", "Prev"),
                ("up", "move_up", "Move Up"),
                ("down", "move_down", "Move Down"),
                ("a","add_note","add a new note"),
                ("r","delete_note","delete a note"),
                ("e","edit_note","edit a note"),
                ("1-9"," ","border color"),
                ("s","search_notes","search notes"),
                ("o", "sort_notes", "Sort notes") 
                ]
    CSS_PATH = "style.css"

    COLORS = {
        "1": "#ffadad", "2": "#ffd6a5", "3": "#fdffb6",
        "4": "#caffbf", "5": "#9bf6ff", "6": "#a0c4ff",
        "7": "#bdb2ff", "8": "#ffc6ff", "9": "#fffffc"
    }

    def on_key(self, event) -> None:
        if isinstance(self.screen, ModalScreen):
            return  

        if event.key in self.COLORS:
            focused_widget = self.screen.focused
            if isinstance(focused_widget, StickyNote):
                focused_widget.color = self.COLORS[event.key]

    def action_move_up(self):
        for _ in range(self.column_count):
            self.action_focus_previous()
    def action_move_down(self):
        for _ in range(self.column_count):
            self.action_focus_next()

    def compose(self) -> ComposeResult:
        yield Header()
        with ScrollableContainer(id="notes"):
            yield StickyNote(note=copy.deepcopy(self.default_note))
            yield StickyNote(note=copy.deepcopy(self.default_note))
        yield Footer()

    def action_toggle_dark_mode(self):
        self.action_toggle_dark()
    
    @work
    async def action_add_note(self):
        new_note = copy.deepcopy(self.default_note)
        stickyNote = StickyNote(note=new_note)
        container = self.query_one("#notes")
        container.mount(stickyNote)
        stickyNote.scroll_visible()

    def action_sort_notes(self):
        self.sort_notes()
        self.notify("Notes sorted!", severity="information")

    def sort_notes(self):
        """Sort notes: pinned first, then by priority"""
        container = self.query_one("#notes")
        notes = list(self.query(StickyNote))
        
        if not notes:
            return
        
        
        sorted_notes = sorted(notes, 
                            key=lambda n: (-n.is_pinned, -n.priority_level))
            
        
        for i, note in enumerate(sorted_notes):
            container.move_child(note, after=len(container.children) - 1)

    @work
    async def action_delete_note(self):
        focused_widget = self.screen.focused

        if focused_widget is not None and isinstance(focused_widget, StickyNote):
            confirm = await self.push_screen_wait(DeleteModal())
            if confirm:
                focused_widget.remove()

    @work
    async def action_edit_note(self):
        focused_widget = self.screen.focused
        if focused_widget is not None and isinstance(focused_widget, StickyNote):
            updatedNote = await self.push_screen_wait(EditModal(focused_widget.note))
            if updatedNote:
                focused_widget.note = updatedNote
                
                # Reactive properties'i güncelle
                focused_widget.priority_level = updatedNote.priority
                focused_widget.is_pinned = updatedNote.pinned
                
                # Border title'ı güncelle
                focused_widget.update_title()
                
                # Content'i güncelle
                content_widget = focused_widget.query_one("#noteContent")
                content_widget.update(updatedNote.content)

    @work
    async def action_search_notes(self):
        """Search through all notes"""
        # Tüm notları ve widget'larını topla
        all_notes = []
        note_widgets = {}
        
        for sticky_note in self.query(StickyNote):
            all_notes.append(sticky_note.note)
            # Note objesinin id'sini key olarak kullan
            note_widgets[id(sticky_note.note)] = sticky_note
        
        if not all_notes:
            self.notify("No notes to search!", severity="warning")
            return
        
        # Search modal'ını aç
        selected_note = await self.push_screen_wait(SearchModal(all_notes))
        
        # Eğer bir not seçildiyse
        if selected_note is not None:
            # Seçilen nota karşılık gelen widget'ı bul
            target_widget = note_widgets.get(id(selected_note))
            if target_widget:
                target_widget.focus()
                target_widget.scroll_visible()
                self.notify(f"Found: {selected_note.noteTitle}", severity="information")

    def _on_resize(self, event):
        notes_container = self.query_one("#notes")
        self.column_count = max(1,event.size.width//40)
        notes_container.styles.grid_size_columns = self.column_count
        return super()._on_resize(event)

