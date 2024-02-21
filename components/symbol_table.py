from .utils.debug import DebugMessage
from .value.value import Value

debug_message = DebugMessage("", 0, 1)
symbol_table_count = 0

class SymbolTable:
    def __init__(self, parent = None):
        global symbol_table_count
        self.id = symbol_table_count
        self.symbols: dict[str, Value] = {}
        self.immutable_symbols: dict[str, Value] = {}
        self.temporary_symbols: dict[str, (Value, int)] = {}
        self.scoped_symbols: dict[str, Value] = {}
        
        self.parent: SymbolTable = parent
        self.is_child = True if self.parent else False
        symbol_table_count += 1
    
    def _exists(self, name: str, symbols_name: str, extra_condition: bool = True):
        return name in getattr(self, symbols_name) and extra_condition
    
    def exists(self, name: str):
        exists = False
        debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': EXISTS: CHECKING")

        symbols_list = [
            ("symbols", 1),
            ("immutable_symbols", 1),
            ("temporary_symbols", 1),
            ("scoped_symbols", not self.is_child)
        ]
        
        for symbols in symbols_list:
            exists = self._exists(name, symbols[0], symbols[1])
            if exists: break
            
        if not exists and self.parent:
            debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': EXISTS: CHECKING IN PARENT ST {self.parent.id}")
            exists = self.parent.exists(name)
        
        debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': EXISTS: {exists}")
        return exists

    def _is_immutable_check(self, name: str):
        exists = self._exists(name, "immutable_symbols")
        
        if not exists and self.parent:
            exists = self.parent._is_immutable_check(name)
        
        return exists
    
    def get(self, name: str):
        debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': GET: CHECKING")
        value = self.symbols.get(name, None)
        
        if value is None:
            if name in self.immutable_symbols:
                value = self.immutable_symbols.get(name, None)
            
            elif name in self.temporary_symbols:
                value = self.temporary_symbols.get(name, [None])[0]
                
                if value is not None:
                    new_lifetime = self.temporary_symbols[name][1] - 1 or 0
                    self.set_as_temp(name, value, new_lifetime)
                    
            elif name in self.scoped_symbols and not self.is_child:
                value = self.scoped_symbols.get(name, None)

            if value is None and self.parent:
                debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': GET: CHECKING IN PARENT ST {self.parent.id}")
                value = self.parent.get(name)
                
        return value
    

    def _set_symbol(self, name: str, value: Value, symbol_name: str, **kwargs):
        success = False
        debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': SET: CHECKING")
        
        if not self._is_immutable_check(name):
            if symbol_name.startswith("temp"):
                lifetime = kwargs.get("lifetime", 0)
                if not self._exists(name, symbol_name):
                    if lifetime > 0:
                        getattr(self, symbol_name)[name] = (value, lifetime+1)
                        success =  True
                else:
                    if lifetime <= 0: self.remove(name)
                    else:
                        getattr(self, symbol_name)[name] = (value, lifetime)
                        success = True
            else:
                getattr(self, symbol_name)[name] = value
                success = True

        debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': SET: SUCCESSFUL: {success}")
        return success
   
    def set(self, name: str, value: Value):
        return self._set_symbol(name, value, "symbols")

    def set_as_immutable(self, name: str, value: Value):
        return self._set_symbol(name, value, "immutable_symbols")
        
    def set_as_temp(self, name: str, value: Value, lifetime: int):
        return self._set_symbol(name, value, "temporary_symbols", lifetime = lifetime)
        
    def set_as_scoped(self, name: str, value: Value):
        return self._set_symbol(name, value, "scoped_symbols")
        
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
        copy = SymbolTable()
        copy.parent = self
        return copy
            