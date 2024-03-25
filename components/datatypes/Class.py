from .Value import Value
from .Function import Function
from .Instance import Instance
from ..node import VarAccessNode, CallNode, ListNode
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
        new_context.symbol_table = SymbolTable(self.symbol_table)
        return new_context
    
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

    def execute(self, args):
        res = RunTimeResult()

        exec_ctx = self.generate_new_context()

        # TODO: Some issue here when direct accessing class methods without instantiation
        inst = Instance(self, SymbolTable(self.symbol_table))
        #inst = Instance(self, self.symbol_table)

        exec_ctx.symbol_table = inst.symbol_table
 
        for name in self.symbol_table.symbols:
            value, type_ = self.symbol_table.copy_symbol(name)
            inst.symbol_table.set(name, value.set_context(exec_ctx), type_)

        for name in self.symbol_table.immutable_symbols:
            value, type_ = self.symbol_table.copy_symbol(name)
            inst.symbol_table.set_as_immutable(name, value.set_context(exec_ctx), type_)

        constructor_name = "__setup__"
        constructor_method = inst.symbol_table.get(constructor_name) if inst.symbol_table.exists(constructor_name) else None

        if constructor_method and isinstance(constructor_method, Function):
            # inst.symbol_table.set_as_builtin(Keyword.SELFREF.value, inst, Instance)
            
            res.register(constructor_method.execute(args))
            if res.should_return():
                return res
        
        elif constructor_method and not isinstance(constructor_method, Function):
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
