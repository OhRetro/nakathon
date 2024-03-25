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
        self.parent: Context = parent
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
        
        for symbol in symbols_list:
            for k, v in getattr(other.symbol_table, symbol).items():
                self.symbol_table._set_symbol(f"{namespace}_{k}", v[0], v[1], symbol)
    
    def exists_in(self, name: str, calling_from_parent: bool = False):
        debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': CHECKING SYMBOL TYPE")
        symbol_type_name = None
        ctx_inst = self
        
        if name in self.symbol_table.symbols:
            symbol_type_name = "symbols"
            
        elif name in self.symbol_table.immutable_symbols:
            symbol_type_name = "immutable_symbols"
            
        elif name in self.symbol_table.temporary_symbols and not calling_from_parent:
            symbol_type_name = "temporary_symbols"
            
        elif name in self.symbol_table.scoped_symbols and not calling_from_parent:
            symbol_type_name = "scoped_symbols"
            
        elif name in self.symbol_table.builtin_symbols:
            symbol_type_name = "builtin_symbols"
            
        if symbol_type_name is None and self.parent:
            symbol_type_name, ctx_inst = self.parent.exists_in(name, True)
        
        return symbol_type_name, ctx_inst
    
    def __repr__(self) -> str:
        return f"<Context:{self.display_name}, Id:{self.id}, Parent:{self.parent}>"
        