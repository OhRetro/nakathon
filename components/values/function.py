from os import system as os_system, name as os_name
from random import randint, random, uniform
from enum import Enum
from .value import Value
from .number import Number
from .boolean import Boolean
from .null import Null
from .string import String
from .list import List
from ..node import Node
from ..context import Context
from ..runtime import RunTimeResult
from ..error import RunTimeError
from ..symbol_table import SymbolTable


class BuiltInFunctionNames(Enum):
    PRINT = "Print"
    INPUT = "Input"
    INPUTNUMBER = "InputNumber"


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


class BuiltInFunction(BaseFunction):
    def __init__(self, name: str):
        self.name = name or "<anonymous>"
        super().__init__(name)

    def execute(self, args):
        res = RunTimeResult()
        exec_ctx = self.generate_new_context()

        method_name = f"execute_{self.name}"
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(
            method.arg_names, args, exec_ctx))
        if res.should_return():
            return res

        return_value = res.register(method(exec_ctx))
        if res.should_return():
            return res

        return res.success(return_value)

    def no_visit_method(self, node: Node, context: Context):
        raise Exception(f"No execute_{self.name} method defined")

    def copy(self):
        copy = self.__class__(self.name)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def execute_print(self, exec_ctx: Context):
        print(exec_ctx.symbol_table.get("value").__print_repr__())
        return RunTimeResult().success(Null.null)
    execute_print.arg_names = ["value"]

    def execute_input_string(self, exec_ctx: Context):
        text = input()
        return RunTimeResult().success(String(text))
    execute_input_string.arg_names = []

    def execute_input_number(self, exec_ctx: Context):
        while True:
            text = input()
            try:
                number = int(text) if "." not in text else float(text)
                break
            except ValueError:
                print(f"'{text}' must be an number. try again")

        return RunTimeResult().success(Number(number))
    execute_input_number.arg_names = []

    def execute_clear(self, exec_ctx: Context):
        os_system("cls" if os_name == "nt" else "clear")
        return RunTimeResult().success(Null.null)
    execute_clear.arg_names = []

    def execute_to_string(self, exec_ctx: Context):
        return RunTimeResult().success(String(exec_ctx.symbol_table.get("value").__print_repr__()))
    execute_to_string.arg_names = ["value"]

    def execute_is_number(self, exec_ctx: Context):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RunTimeResult().success(Boolean.true if is_number else Boolean.false)
    execute_is_number.arg_names = ["value"]

    def execute_is_string(self, exec_ctx: Context):
        is_string = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RunTimeResult().success(Boolean.true if is_string else Boolean.false)
    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_ctx: Context):
        is_list = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RunTimeResult().success(Boolean.true if is_list else Boolean.false)
    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_ctx: Context):
        is_function = isinstance(exec_ctx.symbol_table.get("value"), Function) or isinstance(
            exec_ctx.symbol_table.get("value"), BuiltInFunction)
        return RunTimeResult().success(Boolean.true if is_function else Boolean.false)
    execute_is_function.arg_names = ["value"]

    def execute_is_boolean(self, exec_ctx: Context):
        is_boolean = isinstance(exec_ctx.symbol_table.get("value"), Boolean)
        return RunTimeResult().success(Boolean.true if is_boolean else Boolean.false)
    execute_is_boolean.arg_names = ["value"]
    
    def execute_is_null(self, exec_ctx: Context):
        is_null = isinstance(exec_ctx.symbol_table.get("value"), Null)
        return RunTimeResult().success(Boolean.true if is_null else Boolean.false)
    execute_is_null.arg_names = ["value"]
    
    def execute_list_append(self, exec_ctx: Context):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "First arg must be list",
                exec_ctx
            ))

        list_.elements.append(value)

        return RunTimeResult().success(list_)
    execute_list_append.arg_names = ["list", "value"]

    def execute_list_pop(self, exec_ctx: Context):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "First arg must be list",
                exec_ctx
            ))

        if not isinstance(index, Number):
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "Second arg must be number",
                exec_ctx
            ))

        try:
            element = list_.elements.pop(index.value)
        except:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "Out of Bounds",
                exec_ctx
            ))

        return RunTimeResult().success(element)
    execute_list_pop.arg_names = ["list", "index"]

    def execute_list_extend(self, exec_ctx: Context):
        list_a = exec_ctx.symbol_table.get("listA")
        list_b = exec_ctx.symbol_table.get("listB")

        if not isinstance(list_a, List):
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "First arg must be list",
                exec_ctx
            ))

        if not isinstance(list_b, List):
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "Second arg must be list",
                exec_ctx
            ))

        list_a.elements.extend(list_b.elements)

        return RunTimeResult().success(list_a)
    execute_list_extend.arg_names = ["listA", "listB"]

    def execute_list_len(self, exec_ctx: Context):
        list_ = exec_ctx.symbol_table.get("list")

        if not isinstance(list_, List):
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "First arg must be list",
                exec_ctx
            ))

        return RunTimeResult().success(Number(len(list_.elements)))
    execute_list_len.arg_names = ["list"]

    def execute_random(self, exec_ctx: Context):
        return RunTimeResult().success(Number(random()))
    execute_random.arg_names = []

    def execute_random_int(self, exec_ctx: Context):
        min = exec_ctx.symbol_table.get("min")
        max = exec_ctx.symbol_table.get("max")

        if not isinstance(min, Number) or not isinstance(max, Number) or min.is_float or max.is_float:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "Both arg must be int",
                exec_ctx
            ))

        return RunTimeResult().success(Number(randint(min.value, max.value)))
    execute_random_int.arg_names = ["min", "max"]
    
    def execute_random_float(self, exec_ctx: Context):
        min = exec_ctx.symbol_table.get("min")
        max = exec_ctx.symbol_table.get("max")

        if not isinstance(min, Number) or not isinstance(max, Number):
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "Both arg must be number",
                exec_ctx
            ))

        return RunTimeResult().success(Number(uniform(min.value, max.value)))
    execute_random_float.arg_names = ["min", "max"]
    
    def execute_run(self, exec_ctx: Context):
        from ..wrapper import run
        fn = exec_ctx.symbol_table.get("fn")

        if not isinstance(fn, String):
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "Arg must be string",
                exec_ctx
            ))

        fn = fn.value

        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"Failed to load script \"{fn}\"\n" + str(e),
                exec_ctx
            ))

        _, error = run(fn, script)

        if error:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"Failed to finish executing the script \"{fn}\"\n" +
                error.as_string(),
                exec_ctx
            ))

        return RunTimeResult().success(Null.null)
    execute_run.arg_names = ["fn"]


BuiltInFunction.print = BuiltInFunction("print")

BuiltInFunction.input = BuiltInFunction("input_string")
BuiltInFunction.input_int = BuiltInFunction("input_number")

BuiltInFunction.clear = BuiltInFunction("clear")

BuiltInFunction.to_string = BuiltInFunction("to_string")

BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.is_boolean = BuiltInFunction("is_boolean")
BuiltInFunction.is_null = BuiltInFunction("is_null")

BuiltInFunction.list_append = BuiltInFunction("list_append")
BuiltInFunction.list_pop = BuiltInFunction("list_pop")
BuiltInFunction.list_extend = BuiltInFunction("list_extend")
BuiltInFunction.list_len = BuiltInFunction("list_len")

BuiltInFunction.random = BuiltInFunction("random")
BuiltInFunction.random_int = BuiltInFunction("random_int")
BuiltInFunction.random_float = BuiltInFunction("random_float")

BuiltInFunction.run = BuiltInFunction("run")
