from .value import Value
from .boolean import Boolean
from ..context import Context
from ..error import RunTimeError
from ..utils.error_messages import division_by_zero


class Number(Value):
    def __init__(self, value: int|float):
        super().__init__(value)

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context: Context = None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.pos_start, other.pos_end,
                    division_by_zero,
                    self.context
                )
            return Number(self.value / other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def rest_of_dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.pos_start, other.pos_end,
                    division_by_zero,
                    self.context
                )
            return Number(self.value % other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Boolean(self.value == other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Boolean(self.value != other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Boolean(self.value < other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Boolean(self.value > other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Boolean(self.value <= other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Boolean(self.value >= other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def anded_by(self, other):
        if isinstance(other, Number):
            return Boolean(self.value and other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def ored_by(self, other):
        if isinstance(other, Number):
            return Boolean(self.value or other.value).set_context(self.context), None
        
        return self.illegal_operation(other)

    def notted(self):
        return Boolean(True if self.value == 0 else False).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value)

