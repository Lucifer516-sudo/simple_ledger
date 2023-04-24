from kivy.app import App
from kivy.uix.button import Button
from simple_ledger import ledger_logger


ledger_logger.debug("Ledger UI: In the App Instance")


class Main(App):
    def build(self):
        return Button(text="Pls Click Me ... ")


App().run()
