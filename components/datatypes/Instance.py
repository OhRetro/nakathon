from .Value import Value

#! Code from the Radon Project, I will do my own implementation, using as a reference
class Instance(Value):
    def __init__(self, parent_class):
        self.parent_class = parent_class
        self.symbol_table = None
        super().__init__()

    def copy(self):
        copy = Instance(self.parent_class)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"<Instance:{self.parent_class.name}>"
