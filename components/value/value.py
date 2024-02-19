from ..utils.debug import DebugMessage
from ..utils.error_messages import illegal_operation, no_method_defined
from typing import Any

class Value:
   
    def __init__(self, value: Any = None):
        self.value = value
        self.set_pos()
        self.set_context()
        
        DebugMessage(f"Created {self}").display()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context = None):
        self.context = context
        return self

    def added_to(self, other):
        return self.illegal_operation(other)

    def subbed_by(self, other):
        return self.illegal_operation(other)

    def multed_by(self, other):
        return self.illegal_operation(other)

    def dived_by(self, other):
        return self.illegal_operation(other)

    def powed_by(self, other):
        return self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return self.illegal_operation(other)

    def anded_by(self, other):
        return self.illegal_operation(other)

    def ored_by(self, other):
        return self.illegal_operation(other)

    def notted(self, other):
        return self.illegal_operation(other)

    def execute(self, args):
        from ..runtime import RunTimeResult
        return RunTimeResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception(no_method_defined.format("copy"))

    def is_true(self):
        return False

    def illegal_operation_error(self, other = None):
        from ..error import RunTimeError
        if not other: other = self
        return RunTimeError(
            self.pos_start, other.pos_end,
            illegal_operation,
            self.context
        )
    
    def illegal_operation(self, other = None):
        if not other: other = self
        return None, self.illegal_operation_error(other)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.value}>"
