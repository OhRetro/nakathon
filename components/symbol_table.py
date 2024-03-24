from .utils.debug import DebugMessage
from .datatypes.Value import Value
from copy import deepcopy

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
        
        self.builtin_symbols: dict[str, (Value, Value)] = {}
        
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

    def copy_symbol(self, name: str):
        symbol_type_id = self.exists_in(name)
        
        if not symbol_type_id or symbol_type_id in {"temporary_symbols", "scoped_symbols"}: 
            # I don't know how to handle this situation properly
            return None
        
        return (self.get(name).copy(), self.get_type(name))

    def _exists(self, name: str, symbols_name: str, extra_condition: bool = True):
        return name in getattr(self, symbols_name) and extra_condition

    def exists_in(self, name: str, calling_from_parent: bool = False):
        debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': CHECKING SYMBOL TYPE")
        symbol_type_name = None
        symbol_table_inst = self
        
        if name in self.symbols:
            symbol_type_name = "symbols"
            
        elif name in self.immutable_symbols:
            symbol_type_name = "immutable_symbols"
            
        elif name in self.temporary_symbols and not calling_from_parent:
            symbol_type_name = "temporary_symbols"
            
        elif name in self.scoped_symbols and not calling_from_parent:
            symbol_type_name = "scoped_symbols"
            
        elif name in self.builtin_symbols:
            symbol_type_name = "builtin_symbols"
            
        if symbol_type_name is None and self.parent:
            symbol_type_name, symbol_table_inst = self.parent.exists_in(name, True)
            
        return symbol_type_name, symbol_table_inst
            
    def exists(self, name: str, calling_from_parent: bool = False) -> bool:
        exists = False
        if not calling_from_parent: debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': EXISTS: CHECKING")

        symbols_list = [
            ("symbols", 1),
            ("immutable_symbols", 1),
            ("temporary_symbols", 1),
            ("scoped_symbols", not calling_from_parent),
            ("builtin_symbols", 1)
        ]
        
        for symbols in symbols_list:
            exists = self._exists(name, symbols[0], symbols[1])
            if exists: break
            
        if not exists and self.parent:
            debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': EXISTS: CHECKING IN PARENT ST {self.parent.id}")
            exists = self.parent.exists(name, True)
        
        if not calling_from_parent: debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': EXISTS: {exists}")
        return exists

    def _is_immutable_or_builtin_check(self, name: str):
        exists = self._exists(name, "immutable_symbols") or self._exists(name, "builtin_symbols")
        
        if not exists and self.parent:
            exists = self.parent._is_immutable_or_builtin_check(name)
        
        return exists
    
    def _get(self, name: str, calling_from_parent: bool = False):
        if not calling_from_parent: debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': GET: CHECKING")
        value = self.symbols.get(name, [None])[0]
        type = self.symbols.get(name, [None, None])[1]
        
        if value is None:
            if name in self.immutable_symbols:
                value = self.immutable_symbols.get(name, [None])[0]
                type = self.immutable_symbols.get(name, [None, None])[1]
            
            elif name in self.temporary_symbols:
                value = self.temporary_symbols.get(name, [None])[0]
                type = self.temporary_symbols.get(name, [None, None])[1]
                
                if value is not None:
                    new_lifetime = self.temporary_symbols[name][2] - 1 or 0
                    self.set_as_temporary(name, value, type, new_lifetime)
                    
            elif name in self.scoped_symbols and not calling_from_parent:
                value = self.scoped_symbols.get(name, [None])[0]
                type = self.scoped_symbols.get(name, [None, None])[1]

            elif name in self.builtin_symbols:
                value = self.builtin_symbols.get(name, [None])[0]
                type = self.builtin_symbols.get(name, [None, None])[1]
                
            if value is None and self.parent:
                debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': GET: CHECKING IN PARENT ST {self.parent.id}")
                value = self.parent._get(name, True)[0]
                type = self.parent._get(name, True)[1]
                
        return value, type

    def get(self, name: str, calling_from_parent: bool = False) -> Value:
        return self._get(name, calling_from_parent)[0]
    
    def get_type(self, name: str, calling_from_parent: bool = False) -> Value:
        return self._get(name, calling_from_parent)[1]
    
    def _set_symbol(self, name: str, value: Value, type: Value, symbols_name: str, **kwargs):
        success = False
        fail_type = "const"
        debug_message.set_message(f"ST {self.id}: SYMBOL '{name}': SET: CHECKING")
        
        if self._exists(name, symbols_name):
            current_type = getattr(self, symbols_name)[name][1]
            if type != current_type:
                fail_type = "type"
        
        if not self._is_immutable_or_builtin_check(name) and fail_type == "const":
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

    def set_as_builtin(self, name: str, value: Value, type: Value):
        return self._set_symbol(name, value, type, "builtin_symbols")
        
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
        copy.symbols = self.symbols
        copy.immutable_symbols = self.immutable_symbols
        return copy
            