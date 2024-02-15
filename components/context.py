from .symbol_table import SymbolTable

class Context:
    def __init__(self, display_name: str, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table: SymbolTable = None
        
    def __repr__(self) -> str:
        return f"<Context:{self.display_name}, Parent:{self.parent}>"
        
