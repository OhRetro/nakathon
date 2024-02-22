from .utils.debug import DebugMessage
from .position import Position
from .symbol_table import SymbolTable

context_count = 0

class Context:
    def __init__(self, display_name: str, parent= None, parent_entry_pos: Position = None):
        global context_count
        self.id = context_count
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table: SymbolTable = None
        
        context_count += 1
        DebugMessage(f"CONTEXT {self.id}: CREATED: {self.display_name}").display()
        
    def __repr__(self) -> str:
        return f"<Context:{self.display_name}, Parent:{self.parent}>"
        
