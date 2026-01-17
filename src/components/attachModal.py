"""
Modal for adding file attachments to notes
"""
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Container, Vertical
from textual.widgets import Button, Static, Input, Label
from pathlib import Path

class AttachModal(ModalScreen):
    """Modal screen for attaching files"""

    def __init__(self, note_id: str):
        super().__init__()
        self.note_id = note_id
        self.file_path = None

    def compose(self) -> ComposeResult:
        with Container(id="attach-modal"):
            with Vertical():
                yield Static("📎 Attach File (Max 10MB)", id="attach-title")
                yield Static("", id="attach-instructions")
                yield Label("File Path:")
                yield Input(
                    placeholder="Enter full path to file or drag & drop",
                    id="file-path-input"
                )
                yield Static("", id="file-info")
                with Container(id="attach-buttons"):
                    yield Button("Attach", variant="success", id="attach-button")
                    yield Button("Cancel", variant="default", id="cancel-attach")

    def on_mount(self) -> None:
        """Focus the input when modal opens"""
        self.query_one("#file-path-input").focus()
        instructions = self.query_one("#attach-instructions")
        instructions.update("Paste the full path to a file you want to attach.\n"
                          "Supported: Images, PDFs, documents, etc.")

    def on_input_changed(self, event: Input.Changed) -> None:
        """Update file info as user types"""
        if event.input.id == "file-path-input":
            path_str = event.value.strip().strip('"')  # Remove quotes if pasted
            if path_str:
                self._update_file_info(path_str)
            else:
                self.query_one("#file-info").update("")

    def _update_file_info(self, path_str: str) -> None:
        """Update file information display"""
        from file_utils import validate_file, format_file_size

        path = Path(path_str)
        info_widget = self.query_one("#file-info")

        if not path.exists():
            info_widget.update("❌ File not found")
            return

        if not path.is_file():
            info_widget.update("❌ Not a file")
            return

        is_valid, error = validate_file(path_str)
        if not is_valid:
            info_widget.update(f"❌ {error}")
            return

        size = path.stat().st_size
        size_str = format_file_size(size)
        info_widget.update(f"✅ {path.name} ({size_str})")
        self.file_path = path_str

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "attach-button":
            if self.file_path:
                self.dismiss(self.file_path)
            else:
                path_input = self.query_one("#file-path-input")
                path_str = path_input.value.strip().strip('"')
                if path_str:
                    self.file_path = path_str
                    self.dismiss(self.file_path)
                else:
                    info_widget = self.query_one("#file-info")
                    info_widget.update("❌ Please enter a file path")
        elif event.button.id == "cancel-attach":
            self.dismiss(None)
