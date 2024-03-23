from .Value import Value
from .Function import Function
from .Instance import Instance
from ..node import VarAccessNode, CallNode, ListNode, Node
from ..runtime import RunTimeResult
from ..error import RunTimeError
from ..context import Context
from ..symbol_table import SymbolTable
from ..keyword import Keyword

class Class(Value):
    def __init__(self, name: str, body_node: ListNode, symbol_table: SymbolTable):
        self.name = name
        self.body_node = body_node
        self.symbol_table = symbol_table
        super().__init__(name)

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context
    
    #! LEFTOVER OF OLD METHOD, STILL HERE FOR REFERENCING
    def dotted(self, other: VarAccessNode | CallNode):
        # from ..interpreter import Interpreter

        res = RunTimeResult()
        # interpreter = Interpreter()
        # exec_ctx = self.generate_new_context()
        
        if isinstance(other, VarAccessNode):
            # value: Value = res.register(interpreter.visit(self.body_node, exec_ctx))

            class_symbol_name = other.var_name_tok.value
          
            # ret_value = value.context.symbol_table.get(class_symbol_name)
            ret_value = self.symbol_table.get(class_symbol_name)
            
            return ret_value, None
        
        elif isinstance(other, CallNode):
            from .all import make_value
            
            args = [make_value(i.tok.value) for i in other.arg_nodes]
            
            func, _ = self.dotted(other.tok)
            res = func.execute(args)

            if res.error:
                return None, res.error
            
            return res.value, None
        
        else:
            return self._illegal_operation(other)

    #! Code based from the Radon Project, I'm doing my own implementation, using as a reference
    #! If anything https://en.wikipedia.org/wiki/Ship_of_Theseus
    def execute(self, args):
        res = RunTimeResult()

        exec_ctx = Context(self.name, self.context, self.pos_start)

        # TODO: Some issue here when direct accessing class methods without instantiation
        inst = Instance(self, SymbolTable(self.symbol_table))

        exec_ctx.symbol_table = inst.symbol_table
 
        for name in self.symbol_table.symbols:
            inst.symbol_table.set(name, self.symbol_table.get(name).copy(), Value)

        for name in inst.symbol_table.symbols:
            inst.symbol_table.get(name).set_context(exec_ctx)

        inst.symbol_table.set_as_builtin(Keyword.SELFREF.value, inst, Instance)

        _constructor = "__setup__"
        method = inst.symbol_table.get(_constructor) if inst.symbol_table.exists(_constructor) else None

        if method != None and isinstance(method, Function):
            res.register(method.execute(args))
            if res.should_return():
                return res
        
        elif method != None and not isinstance(method, Function):
            return res.failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"The __setup__ in '{self.name}' must be a function",
                self.context
            ))

        return res.success(inst.set_context(self.context).set_pos(self.pos_start, self.pos_end))
    
    def copy(self):
        copy = Class(self.name, self.body_node, self.symbol_table)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
