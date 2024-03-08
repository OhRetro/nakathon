from .utils.debug import DebugMessage
from .position import Position
from .symbol_table import SymbolTable

context_count = 0
debug_message = DebugMessage("")

class Context:
    def __init__(self, display_name: str, parent = None, parent_entry_pos: Position = None):
        global context_count
        self.id = context_count
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table: SymbolTable = None
        
        context_count += 1
        debug_message.set_message(f"CONTEXT {self.id}: CREATED: {self.display_name}").display()
        
    def merge(self, other):
        self.symbol_table.merge(other.symbol_table)

    def import_from(self, other, namespace: str):
        symbols_list = [
            "symbols",
            "immutable_symbols"
        ]
        
        for symbols in symbols_list:
            for k, v in getattr(other.symbol_table, symbols).items():
                getattr(self.symbol_table, symbols)[f"{namespace}_{k}"] = v
                
    def __repr__(self) -> str:
        return f"<Context:{self.display_name}, Parent:{self.parent}>"
        