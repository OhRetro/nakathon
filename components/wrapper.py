from components.lexer import Lexer
from components.parser import Parser
from components.interpreter import Interpreter
from components.context import Context
from components.symbol_table import SymbolTable
from components.values.null import Null
from components.values.boolean import Boolean
from components.values.function import BuiltInFunction
from components.utils.debug import DebugMessage

debug_message = DebugMessage("")

global_symbol_table = SymbolTable()

global_symbol_table.set_as_immutable("null", Null.null)
global_symbol_table.set_as_immutable("false", Boolean.false)
global_symbol_table.set_as_immutable("true", Boolean.true)

global_symbol_table.set_as_immutable("Print", BuiltInFunction.print)

global_symbol_table.set_as_immutable("Input", BuiltInFunction.input)
global_symbol_table.set_as_immutable("InputNumber", BuiltInFunction.input_int)

global_symbol_table.set_as_immutable("Clear", BuiltInFunction.clear)

global_symbol_table.set_as_immutable("ToString", BuiltInFunction.to_string)

global_symbol_table.set_as_immutable("IsNumber", BuiltInFunction.is_number)
global_symbol_table.set_as_immutable("IsString", BuiltInFunction.is_string)
global_symbol_table.set_as_immutable("IsList", BuiltInFunction.is_list)
global_symbol_table.set_as_immutable("IsFunction", BuiltInFunction.is_function)
global_symbol_table.set_as_immutable("IsBoolean", BuiltInFunction.is_boolean)
global_symbol_table.set_as_immutable("IsNull", BuiltInFunction.is_null)

global_symbol_table.set_as_immutable("ListAppend", BuiltInFunction.list_append)
global_symbol_table.set_as_immutable("ListPop", BuiltInFunction.list_pop)
global_symbol_table.set_as_immutable("ListExtend", BuiltInFunction.list_extend)
global_symbol_table.set_as_immutable("ListLen", BuiltInFunction.list_len)

global_symbol_table.set_as_immutable("Random", BuiltInFunction.random)
global_symbol_table.set_as_immutable("RandomInt", BuiltInFunction.random_int)
global_symbol_table.set_as_immutable("RandomFloat", BuiltInFunction.random_float)

global_symbol_table.set_as_immutable("Run", BuiltInFunction.run)
global_symbol_table.set_as_immutable("Exit", BuiltInFunction.exit)

#global_symbol_table.set_as_immutable("te", builtin_func)

def run(fn: str, text: str, context_name: str, calling_external_code: bool = False):  
    # Generate tokens
    lexer = Lexer(fn, text, calling_external_code)
    tokens, error = lexer.make_tokens()
    debug_message.set_message(f"Lexer generated:\n\tTokens: {tokens}\n\tError: {error}\n").display()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    debug_message.set_message(f"Parser generated:\n\tNode: {ast.node}\n\tError: {ast.error}\n").display()
    if ast.error: return None, ast.error
    
    # Run Program
    interpreter = Interpreter()
    context = Context(context_name)
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)
    debug_message.set_message(f"Interpreter generated:\n\tValue: {result.value}\n\tError: {result.error}\n").display()
    return result.value, result.error
