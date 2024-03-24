from .Value import Value
from ..node import VarAccessNode, CallNode

class Instance(Value):
    def __init__(self, parent_class, symbol_table):
        self.parent_class = parent_class
        self.symbol_table = symbol_table
        super().__init__(parent_class)

    def dotted(self, other: VarAccessNode | CallNode):
        return self.parent_class.dotted(other)
        
    def copy(self):
        return self

    # def __repr__(self):
    #     return f"<Instance:{self.parent_class}>"
