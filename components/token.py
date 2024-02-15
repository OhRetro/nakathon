from enum import Enum
from typing import Any
from .position import Position

KEYWORDS = [
    "VAR"
]

class TokenType(Enum):
    # General types
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    EQUALS = "EQUALS"
    
    # Data types
    INT = "INT"
    FLOAT = "FLOAT"
    
    # Mathmatic types
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    POWER = "POWER"
    DIVREST = "DIVREST"
    
    # Parenthesis
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    
    # Other
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

    def matches(self, type_: TokenType, value: Any = None):
        return self.type == type_ and self.value == value

    def __repr__(self):
        strRepr = f"<Token:{self.type.name}"
        if self.value:
            strRepr += f":{self.value}>"
        else:
            strRepr += ">"
        return strRepr
