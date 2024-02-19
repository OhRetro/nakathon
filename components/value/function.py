from os import system as os_system, name as os_name
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
                f"{len(args) - len(arg_names)} too many args passed into '{self.name}'",
                self.context
            ))
            
        if len(args) < len(arg_names):
            return res.failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)} too few args passed into '{self.name}'",
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
        if res.error: return res
        self.populate_args(arg_names, args, exec_ctx)
        
        return res.success(None)

    def __repr__(self):
        return f"<{self.__class__.__qualname__}:{self.name}>"
    #({", ".join(self.arg_names)})
    
class Function(BaseFunction):
    def __init__(self, name: str, body_node: Node, arg_names: list[str] = [], should_return_null: bool = False):
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_return_null = should_return_null
        super().__init__(name)
        
    def execute(self, args):
        from ..interpreter import Interpreter
        
        res = RunTimeResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()
        
        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.error: return res
        
        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.error: return res
        
        return res.success(Null.null if self.should_return_null else value)
    
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_return_null)
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
        
        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.error: return res
        
        return_value = res.register(method(exec_ctx))
        if res.error: return res
        
        return res.success(return_value)

    def no_visit_method(self, node: Node, context: Context):
        raise Exception(f"No execute_{self.name} method defined")
    
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def execute_print(self, exec_ctx: Context):
        print(str(exec_ctx.symbol_table.get("value")))
        return RunTimeResult().success(Null.null)
    execute_print.arg_names = ["value"]
    
    def execute_print_ret(self, exec_ctx: Context):
        return RunTimeResult().success(String(str(exec_ctx.symbol_table.get("value"))))
    execute_print_ret.arg_names = ["value"]
    
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
        is_function = isinstance(exec_ctx.symbol_table.get("value"), Function) or isinstance(exec_ctx.symbol_table.get("value"), BuiltInFunction)
        return RunTimeResult().success(Boolean.true if is_function else Boolean.false)
    execute_is_function.arg_names = ["value"]
    
    def execute_append(self, exec_ctx: Context):
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
    execute_append.arg_names = ["list", "value"]
    
    def execute_pop(self, exec_ctx: Context):
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
    execute_pop.arg_names = ["list", "index"]
    
    def execute_extend(self, exec_ctx: Context):
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
    execute_extend.arg_names = ["listA", "listB"]
    
BuiltInFunction.print       = BuiltInFunction("print")
BuiltInFunction.print_ret   = BuiltInFunction("print_ret")
BuiltInFunction.input       = BuiltInFunction("input_string")
BuiltInFunction.input_int   = BuiltInFunction("input_number")
BuiltInFunction.clear       = BuiltInFunction("clear")
BuiltInFunction.is_number   = BuiltInFunction("is_number")
BuiltInFunction.is_string   = BuiltInFunction("is_string")
BuiltInFunction.is_list     = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append      = BuiltInFunction("append")
BuiltInFunction.pop         = BuiltInFunction("pop")
BuiltInFunction.extend      = BuiltInFunction("extend")
