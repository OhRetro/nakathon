from .value import Value


class Boolean(Value):
    def __init__(self, value: bool):
        super().__init__(value)
    
    def __int__(self):
        return int(self.value)

    def __bool__(self):
        return bool(self.value)
    
    def __str__(self):
        return str(self.value).lower()

    def anded_by(self, other):
        if isinstance(other, Boolean):
            return Boolean(self.value and other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def ored_by(self, other):
        if isinstance(other, Boolean):
            return Boolean(self.value or other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def notted(self):
        return Boolean(True if self.value == 0 else False).set_context(self.context), None

    def is_true(self):
        return self.value is True
    
    def notted(self, other):
        return Boolean(True if self.value == 0 else False).set_context(self.context), None

    def copy(self):
        copy = Boolean(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __repr__(self):
        return self.__str__()

Boolean.false = Boolean(False) 
Boolean.true = Boolean(True)
