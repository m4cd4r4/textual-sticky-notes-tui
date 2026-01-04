from textual.screen import ModalScreen
from textual.widgets import Static,TextArea,OptionList,Checkbox,Label,Button
from textual.containers import Grid

class DeleteModal(ModalScreen[bool]):
    BINDINGS = [("escape", "dismiss", "Close")] 

     
    
    def compose(self):
        with Grid(id="deleteModalContainer"):
            yield Label("You are deleting this note!",id="question")
  
            yield Button("YES",variant="error",id="yes")
            yield Button("NO","primary",id="no")

        return super().compose()

    def on_button_pressed(self, event: Button.Pressed) -> None:
            if event.button.id == "yes":
                self.dismiss(True)  
            else:
                self.dismiss(False) 

    def action_dismiss(self):
        self.dismiss()