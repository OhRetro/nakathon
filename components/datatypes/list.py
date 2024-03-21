from .Value import Value
from .Number import Number
from ..token import TokenType
from ..error import RunTimeError
from ..utils.strings_template import OUT_OF_BOUNDS_ERROR

class List(Value):
    def __init__(self, elements: list):
        self.elements = elements
        super().__init__(elements)
        
    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RunTimeError(
                    other.pos_start, other.pos_end,
                    OUT_OF_BOUNDS_ERROR,
                    self.context
                )

        return self._illegal_operation(other)
        
    def multed_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        
        return self._illegal_operation(other)
      
    def dived_by(self, other):
        if isinstance(other, Number):            
            try:
                return self.elements[other.value], None
            except:
                return None, RunTimeError(
                    other.pos_start, other.pos_end,
                    OUT_OF_BOUNDS_ERROR,
                    self.context
                )
        
        return self._illegal_operation(other)
    
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __repr__(self):
        return f"{TokenType.LSQUARE.value}{', '.join([str(x) for x in self.elements])}{TokenType.RSQUARE.value}"
