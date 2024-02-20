from enum import Enum
from typing import Any
from .position import Position
from .utils.debug import DebugMessage

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
    THEN = "then"
    ELSEIF = "else if"
    ELSE = "else"
    IS = "is"
    
    # Loops
    FOR = "for"
    TO = "to"
    STEP = "step"
    WHILE = "while"
    CONTINUE = "continue"
    BREAK = "break"
    
    # Other
    RETURN = "return"
    END = "end"


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
    COMMA = ","
    ARROW = "->"
    SEMICOLON = ";"
    NEWLINE = "\n"
    COMMENT = "#"
    
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
            
        DebugMessage(f"Created {self}").display()

    def matches(self, type_: TokenType, value: Any = None):
        return self.type == type_ and self.value == value

    def __repr__(self):
        strRepr = f"<Token:{self.type.name}"
        if self.value:
            strRepr += f":{self.value}>" if not isinstance(self.value, Enum) else f":{self.value.name}>"
        else:
            strRepr += ">"
        return strRepr
