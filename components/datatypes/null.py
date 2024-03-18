from .Value import Value
from .Boolean import Boolean

class Null(Value):
    def __init__(self):
        super().__init__(None)

    def get_comparison_eq(self, other):
        if isinstance(other, Value):
            return Boolean(self.value == other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def get_comparison_ne(self, other):
        if isinstance(other, Value):
            return Boolean(self.value != other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def anded_by(self, other):
        if isinstance(other, Value):
            return Boolean(self.value and other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def ored_by(self, other):
        if isinstance(other, Value):
            return Boolean(self.value or other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def notted(self):
        return Boolean(True if self.value != None else False).set_context(self.context), None
    
    def copy(self):
        copy = Null()
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
      
    def __int__(self):
        return -1

    def __str__(self):
        return "null"
    
    def __repr__(self):
        return self.__str__()

Null.null = Null()