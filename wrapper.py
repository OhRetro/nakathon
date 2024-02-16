from components.lexer import Lexer
from components.parser import Parser
from components.interpreter import Interpreter
from components.context import Context
from components.symbol_table import SymbolTable
from components.number import Number


global_symbol_table = SymbolTable({
    "PI": Number(3.14),
    "NULL": Number(-1),
    "FALSE": Number(0),
    "TRUE": Number(1)
})


def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error
    
    # Run Program
    interpreter = Interpreter()
    context = Context("<Program>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)
    return result.value, result.error
