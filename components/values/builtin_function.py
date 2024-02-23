from os import system as os_system, name as os_name
from random import randint, random, uniform
from enum import Enum
from .value import Value
from .number import Number
from .boolean import Boolean
from .null import Null
from .string import String
from .list import List
from .function import BaseFunction, Function
from ..symbol_table import SymbolTable
from ..node import Node
from ..context import Context
from ..runtime import RunTimeResult
from ..error import RunTimeError
from ..utils.strings_template import OUT_OF_BOUNDS_ERROR

class BuiltInFunctionNames(Enum):
    PRINT = "Print"
    
    INPUT = "Input"
    INPUTNUMBER = "InputNumber"
    
    CLEAR = "Clear"
    
    TOSTRING = "ToString"
    
    ISNUMBER = "IsNumber"
    ISSTRING = "IsString"
    ISLIST = "IsList"
    ISFUNCTION = "IsFunction"
    ISBOOLEAN = "IsBoolean"
    ISNULL = "IsNull"
    
    LISTAPPEND = "ListAppend"
    LISTPOP = "ListPop"
    LISTEXTEND = "ListExtend"
    LISTLEN = "ListLen"
    
    RANDOM = "Random"
    RANDOMINT = "RandomInt"
    RANDOMFLOAT = "RandomFloat"
    
    RUN = "Run"
    EXIT = "Exit"

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

    def execute_PRINT(self, exec_ctx: Context):
        print(exec_ctx.symbol_table.get("value").__print_repr__())
        return RunTimeResult().success(Null.null)
    execute_PRINT.arg_names = ["value"]

    def execute_INPUT(self, exec_ctx: Context):
        text = input()
        return RunTimeResult().success(String(text))
    execute_INPUT.arg_names = []

    def execute_INPUTNUMBER(self, exec_ctx: Context):
        while True:
            text = input()
            try:
                number = int(text) if "." not in text else float(text)
                break
            except ValueError:
                print(f"'{text}' must be an number. try again")

        return RunTimeResult().success(Number(number))
    execute_INPUTNUMBER.arg_names = []

    def execute_CLEAR(self, exec_ctx: Context):
        os_system("cls" if os_name == "nt" else "clear")
        return RunTimeResult().success(Null.null)
    execute_CLEAR.arg_names = []

    def execute_TOSTRING(self, exec_ctx: Context):
        return RunTimeResult().success(String(exec_ctx.symbol_table.get("value").__print_repr__()))
    execute_TOSTRING.arg_names = ["value"]

    def execute_ISNUMBER(self, exec_ctx: Context):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RunTimeResult().success(Boolean.true if is_number else Boolean.false)
    execute_ISNUMBER.arg_names = ["value"]

    def execute_ISSTRING(self, exec_ctx: Context):
        is_string = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RunTimeResult().success(Boolean.true if is_string else Boolean.false)
    execute_ISSTRING.arg_names = ["value"]

    def execute_ISLIST(self, exec_ctx: Context):
        is_list = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RunTimeResult().success(Boolean.true if is_list else Boolean.false)
    execute_ISLIST.arg_names = ["value"]

    def execute_ISFUNCTION(self, exec_ctx: Context):
        is_function = isinstance(exec_ctx.symbol_table.get("value"), Function) or isinstance(
            exec_ctx.symbol_table.get("value"), BuiltInFunction)
        return RunTimeResult().success(Boolean.true if is_function else Boolean.false)
    execute_ISFUNCTION.arg_names = ["value"]

    def execute_ISBOOLEAN(self, exec_ctx: Context):
        is_boolean = isinstance(exec_ctx.symbol_table.get("value"), Boolean)
        return RunTimeResult().success(Boolean.true if is_boolean else Boolean.false)
    execute_ISBOOLEAN.arg_names = ["value"]
    
    def execute_ISNULL(self, exec_ctx: Context):
        is_null = isinstance(exec_ctx.symbol_table.get("value"), Null)
        return RunTimeResult().success(Boolean.true if is_null else Boolean.false)
    execute_ISNULL.arg_names = ["value"]
    
    def execute_LISTAPPEND(self, exec_ctx: Context):
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
    execute_LISTAPPEND.arg_names = ["list", "value"]

    def execute_LISTPOP(self, exec_ctx: Context):
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
                OUT_OF_BOUNDS_ERROR,
                exec_ctx
            ))

        return RunTimeResult().success(element)
    execute_LISTPOP.arg_names = ["list", "index"]

    def execute_LISTEXTEND(self, exec_ctx: Context):
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
    execute_LISTEXTEND.arg_names = ["listA", "listB"]

    def execute_LISTLEN(self, exec_ctx: Context):
        list_ = exec_ctx.symbol_table.get("list")

        if not isinstance(list_, List):
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "First arg must be list",
                exec_ctx
            ))

        return RunTimeResult().success(Number(len(list_.elements)))
    execute_LISTLEN.arg_names = ["list"]

    def execute_RANDOM(self, exec_ctx: Context):
        return RunTimeResult().success(Number(random()))
    execute_RANDOM.arg_names = []

    def execute_RANDOMINT(self, exec_ctx: Context):
        min = exec_ctx.symbol_table.get("min")
        max = exec_ctx.symbol_table.get("max")

        if not isinstance(min, Number) or not isinstance(max, Number) or min.is_float or max.is_float:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "Both arg must be int",
                exec_ctx
            ))

        return RunTimeResult().success(Number(randint(min.value, max.value)))
    execute_RANDOMINT.arg_names = ["min", "max"]
    
    def execute_RANDOMFLOAT(self, exec_ctx: Context):
        min = exec_ctx.symbol_table.get("min")
        max = exec_ctx.symbol_table.get("max")

        if not isinstance(min, Number) or not isinstance(max, Number):
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "Both arg must be number",
                exec_ctx
            ))

        return RunTimeResult().success(Number(uniform(min.value, max.value)))
    execute_RANDOMFLOAT.arg_names = ["min", "max"]
    
    def execute_RUN(self, exec_ctx: Context):
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

        _, error = run(fn, script, "<ShellRun>", True)

        if error:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"Failed to finish executing the script \"{fn}\"\n" +
                error.as_string(),
                exec_ctx
            ))

        return RunTimeResult().success(Null.null)
    execute_RUN.arg_names = ["fn"]
    
    def execute_EXIT(self, exec_ctx: Context):
        code_number = exec_ctx.symbol_table.get("code_number")
        if not isinstance(code_number, Number) or code_number.is_float:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "Arg must be int",
                exec_ctx
            ))
        return RunTimeResult().success(Number(code_number))
    execute_EXIT.arg_names = ["code_number"]
    
def define_builtin_functions(symbol_table: SymbolTable):
    for name in BuiltInFunctionNames:
        symbol_table.set_as_immutable(name.value, BuiltInFunction(name.name))