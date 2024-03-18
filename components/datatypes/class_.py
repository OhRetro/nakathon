from .value import Value
from ..node import ListNode, VarAccessNode, CallNode
from ..runtime import RunTimeResult
from ..context import Context
from ..symbol_table import SymbolTable

class Class(Value):
    def __init__(self, name: str, body_node: ListNode):
        self.name = name
        self.body_node = body_node
        self.symbol_table = None
        super().__init__(name)

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context
    
    # LEFTOVER OF OLD METHOD, STILL HERE FOR REFERENCING
    def dotted(self, other: VarAccessNode | CallNode):
        from ..interpreter import Interpreter

        res = RunTimeResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()
        
        if isinstance(other, VarAccessNode):
            value: Value = res.register(interpreter.visit(self.body_node, exec_ctx))

            class_symbol_name = other.var_name_tok.value
          
            ret_value = value.context.symbol_table.get(class_symbol_name)

            return ret_value, None

        elif isinstance(other, CallNode):
            from .all import make_value
            
            args = [make_value(i.tok.value) for i in other.arg_nodes]
            
            func, _ = self.dotted(other.tok)
            res = func.execute(args)

            if res.error:
                return None, res.error
            
            return res.value, None
        
    def copy(self):
        copy = Class(self.name, self.body_node)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    