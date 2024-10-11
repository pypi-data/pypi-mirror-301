from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree, Static, Label, Button, LoadingIndicator
from textual.screen import Screen, ModalScreen
from textual.containers import Container, Horizontal, VerticalScroll, Grid



class Confirm_Screen(ModalScreen[bool]):
    CSS_PATH = "css_lib/cofirm_screen.tcss"

    def __init__(self, message:str):
        self.message = message
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Grid(
            Static(self.message, id="question"),
            Button("Cancel", id="cancel", variant="error"),
            Button("OK", id="ok", variant="success")
            ,id="confirmscreen"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            self.dismiss(True)
        else:
            self.dismiss(False)