from .value import Value
from ..runtime import RunTimeResult
from ..error import RunTimeError
from ..context import Context
from ..symbol_table import SymbolTable
from ..node import Node

class Function(Value):
    def __init__(self, name: str, body_node: Node, arg_names: list[str] = []):
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names
        
        super().__init__(name)
        
    def execute(self, args):
        from ..interpreter import Interpreter
        
        res = RunTimeResult()
        interpreter = Interpreter()
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        
        if len(args) > len(self.arg_names):
            return res.failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(self.arg_names)} too many args passed into '{self.name}'",
                self.context
            ))
            
        if len(args) < len(self.arg_names):
            return res.failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(self.arg_names)} too few args passed into '{self.name}'",
                self.context
            ))
            
        for i in range(len(args)):
            arg_name = self.arg_names[i]
            arg_value = args[i]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)
            
        value = res.register(interpreter.visit(self.body_node, new_context))
        if res.error: return res
        return res.success(value)
    
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __repr__(self):
        return f"<Function:{self.name}({", ".join(self.arg_names)})>"