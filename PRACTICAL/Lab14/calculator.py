from js import document
from pyodide import create_proxy
from datetime import datetime

def getTime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")

class InputLog():
    def __init__(self, element_id):
        self.element_id = element_id
        self._element = None
        self.displayString = ""
        self.accpeted = ["0","1","2","3","4","5","6","7","8","9",".","+","-","*","/","(",")"]

    @property
    def element(self):
        """Return the dom element"""
        if not self._element:
            self._element = document.querySelector(f"#{self.element_id}")
        return self._element


    def on_event(self, event):
        if event.key == "<":
            self.displayString = self.displayString[:-1]
        elif event.key == "c":
            self.displayString = ""
        elif event.key == "=" or event.key == "Enter":
            # check if displayString contain "/0"?
            if "/0" in self.displayString:
                self.element.innerHTML = "Infinity"
                return
                
            self.element.innerHTML = str(eval(self.displayString))
            self.displayString = self.element.innerHTML
            return
        elif event.key in self.accpeted:
            self.displayString += event.key
        else:
            return
        self.element.innerHTML = self.displayString
    
output = InputLog("result")

event_proxy = create_proxy(output.on_event)

document.addEventListener("keydown", event_proxy)