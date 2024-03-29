from os import getcwd
from components.lexer import Lexer
from components.parser import Parser
from components.interpreter import Interpreter
from components.context import Context
from components.symbol_table import SymbolTable
from components.datatypes.all import Value, Boolean, Null, String
from components.datatypes.BuiltInFunction import define_builtin_functions
from components.utils.debug import DebugMessage

debug_message = DebugMessage("").set_auto_display(True)

global_symbol_table = SymbolTable()

def set_builtin(name: str, value: Value, type: Value = Value):
    global_symbol_table.set_as_builtin(name, value, type)
    
set_builtin("null", Null.null, Null)
set_builtin("false", Boolean.false, Boolean)
set_builtin("true", Boolean.true, Boolean)
define_builtin_functions(global_symbol_table)

def run(fn: str, text: str, context_name: str, calling_external_code: bool = False, isolated_symbol_table: bool = False, **kwargs):
    _cwd = getcwd()
    if "cwd" in kwargs:
        _cwd = kwargs["cwd"]
        
    set_builtin("NAKATHON_CWD", String(_cwd.replace("\\", "/")), String)
        
    # Generate tokens
    lexer = Lexer(fn, text, calling_external_code)
    tokens, error = lexer.make_tokens()
    debug_message.set_message(f"Lexer generated:\n\tTokens: {tokens}\n\tError: {error}\n")
    if error: return None, error, None

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    debug_message.set_message(f"Parser generated:\n\tNode: {ast.node}\n\tError: {ast.error}\n")
    if ast.error: return None, ast.error, None
    
    # Run Program
    interpreter = Interpreter()
    context = Context(context_name)
    context.symbol_table = global_symbol_table.copy() if isolated_symbol_table else global_symbol_table
    result = interpreter.visit(ast.node, context)
    debug_message.set_message(f"Interpreter generated:\n\tValue: {result.value}\n\tError: {result.error}\n")

    return result.value, result.error, context
