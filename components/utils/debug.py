import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class DebugMessage:
    def __init__(self, message: str, enable = False):
        self.set_message(message)
        self.set_enabled(enable)
        

    def display(self):
        if not self.enabled: return
        logging.log(logging.DEBUG, self.message)

    def set_message(self, message):
        self.message = message
        return self
    
    def set_enabled(self, enabled):
        self.enabled = enabled
        return self
    

