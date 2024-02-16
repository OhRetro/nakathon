from components.lexer import Lexer
from components.parser import Parser
from components.interpreter import Interpreter
from components.context import Context
from components.symbol_table import SymbolTable
from components.values.number import Number
from components.values.function import Function
from components.position import Position
from components.node import *

from components.utils.debug import DebugMessage

global_symbol_table = SymbolTable(None, {
    "PI": Number(3.14),
    "NULL": Number(-1),
    "FALSE": Number(0),
    "TRUE": Number(1)
})


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
