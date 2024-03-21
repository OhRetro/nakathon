from .Value import Value
from .Number import Number
from ..token import TokenType

class String(Value):
    def __init__(self, value: str):
        super().__init__(value)
        
    def added_to(self, other: Value):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        
        return self._illegal_operation(other)

    def multed_by(self, other: Value):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        
        return self._illegal_operation(other)
      
    def is_true(self):
        return self.value != ""
    
    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __print_repr__(self) -> str:
        return self.value

    def __repr__(self):
        return f"{TokenType.STRING.value}{self.value}{TokenType.STRING.value}"
