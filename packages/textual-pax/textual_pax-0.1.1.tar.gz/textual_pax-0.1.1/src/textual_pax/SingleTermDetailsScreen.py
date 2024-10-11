from textual.widgets import MarkdownViewer, Label, Button, Footer, Header
from textual.app import App, ComposeResult
from textual.screen import Screen, ModalScreen
from textual.binding import Binding
from textual.widgets import Footer

def update_table(appdata):
        headers = "| ".join(appdata[0].keys()) + " \n| --------------- | --------------- | --------------- | --------------- | --------------- |"
        rows = "\n|".join(["|".join(str(value) for value in item.values()) + "|" for item in appdata])
        content = f"## Installed Applications\n\n|{headers} \n|{rows}"
        return content

def format_terminal_details(termDetails:dict, appdata:list):

    text = ""
    text += "## Basic Info\n\n"
    for key, value in termDetails.items():
        if key == "serialNo":
            text += f"**Serial No:** {value}\n"
    for key, value in termDetails.items(): 
            if key !="serialNo":
                text += f"* {key}: {value}\n"
    text += update_table(appdata) 
    return text

class TerminalDetailsScreen(Screen):
    
    BINDINGS = [("escape", "app.pop_screen", "BACK")]
    
    def __init__(self,details:tuple):

        self.termdetails = details[0]
        self.appdata = details[1]
        self.markdown = format_terminal_details(*self.termdetails,self.appdata)

        super().__init__()

    def compose(self)-> ComposeResult:
        yield Header(name='PaxTools')
        yield MarkdownViewer(markdown=self.markdown,show_table_of_contents= True)
        yield Footer()

class TerminalDetailsApp(App):
    def on_mount(self) -> None:
        self.push_screen(TerminalDetailsScreen())

if __name__ == "__main__":
    app = TerminalDetailsApp()
    app.run()
