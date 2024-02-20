from .value.value import Value

class SymbolTable:
    def __init__(self, parent = None):
        self.symbols: dict[str, Value] = {}
        self.immutable_symbols: dict[str, Value] = {}
        self.temporary_symbols: dict[str, (Value, int)] = {}
        
        #self.scoped_symbols: dict[str, Value] = {} # For Now Unused
        
        self.parent: SymbolTable = parent
    
    def exists(self, name: str):
        if name in self.symbols:
            return True
        elif name in self.immutable_symbols:
            return True
        elif name in self.temporary_symbols:
            return True
        
        return False
    
    def copy(self):
        copy = SymbolTable()
        self.parent = self
        return copy
    
    def get(self, name: str):
        if name in self.symbols:
            value = self.symbols.get(name, None)
        elif name in self.immutable_symbols:
            value = self.immutable_symbols.get(name, None)
        elif name in self.temporary_symbols:
            value = self.temporary_symbols.get(name, None)[0]
            new_lifetime = self.temporary_symbols[name][1] - 1 or 0
            self.set_as_temp(name, value, new_lifetime)
        else:
            value = None
            
        if value is None and self.parent:
            return self.parent.get(name)
                
        return value
    
    def set(self, name: str, value: Value):
        if name not in self.immutable_symbols:
            self.symbols[name] = value
            return True
        else:
            return False

    def set_as_immutable(self, name: str, value: Value):
        if name not in self.immutable_symbols:
            self.immutable_symbols[name] = value
            return True
        else:
            return False
        
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
        if name not in self.immutable_symbols:
            self.scoped_symbols[name] = value
            return True
        else:
            return False
        
    def remove(self, name: str):
        if name in self.symbols:
            del self.symbols[name]
        elif name in self.immutable_symbols:
            del self.immutable_symbols[name]
        elif name in self.temporary_symbols:
            del self.temporary_symbols[name]