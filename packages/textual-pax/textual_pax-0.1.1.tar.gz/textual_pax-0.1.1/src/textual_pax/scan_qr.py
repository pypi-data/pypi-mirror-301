from textual.screen import Screen
from textual.widgets import Static, Input, Header, Footer
from textual import events, on, work
from textual.app import ComposeResult
from .confmscn import Confirm_Screen
from .revertpaxmodule import apiPaxFunctions
from .functionsScreen import FunctionsScreen

class Scan_qr(Screen):
    """QR SCANNER"""
    BINDINGS = [("escape", "app.pop_screen", "BACK")]

    def compose(self) -> ComposeResult:
        yield Static("PlEASE SCAN QR CODE TO BEGIN", classes="question" )
        yield Input(placeholder=">>>>")
        yield Footer()
    @on(Input.Submitted)
    @work
    async def fix_qr(self) -> None:
        self.l = self.query_one(Input).value
        self.disabled = True
        self.serialNoList = eval(self.l)  # Assuming the QR code contains a list of serial numbers
        if await self.app.push_screen_wait(Confirm_Screen(f"Are these terminals you wish to activate\n{self.serialNoList}?")):
            self.notify("Activating>>>")
            
            apifun = apiPaxFunctions() 
            """self.thing = await apifun.startPaxGroup(self.serialNoList)
            self.thing2 = await apifun.disableTerminals(self.thing['id'])
            self.app.notify(str(self.thing2))
            self.thing3 = await apifun.deleteTerminals(self.thing['id'])
            self.thing4 = await apifun.createTerminals(self.serialNoList)
            self.app.notify(str(self.thing4))"""
            if await self.app.push_screen_wait(Confirm_Screen("Please ensure network connection & open PaxStore on device")):
                self.thing5 = await apifun.startPaxGroup(self.seria)
                self.app.push_screen(FunctionsScreen(self.thing5))

