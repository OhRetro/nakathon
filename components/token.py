from enum import Enum
from typing import Any
from .position import Position
from .utils.debug import DebugMessage

debug_message = DebugMessage("", filename=__file__)

class Keyword(Enum):
    # Variables and Methods/Functions
    SETVAR = "var"
    SETIMMUTABLEVAR = "const"
    SETTEMPVAR = "temp"
    SETSCOPEDVAR = "local"
    SETFUNCTION = "func"
      
    # Conditional
    AND = "&&"
    OR = "||"
    NOT = "not"
    IF = "if"
    ELSEIF = "else if"
    ELSE = "else"
    IS = "is"
    
    # Loops
    FOR = "for"
    WHILE = "while"
    CONTINUE = "continue"
    BREAK = "break"
    
    # Other
    RETURN = "return"

class TokenType(Enum):
    # General types
    KEYWORD = "keyword"
    IDENTIFIER = "identifier"
    EQUALS = "="
    
    # Data types
    INT = "int"
    FLOAT = "float"
    STRING = '"'
    
    # Mathmatic types
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    POWER = "**"
    DIV = "/"
    DIVREST = "%"
    
    # Parenthesis, Square and Brace
    LPAREN = "("
    RPAREN = ")"
    LSQUARE = "["
    RSQUARE = "]"
    LBRACE = "{"
    RBRACE = "}"
    
    # Conditional types
    EE = "=="
    NE = "!="
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="
    ISNULL = "?="
    
    # Other
    DOT = "."
    COMMA = ","
    ARROW = "->"
    SEMICOLON = ";"
    COLON = ":"
    NEWLINE = "\n"
    COMMENT = "#"
    
    GENERIC = "GENERIC"
    
    EOF = "EOF"

class Token:
    def __init__(self, type_: TokenType, value: Any = None, pos_start: Position = None, pos_end: Position = None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end
            
        debug_message.set_message(f"TOKEN: CREATED: {self}").display()

    def matches(self, type_: TokenType, value: Any = None):
        return (self.type == type_ and self.value == value) if value else (self.type == type_)

    def __repr__(self):
        strRepr = f"<Token:{self.type.name}"
        if self.value and not isinstance(self.value, type):
            strRepr += f":{self.value}>" if not isinstance(self.value, Enum) else f":{self.value.name}>"
        elif self.value and isinstance(self.value, type):
            strRepr += f":{self.value.__name__}>"
        else:
            strRepr += ">"
        return strRepr
