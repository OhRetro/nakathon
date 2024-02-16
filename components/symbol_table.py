class SymbolTable:
    def __init__(self, parent = None, immutable_symbols: dict = {}):
        self.symbols = {}
        self.immutable_symbols = immutable_symbols
        self.parent: SymbolTable = parent
        
    def get(self, name):
        value = self.symbols.get(name, None)
        
        if value is None and self.parent:
            return self.parent.get(name)
        
        elif value is None and self.parent is None:
            if name in self.immutable_symbols:
                value = self.immutable_symbols.get(name)
                
        return value
    
    def set(self, name, value):
        if name not in self.immutable_symbols:
            self.symbols[name] = value
            return True
        else:
            return False
        
    def remove(self, name):
        del self.symbols[name]