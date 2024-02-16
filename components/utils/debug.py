import logging

enable = False

class DebugMessage:
    def __init__(self, message: str):
        self.message = message
        self.enabled = enable
        
    def display(self):
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG if self.enabled else logging.INFO)
        logging.log(logging.DEBUG, self.message)

    def set_message(self, message):
        self.message = message
        return self

