from .value import Value
from .null import Null
from ..node import Node
from ..context import Context
from ..runtime import RunTimeResult
from ..error import RunTimeError
from ..symbol_table import SymbolTable
from ..utils.misc import index_exists, try_get, try_set, try_del
from ..utils.debug import DebugMessage

debug_message = DebugMessage("", 1)

class BaseFunction(Value):
    def __init__(self, name: str, display_name: str = None):
        self.name = name or "<anonymous>"
        self.display_name = display_name
        super().__init__()
        
    def _get_name(self) -> str:
        return self.display_name or self.name

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names: list[str], arg_values: list[Value], arg_types: list[Value], arg_default_values: list[Value]):
        res = RunTimeResult()
        # TODO: PROBLEM HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
        for i in range(len(arg_names)):
            if try_get(arg_values, i) is not None:
                if not isinstance(try_get(arg_values, i), arg_types[i]):
                    return res.failure(RunTimeError(
                        self.pos_start, self.pos_end,
                        f"Argument {i} '{arg_names[i]}' in '{self._get_name()}' must be an type of '{arg_types[i].__qualname__}' but got '{type(arg_values[i]).__qualname__}'",
                        self.context
                    ))
            elif try_get(arg_values, i) is None:
                #try_del(arg_values, i)
                if index_exists(arg_values, i):
                    del arg_values[i]
                    
        if len(arg_values) > len(arg_names):
            return res.failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"{len(arg_values) - len(arg_names)} too many args passed into '{self._get_name()}'",
                self.context
            ))

        if len(arg_values) < len(arg_names):
            return res.failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(arg_values)} too few args passed into '{self._get_name()}'",
                self.context
            ))
             

        return res.success(None)

    def populate_args(self, arg_names: list[str], arg_values: list[Value], arg_types: list[Value], arg_default_values: list[Value], exec_ctx: Context):
        for i in range(len(arg_values)):
            arg_name: str = try_get(arg_names, i)
            arg_value: Value = try_get(arg_values, i)
            arg_type: Value = try_get(arg_types, i)
            arg_default_value: Value = try_get(arg_default_values, i)
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)
            exec_ctx.symbol_table.set(f"{arg_name}.TYPE", arg_type)
            exec_ctx.symbol_table.set(f"{arg_name}.DEFAULT", arg_default_value)

    def check_and_populate_args(self, arg_names: list[str], arg_values: list[Value], arg_types: list[Value], arg_default_values: list[Value], exec_ctx: Context):
        res = RunTimeResult()
        
        arg_values = fill_default_args(arg_values, arg_default_values, arg_names)
        
        res.register(self.check_args(arg_names, arg_values, arg_types, arg_default_values))
        if res.should_return() and res.func_return_value is None:
            return res
        self.populate_args(arg_names, arg_values, arg_types, arg_default_values, exec_ctx)

        return res.success(None)

    def __repr__(self):
        return f"<{self.__class__.__qualname__}:{self.name}>"


class Function(BaseFunction):
    def __init__(self, name: str, body_node: Node, arg_names: list[str], arg_types: list[Value], arg_default_values: list[Value], should_auto_return: bool = False):
        self.body_node = body_node
        self.arg_names = arg_names
        self.arg_types = arg_types
        self.arg_default_values = arg_default_values
        self.should_auto_return = should_auto_return
        super().__init__(name)

    def execute(self, arg_values: list[Value]):
        from ..interpreter import Interpreter

        res = RunTimeResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        ##########
        
        #arg_values = fill_default_args(arg_values, self.arg_default_values, self.arg_names)
            
        ##########
        
        res.register(self.check_and_populate_args(
            self.arg_names, arg_values, self.arg_types, self.arg_default_values, exec_ctx))
        if res.should_return() and res.func_return_value is None:
            return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value is None:
            return res

        ret_value = (
            value if self.should_auto_return else None) or res.func_return_value or Null.null
        return res.success(ret_value)

    def copy(self):
        copy = Function(self.name, self.body_node,
                        self.arg_names, self.arg_types, self.arg_default_values, self.should_auto_return)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

def make_args_struct(name: str, type: Value = Value, default_value: Value = None):
    return {
        "NAME": name,
        "TYPE": type,
        "DEFAULT_VALUE": default_value
    }
    
# TODO: PROBLEM HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
def fill_default_args(input_arg_values, default_arg_values, arg_names):
    debug_message.set_auto_display(True)

    new_args = [None] * (len(default_arg_values) if input_arg_values == [] else len(input_arg_values))
    
    debug_message.set_message(f"ARG VALUES: INPUT: {input_arg_values}")
    debug_message.set_message(f"ARG VALUES: DEFAULT: {default_arg_values}")
    debug_message.set_message(f"ARG VALUES: NAMESs: {arg_names}")
    
    for i in range(len(new_args)):
        if index_exists(default_arg_values, i):
            new_args[i] = default_arg_values[i]
            
        if index_exists(input_arg_values, i) and try_get(new_args, i) == None:
            try_set(new_args, i, try_get(input_arg_values, i))
            new_args[i] = input_arg_values[i]
    
    debug_message.set_message(f"ARG VALUES: NEW: {new_args}")

    return new_args