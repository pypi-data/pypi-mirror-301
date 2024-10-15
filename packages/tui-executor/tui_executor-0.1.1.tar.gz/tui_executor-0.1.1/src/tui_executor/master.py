from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer
from textual.widgets import Header


class MasterScreen(Screen):
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
