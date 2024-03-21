from .Value import Value
from ..node import VarAccessNode, CallNode

#! Code from the Radon Project, I will do my own implementation, using as a reference
class Instance(Value):
    def __init__(self, parent_class, symbol_table):
        self.parent_class = parent_class
        self.symbol_table = symbol_table
        super().__init__()

    #! LEFTOVER OF OLD METHOD, STILL HERE FOR REFERENCING
    def dotted(self, other: VarAccessNode | CallNode):
        return self.parent_class.dotted(other)
        
    def copy(self):
        copy = Instance(self.parent_class, self.symbol_table)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"<Instance:{self.parent_class}>"
