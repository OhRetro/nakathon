from logging import basicConfig, log, DEBUG
from inspect import currentframe as i_currentframe, getouterframes as i_getouterframes

basicConfig(format = "[%(levelname)s]: %(message)s", level = DEBUG, encoding = "utf-8")

DEFAULT_ENABLED = 1
ALL_USES_DEFAULT = 0

COMPONENTS_ENABLED = {
    "context.py": 0,
    "interpreter.py": 0,
    "node.py": 0,
    "parser.py": 0,
    "symbol_table.py": 0,
    "token.py": 0,
    "wrapper.py": 0,
    
    "function.py": 0,
    "value.py": 0
}

class DebugMessage:
    def __init__(self, message: str, auto_display_on_message_set: bool = False):
        curframe = i_currentframe()
        calframe = i_getouterframes(curframe, 2)
        self.caller = calframe[1][1].replace("\\", "/").split("/")[-1].lower()
        
        self.set_auto_display(auto_display_on_message_set)
        self.set_enabled(COMPONENTS_ENABLED.get(self.caller, DEFAULT_ENABLED) if not ALL_USES_DEFAULT else DEFAULT_ENABLED)
        self.set_message(message)
        
    def display(self):
        if not self.enabled: return
        curframe = i_currentframe()
        calframe = i_getouterframes(curframe, 2)
 
        log(DEBUG, f"[{self.caller}]: [{calframe[2][3]}]: {self.message}")
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
    

