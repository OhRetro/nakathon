from .utils.debug import DebugMessage
from .datatypes.value import Value

debug_message = DebugMessage("").set_auto_display(True)
symbol_table_count = 0

class SymbolTable:
    def __init__(self, parent = None):
        global symbol_table_count
        self.id = symbol_table_count
        
        self.symbols: dict[str, (Value, Value)] = {}
        self.immutable_symbols: dict[str, (Value, Value)] = {}
        self.temporary_symbols: dict[str, (Value, Value, int)] = {}
        self.scoped_symbols: dict[str, (Value, Value)] = {}
        
        self.parent: SymbolTable = parent
        
        symbol_table_count += 1
        debug_message.set_message(f"ST {self.id}: CREATED")
        
    def merge(self, other):
        symbols_list = [
            "symbols",
            "immutable_symbols"
        ]
        
        for symbols in symbols_list:
            for k, v in getattr(other, symbols).items():
                getattr(self, symbols)[k] = v

    def _exists(self, name: str, symbols_name: str, extra_condition: bool = True):
        return name in getattr(self, symbols_name) and extra_condition

    def exists_in(self, name: str, calling_from_parent: bool = False):
        debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': CHECKING SYMBOL TYPE")
        symbol_table_name = None
        
        if name in self.symbols:
            symbol_table_name = "symbols"
        elif name in self.immutable_symbols:
            symbol_table_name = "immutable_symbols"
        elif name in self.temporary_symbols:
            symbol_table_name = "temporary_symbols"
        elif name in self.scoped_symbols and not calling_from_parent:
            symbol_table_name = "scoped_symbols"
            
        if symbol_table_name is None and self.parent:
            symbol_table_name = self.parent.exists_in(name, True)
            
        return symbol_table_name
            
    def exists(self, name: str, calling_from_parent: bool = False):
        exists = False
        if not calling_from_parent: debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': EXISTS: CHECKING")

        symbols_list = [
            ("symbols", 1),
            ("immutable_symbols", 1),
            ("temporary_symbols", 1),
            ("scoped_symbols", not calling_from_parent)
        ]
        
        for symbols in symbols_list:
            exists = self._exists(name, symbols[0], symbols[1])
            if exists: break
            
        if not exists and self.parent:
            debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': EXISTS: CHECKING IN PARENT ST {self.parent.id}")
            exists = self.parent.exists(name, True)
        
        if not calling_from_parent: debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': EXISTS: {exists}")
        return exists

    def _is_immutable_check(self, name: str):
        exists = self._exists(name, "immutable_symbols")
        
        if not exists and self.parent:
            exists = self.parent._is_immutable_check(name)
        
        return exists
    
    def get(self, name: str, calling_from_parent: bool = False):
        if not calling_from_parent: debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': GET: CHECKING")
        value = self.symbols.get(name, [None])[0]
        
        if value is None:
            if name in self.immutable_symbols:
                value = self.immutable_symbols.get(name, [None])[0]
            
            elif name in self.temporary_symbols:
                value = self.temporary_symbols.get(name, [None])[0]
                type = self.temporary_symbols.get(name, [None])[1]
                
                if value is not None:
                    new_lifetime = self.temporary_symbols[name][2] - 1 or 0
                    self.set_as_temporary(name, value, type, new_lifetime)
                    
            elif name in self.scoped_symbols and not calling_from_parent:
                value = self.scoped_symbols.get(name, [None])[0]

            if value is None and self.parent:
                debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': GET: CHECKING IN PARENT ST {self.parent.id}")
                value = self.parent.get(name, True)
                
        return value
    
    def _set_symbol(self, name: str, value: Value, type: Value, symbols_name: str, **kwargs):
        success = False
        fail_type = "const"
        debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': SET: CHECKING")
        
        if self._exists(name, symbols_name):
            current_type = getattr(self, symbols_name)[name][1]

            if type != current_type:
                fail_type = "type"
        
        if not self._is_immutable_check(name) and fail_type == "const":
            if symbols_name.startswith("temp"):
                lifetime = kwargs.get("lifetime", 0)
                if not self._exists(name, symbols_name):
                    if lifetime > 0:
                        getattr(self, symbols_name)[name] = (value, type, lifetime+1)
                        success =  True
                else:
                    if lifetime <= 0: self.remove(name)
                    else:
                        getattr(self, symbols_name)[name] = (value, type, lifetime)
                        success = True
            else:
                getattr(self, symbols_name)[name] = (value, type)
                success = True
                
        debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': SET: SUCCESSFUL: {success}")
        return success, fail_type
   
    def set(self, name: str, value: Value, type: Value):
        return self._set_symbol(name, value, type, "symbols")

    def set_as_immutable(self, name: str, value: Value, type: Value):
        return self._set_symbol(name, value, type, "immutable_symbols")
        
    def set_as_temporary(self, name: str, value: Value, type: Value, lifetime: int):
        return self._set_symbol(name, value, type, "temporary_symbols", lifetime = lifetime)
        
    def set_as_scoped(self, name: str, value: Value, type: Value):
        return self._set_symbol(name, value, type, "scoped_symbols")
        
    def remove(self, name: str):
        debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': DELETE")
        if name in self.symbols:
            del self.symbols[name]
        elif name in self.immutable_symbols:
            del self.immutable_symbols[name]
        elif name in self.temporary_symbols:
            del self.temporary_symbols[name]
        elif name in self.scoped_symbols:
            del self.scoped_symbols[name]
            
    def copy(self):
        copy = SymbolTable(self)
        return copy
            