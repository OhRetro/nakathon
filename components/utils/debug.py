import logging

logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.DEBUG)

class DebugMessage:
    def __init__(self, message: str, enable: bool = 0, auto_display_on_message_set: bool = False, filename: str = __file__):
        self.filename = filename.replace("\\", "/").split("/")[-1]
        self.set_auto_display(auto_display_on_message_set)
        self.set_enabled(enable)
        self.set_message(message)
        
    def display(self):
        if not self.enabled: return
        logging.log(logging.DEBUG, f"[{self.filename}]: {self.message}")
        return self.message
        
    def set_message(self, message):
        self.message = message
        if self.auto_display: self.display()
        return self
    
    def set_enabled(self, enabled):
        self.enabled = enabled
        return self
    
    def set_auto_display(self, enabled):
        self.auto_display = enabled
        return self
    

