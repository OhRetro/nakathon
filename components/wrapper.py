from components.lexer import Lexer
from components.parser import Parser
from components.interpreter import Interpreter
from components.context import Context
from components.symbol_table import SymbolTable
from components.datatypes.all import Value, Boolean, Null
from components.datatypes.builtin_function import define_builtin_functions
from components.utils.debug import DebugMessage

debug_message = DebugMessage("").set_auto_display(True)

global_symbol_table = SymbolTable()

def set_global(name: str, value: Value, type: Value = Value):
    global_symbol_table.set_as_immutable(name, value, type)
    
set_global("null", Null.null, Null)
set_global("false", Boolean.false, Boolean)
set_global("true", Boolean.true, Boolean)
define_builtin_functions(global_symbol_table)

def run(fn: str, text: str, context_name: str, calling_external_code: bool = False):  
    # Generate tokens
    lexer = Lexer(fn, text, calling_external_code)
    tokens, error = lexer.make_tokens()
    debug_message.set_message(f"Lexer generated:\n\tTokens: {tokens}\n\tError: {error}\n")
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    debug_message.set_message(f"Parser generated:\n\tNode: {ast.node}\n\tError: {ast.error}\n")
    if ast.error: return None, ast.error
    
    # Run Program
    interpreter = Interpreter()
    context = Context(context_name)
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)
    debug_message.set_message(f"Interpreter generated:\n\tValue: {result.value}\n\tError: {result.error}\n")
    return result.value, result.error
