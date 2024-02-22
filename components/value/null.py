from .value import Value


class Null(Value):
    def __init__(self):
        super().__init__(None)

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