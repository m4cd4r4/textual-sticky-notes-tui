from textual.screen import ModalScreen
from textual.widgets import Input, Button, ListView, ListItem, Label
from textual.containers import Vertical, Horizontal
from src.models import Note

class SearchModal(ModalScreen[Note]):
    """Search notes by title, content, or tags"""
    
    all_notes: list = []
    matching_notes: list = [] 
    
    def __init__(self, notes: list, **kwargs):
        self.all_notes = notes
        self.matching_notes = []
        super().__init__(**kwargs)
    
    def compose(self):
        with Vertical(id="searchContainer"):
            yield Label("🔍 Search Notes", id="searchTitle")
            yield Input(placeholder="Search by title, content, or tags...", id="searchInput")
            yield ListView(id="searchResults")
            with Horizontal(id="searchButtons"):
                yield Button("Close", variant="primary", id="close")
    
    def on_mount(self) -> None:
        """Focus input when modal opens"""
        self.query_one("#searchInput", Input).focus()
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Filter notes as user types"""
        search_term = event.value.lower().strip()
        results_view = self.query_one("#searchResults", ListView)
        
        # Clear previous results
        results_view.clear()
        self.matching_notes = []
        
        if not search_term:
            results_view.append(ListItem(Label("Type to search...")))
            return
        
        # Filter notes
        for note in self.all_notes:
            if (search_term in note.noteTitle.lower() or 
                search_term in note.content.lower() or 
                search_term in note.tags.lower()):
                self.matching_notes.append(note)
        
        # Display results
        if self.matching_notes:
            for note in self.matching_notes:
                preview = note.content[:50] + "..." if len(note.content) > 50 else note.content
                results_view.append(
                    ListItem(Label(f"📌 {note.noteTitle}\n   {preview}"))
                )
        else:
            results_view.append(ListItem(Label("❌ No notes found")))
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """When user clicks on a search result"""
        if event.list_view.index is not None:
            index = event.list_view.index
            if 0 <= index < len(self.matching_notes):
                selected_note = self.matching_notes[index]
                self.dismiss(selected_note)  # Return the selected note
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close":
            self.dismiss(None)  # Return None when closing