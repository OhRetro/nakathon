from os import system as os_system, name as os_name
from os.path import join as os_join
from random import randint, random, uniform
from enum import Enum

from .Value import Value
from .Number import Number
from .Boolean import Boolean
from .Null import Null
from .String import String
from .List import List
from .Function import BaseFunction, Function, make_args_struct
from ..symbol_table import SymbolTable
from ..node import Node
from ..context import Context
from ..runtime import RunTimeResult
from ..error import RunTimeError
from ..utils.strings_template import OUT_OF_BOUNDS_ERROR
from ..utils.misc import get_abs_path

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
    
    IMPORT = "Import"
    RUN = "Run"
    EXIT = "Exit"
    
    SHOWCTX = None

class BuiltInFunction(BaseFunction):
    def __init__(self, name: str, display_name: str):
        super().__init__(name, display_name)

    def execute(self, arg_values: list[Value]):
        res = RunTimeResult()
        exec_ctx = self.generate_new_context()

        method_name = f"execute_{self.name}"
        method = getattr(self, method_name, self.no_visit_method)

        ##########
        
        arg_names = []
        arg_types = []
        arg_default_values = []
        
        for arg in method.args:
            arg_names.append(arg.get("NAME"))
            arg_types.append(arg.get("TYPE"))
            arg_default_values.append(arg.get("DEFAULT_VALUE"))
            
        ##########

        res.register(self.check_and_populate_args(
            arg_names, arg_values, arg_types, arg_default_values, exec_ctx))
        if res.should_return():
            return res

        return_value = res.register(method(exec_ctx))
        if res.should_return():
            return res

        return res.success(return_value)

    def no_visit_method(self, node: Node, context: Context):
        raise Exception(f"No execute_{self.name} method defined")

    def copy(self):
        copy = BuiltInFunction(self.name, self.display_name)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def execute_PRINT(self, exec_ctx: Context):
        print(exec_ctx.symbol_table.get("value").__print_repr__())
        return RunTimeResult().success(Null.null)
    execute_PRINT.args = [make_args_struct("value", Value)]

    def execute_INPUT(self, exec_ctx: Context):
        text = input(exec_ctx.symbol_table.get("prompt").__print_repr__())
        return RunTimeResult().success(String(text))
    execute_INPUT.args = [make_args_struct("prompt", String, String("> "))]

    def execute_INPUTNUMBER(self, exec_ctx: Context):
        text = input(exec_ctx.symbol_table.get("prompt").__print_repr__())
        success = False
        try:
            number = int(text) if "." not in text else float(text)
            success = True
        except ValueError:
            pass

        return RunTimeResult().success(Number(number) if success else Null.null)
    execute_INPUTNUMBER.args = [make_args_struct("prompt", String, String("> "))]

    def execute_CLEAR(self, exec_ctx: Context):
        os_system("cls" if os_name == "nt" else "clear")
        return RunTimeResult().success(Null.null)
    execute_CLEAR.args = []

    def execute_TOSTRING(self, exec_ctx: Context):
        return RunTimeResult().success(String(exec_ctx.symbol_table.get("value").__print_repr__()))
    execute_TOSTRING.args = [make_args_struct("value", Value)]

    def execute_ISNUMBER(self, exec_ctx: Context):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RunTimeResult().success(Boolean.true if is_number else Boolean.false)
    execute_ISNUMBER.args = [make_args_struct("value", Value)]

    def execute_ISSTRING(self, exec_ctx: Context):
        is_string = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RunTimeResult().success(Boolean.true if is_string else Boolean.false)
    execute_ISSTRING.args = [make_args_struct("value", Value)]

    def execute_ISLIST(self, exec_ctx: Context):
        is_list = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RunTimeResult().success(Boolean.true if is_list else Boolean.false)
    execute_ISLIST.args = [make_args_struct("value", Value)]

    def execute_ISFUNCTION(self, exec_ctx: Context):
        is_function = isinstance(exec_ctx.symbol_table.get("value"), Function) or isinstance(
            exec_ctx.symbol_table.get("value"), BuiltInFunction)
        return RunTimeResult().success(Boolean.true if is_function else Boolean.false)
    execute_ISFUNCTION.args = [make_args_struct("value", Value)]

    def execute_ISBOOLEAN(self, exec_ctx: Context):
        is_boolean = isinstance(exec_ctx.symbol_table.get("value"), Boolean)
        return RunTimeResult().success(Boolean.true if is_boolean else Boolean.false)
    execute_ISBOOLEAN.args = [make_args_struct("value", Value)]
    
    def execute_ISNULL(self, exec_ctx: Context):
        is_null = isinstance(exec_ctx.symbol_table.get("value"), Null)
        return RunTimeResult().success(Boolean.true if is_null else Boolean.false)
    execute_ISNULL.args = [make_args_struct("value", Value)]
    
    def execute_LISTAPPEND(self, exec_ctx: Context):
        list_: List = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")
        list_.elements.append(value)
        return RunTimeResult().success(list_)
    execute_LISTAPPEND.args = [make_args_struct("list", List), make_args_struct("value", Value)]

    def execute_LISTPOP(self, exec_ctx: Context):
        list_: List = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        try:
            element = list_.elements.pop(index.value)
        except:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                OUT_OF_BOUNDS_ERROR,
                exec_ctx
            ))

        return RunTimeResult().success(element)
    execute_LISTPOP.args = [make_args_struct("list", List), make_args_struct("index", Number)]

    def execute_LISTEXTEND(self, exec_ctx: Context):
        list_a: List = exec_ctx.symbol_table.get("listA")
        list_b: List = exec_ctx.symbol_table.get("listB")
        list_a.elements.extend(list_b.elements)
        return RunTimeResult().success(list_a)
    execute_LISTEXTEND.args = [make_args_struct("listA", List), make_args_struct("listB", List)]

    def execute_LISTLEN(self, exec_ctx: Context):
        list_: List = exec_ctx.symbol_table.get("list")
        return RunTimeResult().success(Number(len(list_.elements)))
    execute_LISTLEN.args = [make_args_struct("list", List)]

    def execute_RANDOM(self, exec_ctx: Context):
        return RunTimeResult().success(Number(random()))
    execute_RANDOM.args = []

    def execute_RANDOMINT(self, exec_ctx: Context):
        min: Number = exec_ctx.symbol_table.get("min")
        max: Number = exec_ctx.symbol_table.get("max")

        if min.is_float or max.is_float:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "Both arg must be int",
                exec_ctx
            ))

        return RunTimeResult().success(Number(randint(min.value, max.value)))
    execute_RANDOMINT.args = [make_args_struct("min", Number), make_args_struct("max", Number)]
    
    def execute_RANDOMFLOAT(self, exec_ctx: Context):
        min: Number = exec_ctx.symbol_table.get("min")
        max: Number = exec_ctx.symbol_table.get("max")
        return RunTimeResult().success(Number(uniform(min.value, max.value)))
    execute_RANDOMFLOAT.args = [make_args_struct("min", Number), make_args_struct("max", Number)]

    def execute_IMPORT(self, exec_ctx: Context):
        from ..wrapper import run
        fn = exec_ctx.symbol_table.get("filename").value
        cwd = exec_ctx.symbol_table.get("NAKATHON_CWD").value
        namespace = exec_ctx.symbol_table.get("namespace").value.replace(" ", "_")

        fn += ".nkt" if not fn.endswith(".nkt") else ""
        
        full_path = os_join(cwd, fn).replace("\\", "/")
        import_cwd = get_abs_path(full_path)
        target_file = full_path.split("/")[-1]
        
        if namespace == "":
            namespace = target_file.removesuffix(".nkt")
        
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                script = f.read()
        except Exception as e:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"Failed to load \"{fn}\"\n" + str(e),
                exec_ctx
            ))

        _, error, context = run(fn, script, 
                                f"<Importing \"{target_file}\" as \"{namespace}\">" if namespace != "*" 
                                else f"<Importing \"{target_file}\" without a namespace>", 
                                True, True, cwd=import_cwd)
        
        if error:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"Failed to finish importing \"{fn}\"\n" +
                error.as_string(),
                exec_ctx
            ))
        
        if namespace != "*":
            exec_ctx.parent.import_from(context, namespace)
        else:
            exec_ctx.parent.merge(context)
        
        return RunTimeResult().success(String(namespace))
    execute_IMPORT.args = [make_args_struct("filename", String), make_args_struct("namespace", String, String(""))]
    
    def execute_RUN(self, exec_ctx: Context):
        from ..wrapper import run
        fn = exec_ctx.symbol_table.get("filename").value
        cwd = exec_ctx.symbol_table.get("NAKATHON_CWD").value
        
        fn += ".nkt" if not fn.endswith(".nkt") else ""

        full_path = os_join(cwd, fn).replace("\\", "/")
        run_cwd = get_abs_path(full_path)
        target_file = full_path.split("/")[-1]
        
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                script = f.read()
        except Exception as e:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"Failed to load script \"{fn}\"\n" + str(e),
                exec_ctx
            ))

        _, error, _ = run(fn, script, f"<Running {target_file}>", True, True, cwd=run_cwd)

        if error:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"Failed to finish executing the script \"{fn}\"\n" +
                error.as_string(),
                exec_ctx
            ))
        
        return RunTimeResult().success(Null.null)
    execute_RUN.args = [make_args_struct("filename", String)]
    
    def execute_EXIT(self, exec_ctx: Context):
        code_number: Number = exec_ctx.symbol_table.get("code_number")
        if code_number.is_float:
            return RunTimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "Arg must be int",
                exec_ctx
            ))
        exit(code_number.value)
    execute_EXIT.args = [make_args_struct("code_number", Number, Number(0))]
    
    def execute_SHOWCTX(self, exec_ctx: Context):
        symbol_id: str = exec_ctx.symbol_table.get("symbol_id").value
        
        def _method(context: Context, symbol_id: str):
            print(f"{context.display_name}:")
            symbols_list = {
                "n": "symbols",
                "i": "immutable_symbols",
                "t": "temporary_symbols",
                "s": "scoped_symbols"
            }
            
            def _method1(symbol_table: SymbolTable, symbol_name: str):
                print(f"\t{symbol_name}:")
                
                symbol = getattr(symbol_table, symbol_name)
                
                _out_text = []
                
                for k, v in symbol.items():
                    _out_text.append(f"{k} = {v[0]}")
                
                if not _out_text:
                    print("\t{}")
                else:
                    print("\t{")
                    for text in _out_text:
                        print(f"\t\t{text}")
                    print("\t}")
                
                # if symbol_table.parent:
                #     _method1(symbol_table.parent, symbol_name)

            if symbol_id in symbols_list and symbol_id != "*":
                _method1(context.symbol_table, symbols_list.get(symbol_id))
            else:
                for _, v in symbols_list.items():
                    _method1(context.symbol_table, v)
                    
            if context.parent:
                print("")
                _method(context.parent, symbol_id)

        _method(exec_ctx, symbol_id)        
        
        return RunTimeResult().success(Null.null)
    execute_SHOWCTX.args = [make_args_struct("symbol_id", String, String("*"))]
    
def define_builtin_functions(symbol_table: SymbolTable):
    for name in BuiltInFunctionNames:
        func_name = name.value if name.value else f"NAKATHON_{name.name}"
        symbol_table.set_as_builtin(func_name, BuiltInFunction(name.name, func_name), BuiltInFunction)
        