from .value.value import Value

class SymbolTable:
    def __init__(self, parent = None):
        self.symbols: dict[str, Value] = {}
        self.immutable_symbols: dict[str, Value] = {}
        self.parent: SymbolTable = parent
        
    def get(self, name: str):
        value = self.symbols.get(name, None)
        
        if value is None and self.parent:
            return self.parent.get(name)
        
        elif value is None and self.parent is None:
            if name in self.immutable_symbols:
                value = self.immutable_symbols.get(name)
                
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
        
    def remove(self, name: str):
        del self.symbols[name]