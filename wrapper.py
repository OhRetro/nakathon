from components.lexer import Lexer
from components.parser import Parser
from components.interpreter import Interpreter
from components.context import Context
from components.symbol_table import SymbolTable
from components.value.null import Null
from components.value.boolean import Boolean
from components.value.function import BuiltInFunction
from components.utils.debug import DebugMessage

global_symbol_table = SymbolTable()
global_symbol_table.set_as_immutable("null", Null.null)
global_symbol_table.set_as_immutable("false", Boolean.false)
global_symbol_table.set_as_immutable("true", Boolean.true)
global_symbol_table.set_as_immutable("Print", BuiltInFunction.print)
global_symbol_table.set_as_immutable("PRINT_RETURN", BuiltInFunction.print_ret)
global_symbol_table.set_as_immutable("InputText", BuiltInFunction.input)
global_symbol_table.set_as_immutable("InputNumber", BuiltInFunction.input_int)
global_symbol_table.set_as_immutable("Clear", BuiltInFunction.clear)
global_symbol_table.set_as_immutable("IsNumber", BuiltInFunction.is_number)
global_symbol_table.set_as_immutable("IsString", BuiltInFunction.is_string)
global_symbol_table.set_as_immutable("IsList", BuiltInFunction.is_list)
global_symbol_table.set_as_immutable("IsFunction", BuiltInFunction.is_function)
global_symbol_table.set_as_immutable("ListAppend", BuiltInFunction.append)
global_symbol_table.set_as_immutable("ListPop", BuiltInFunction.pop)
global_symbol_table.set_as_immutable("ListExtend", BuiltInFunction.extend)

def run(fn: str, text: str):
    debug_message = DebugMessage("")
    
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    debug_message.set_message(f"Lexer generated:\n Tokens: {tokens}\n Error: {error}\n").display()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    debug_message.set_message(f"Parser generated:\n Node: {ast.node}\n Error: {ast.error}\n").display()
    if ast.error: return None, ast.error
    
    # Run Program
    interpreter = Interpreter()
    context = Context("<Program>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)
    debug_message.set_message(f"Interpreter generated:\n Value: {result.value}\n Error: {result.error}\n").display()
    return result.value, result.error
