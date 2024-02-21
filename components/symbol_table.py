from .utils.debug import DebugMessage
from .value.value import Value

debug_message = DebugMessage("", 0, 1)

class SymbolTable:
    def __init__(self, parent = None):
        self.symbols: dict[str, Value] = {}
        self.immutable_symbols: dict[str, Value] = {}
        self.temporary_symbols: dict[str, (Value, int)] = {}
        self.scoped_symbols: dict[str, Value] = {} # WIP
        
        self.parent: SymbolTable = parent
        self.is_child = True if self.parent else False
    
    def exists(self, name: str):
        exists = False
        debug_message.set_message(f"Checking if symbol '{name}' exists")
        
        if name in self.symbols:
            exists = True
        elif name in self.immutable_symbols:
            exists = True
        elif name in self.temporary_symbols:
            exists = True
        elif name in self.scoped_symbols and not self.is_child:
            exists = True
            
        if not exists:
            exists = self.parent.exists(name)
        
        debug_message.set_message(f"Symbol '{name}' exists? {exists}")
        return exists
    
    def copy(self):
        copy = SymbolTable()
        copy.parent = self
        return copy
    
    def get(self, name: str):
        debug_message.set_message(f"Getting the symbol '{name}'")
        debug_message.set_message(f"Checking '{name}' in symbols")
        value = self.symbols.get(name, None)
        
        if value is None and name in self.immutable_symbols:
            debug_message.set_message(f"Checking '{name}' in immutable_symbols")
            value = self.immutable_symbols.get(name, None)
        
        elif value is None and name in self.temporary_symbols:
            debug_message.set_message(f"Checking '{name}' in temporary_symbols")
            value = self.temporary_symbols.get(name, None)[0]
            
            if value is not None:
                new_lifetime = self.temporary_symbols[name][1] - 1 or 0
                self.set_as_temp(name, value, new_lifetime)
                
        elif value is None and name in self.scoped_symbols and not self.is_child:
            debug_message.set_message(f"Checking '{name}' in scoped_symbols")
            value = self.scoped_symbols.get(name, None)

        if value is None and self.parent:
            debug_message.set_message(f"Not present for this symbol table for '{name}', Getting from parent")
            value = self.parent.get(name)
                
        return value
    
    def _set_check(self, name: str, extra_condition: bool = True):
        dont_exists = name not in self.immutable_symbols and extra_condition
        return dont_exists
    
    def _set_symbol(self, name: str, value: Value, symbol_name: str, extra_condition: bool = True):
        debug_message.set_message(f"Setting symbol '{name}'")
        immutable_of_same_name_dont_exists = self._set_check(name, extra_condition)
        if immutable_of_same_name_dont_exists:
            getattr(self, symbol_name)[name] = value

        debug_message.set_message(f"Setting symbol '{name}' successful? {immutable_of_same_name_dont_exists}")
        return immutable_of_same_name_dont_exists 
   
    def set(self, name: str, value: Value):
        return self._set_symbol(name, value, "symbols")

    def set_as_immutable(self, name: str, value: Value):
        return self._set_symbol(name, value, "immutable_symbols")
        
    def set_as_temp(self, name: str, value: Value, lifetime: int):
        if name not in self.immutable_symbols and name not in self.temporary_symbols:
            if lifetime <= 0: return False
            self.temporary_symbols[name] = (value, lifetime+1)
            return True
        
        else:
            if lifetime <= 0:
                self.remove(name)
                return False
            
            self.temporary_symbols[name] = (value, lifetime)
            return True
        
    def set_as_scoped(self, name: str, value: Value):
        return self._set_symbol(name, value, "scoped_symbols")
        
    def remove(self, name: str):
        if name in self.symbols:
            del self.symbols[name]
        elif name in self.immutable_symbols:
            del self.immutable_symbols[name]
        elif name in self.temporary_symbols:
            del self.temporary_symbols[name]
        elif name in self.scoped_symbols:
            del self.scoped_symbols[name]