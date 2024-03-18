from typing import Any
from .Value import Value

class Object(Value):
    def __init__(self, elements: list):
        super().__init__()
        self.elements = elements

    def copy(self):
        copy = Object(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return "object"

    def __repr__(self):
        return "placeholder"
