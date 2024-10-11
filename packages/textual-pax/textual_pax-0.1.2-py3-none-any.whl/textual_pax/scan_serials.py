from textual.screen import Screen
from textual.app import App, ComposeResult

from textual.widgets import Static, Input
from textual import events, on, work
import pandas as pd
from .revertpaxmodule import apiPaxFunctions  # Assuming this is in the same directory
from .confmscn import Confirm_Screen  # Assuming this is in the same directory
from .functionsScreen import FunctionsScreen

class Scan_serials(Screen):

    """SERIAL NUMBER INPUT"""

    def __init__(self):

        self.serialNoList = []
        super().__init__()
    
    def compose(self) -> ComposeResult:
        yield Static("PlEASE SCAN OR TYPE SERIAL NUMBER:", classes="question" )
        yield Input(placeholder="S/N")

    @on(Input.Submitted)
    @work
    async def update_serial_list(self):
        user_input = self.query_one(Input)
        serialNo = user_input.value
        self.serialNoList.append(str(serialNo))
        self.mount(Static(serialNo))
        if user_input.value == "0000":
            self.disabled = True
            self.serialNoList.pop()
            #self.notify(str(self.serial_list))
            df = pd.DataFrame({"serialNo":self.serialNoList},dtype='object')
            if await self.app.push_screen_wait(Confirm_Screen(f"Are these terminals you wish to activate\n{self.serialNoList}?")):
                self.notify("Activating>>>")
                apifun = apiPaxFunctions() 
                self.thing = await apifun.startPaxGroup(self.serialNoList)
                self.thing2 = await apifun.disableTerminals(self.thing['id'])
                self.app.notify(str(self.thing2))
                self.thing3 = await apifun.deleteTerminals(self.thing['id'])
                self.thing4 = await apifun.createTerminals(self.serialNoList)
                self.app.notify(str(self.thing4))
                if await self.app.push_screen_wait(Confirm_Screen("Please ensure network connection & open PaxStore on device")):
                    self.thing5 = await apifun.startPaxGroup(self.serialNoList)
                    self.app.push_screen(FunctionsScreen(self.thing5))
            user_input.clear()

