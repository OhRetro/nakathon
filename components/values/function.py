from .value import Value
from .null import Null
from ..node import Node
from ..context import Context
from ..runtime import RunTimeResult
from ..error import RunTimeError
from ..symbol_table import SymbolTable

class BaseFunction(Value):
    def __init__(self, name: str):
        self.name = name or "<anonymous>"
        super().__init__()

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names: list[str], args):
        res = RunTimeResult()

        if len(args) > len(arg_names):
            return res.failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)
                   } too many args passed into '{self.name}'",
                self.context
            ))

        if len(args) < len(arg_names):
            return res.failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)
                   } too few args passed into '{self.name}'",
                self.context
            ))

        return res.success(None)

    def populate_args(self, arg_names: list[str], args, exec_ctx: Context):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names: list[str], args, exec_ctx: Context):
        res = RunTimeResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return() and res.func_return_value is None:
            return res
        self.populate_args(arg_names, args, exec_ctx)

        return res.success(None)

    def __repr__(self):
        return f"<{self.__class__.__qualname__}:{self.name}>"


class Function(BaseFunction):
    def __init__(self, name: str, body_node: Node, arg_names: list[str] = [], should_auto_return: bool = False):
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return
        super().__init__(name)

    def execute(self, args):
        from ..interpreter import Interpreter

        res = RunTimeResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(
            self.arg_names, args, exec_ctx))
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
                        self.arg_names, self.should_auto_return)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
