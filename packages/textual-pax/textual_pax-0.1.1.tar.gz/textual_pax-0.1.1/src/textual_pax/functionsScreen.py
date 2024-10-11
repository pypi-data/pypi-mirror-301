import pandas as pd
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual import events, on, work
from .DFTable import DataFrameTable
from .revertpaxmodule import apiPaxFunctions, PushConfigs, terminalDetails
from .ti_labels_iccid import create_pdf
from textual.containers import Container, VerticalScroll
from .confmscn import Confirm_Screen
from .singleTerminal import parseList
from .SingleTermDetailsScreen import TerminalDetailsScreen

class FunctionsScreen(Screen):

    CSS_PATH = "css_lib/group_gunctions.tcss"


    def __init__(self, df:pd.DataFrame) -> None:
        self.df = df
        self.button_list = [
            {'name':'Activate Group','id':'activate','classes':'gtask-buttons'},
            {'name':'Get Terminal Detials','id':'details ','classes':'gtask-buttons'},
            {'name':'Deactivate','id':'deactivate','classes':'gtask-buttons'},
            {'name':'Move Terminals', 'id':'move', 'classes':'gtask-buttons'},
            {'name':'Delete Group', 'id':'delete', 'classes':'gtask-buttons'},
            {'name':'Create Ticket Labels', 'id':'labels', 'classes':'gtask-buttons'}
        ]
        self.op = apiPaxFunctions()
        self.pepe = PushConfigs()
        self.operations = {
            "activate": self.op.activateTerminals,
            "details": terminalDetails,
            "deactivate": self.op.disableTerminals, 
            "move": None,
            "delete": self.op.deleteTerminals,
            "labels": create_pdf,
            "payanywhere": self.pepe.pushPAConfig,
            "broadpos":self.pepe.pushBroadPosEPX,
            "other": self.pepe.pushBroadPos_nonEPX
        }

        
        self.functionDict = {}
        super().__init__()
    
    def compose(self) -> ComposeResult:

        with Container(id="app-grid"):
            with VerticalScroll(id = "top-pane"):
                yield DataFrameTable()
            with VerticalScroll(id = "bottom-left"):
                yield Static("Available Tasks", classes="titleheader")
                yield Button("Activate Group", id="activate", classes="gtask-buttons")
                yield Button("Get Terminal Details", id = "details", classes="gtask-buttons")
                yield Button("Dectivate Group", id="deactivate",classes="gtask-buttons")
                yield Button("Move Terminals", id="move", classes="gtask-buttons")
                yield Button("Delete Group", id ="delete", classes="gtask-buttons")
                yield Button("Create Labels", id="labels", classes="gtask-buttons")
            with VerticalScroll(id= "bottom-right"):
                yield Static("Configuration Tasks", classes="titleheader")
                yield Button("Config for PayAnywhere", id="payanywhere", classes="buttons")
                yield Button("Config for BroadPOS - EPX", id="broadpos",classes="buttons")
                yield Button("Config for BroadPOS - Not EPX", id ="other", classes="buttons")
            
    async def on_mount(self):   
        """if self.df == None:
            self.mdf = pd.read_pickle("/Users/scottjamnik/python-to-google-sheets/E600M04.29.2024.14.051.pkl")
        else: self.mdf = pd.DataFrame(self.df)"""

        self.table = self.query_one(DataFrameTable)
        self.table.add_df(self.df)
        self.app.notify(str(self.df))
        self.df.to_pickle("df.pkl")

    
    @on(Button.Pressed)
    @work
    async def do_stuff(self, event: Button.Pressed):
        operation = self.operations.get(event.button.id)  # type: ignore
        result = await operation(idList = self.df['id'], serialNoList = self.df['serialNo'], df = self.df)  # type: ignore
        self.notify(str(result))
        if event.button.id == "details":
            self.ndf = pd.DataFrame(result)
            self.cdf = pd.concat([self.df,self.ndf], axis=1)
            self.table.update_df(self.cdf)
    
    @on(DataFrameTable.CellSelected)
    async def note_cell(self, event:DataFrameTable.CellSelected):
        if event.value in self.df['serialNo'].values:
            self.app.notify(str(event.value))
            if await self.app.push_screen_wait(Confirm_Screen(message=f"View {event.value} Terminal Page?")):
                dList = [event.value]
                termDetails = await parseList(dList)
                self.app.notify(str(termDetails))
                self.app.push_screen(TerminalDetailsScreen(termDetails))