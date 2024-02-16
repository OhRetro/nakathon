from enum import Enum
from typing import Any
from .position import Position
from .utils.debug import DebugMessage

class Keyword(Enum):
    # Variables
    SETVAR = "VAR"
    
    # Conditional
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    ELIF = "ELIF"
    
    # Loops
    FOR = "FOR"
    TO = "TO"
    STEP = "STEP"
    WHILE = "WHILE"
    
    # Other
    SETFUNCTION = "FUN"


class TokenType(Enum):
    # General types
    KEYWORD = "keyword"
    IDENTIFIER = "identifier"
    EQUALS = "="
    
    # Data types
    INT = "int"
    FLOAT = "float"
    
    # Mathmatic types
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    POWER = "**"
    DIV = "/"
    DIVREST = "%"
    
    # Parenthesis
    LPAREN = "("
    RPAREN = ")"
    
    # Conditional types
    EE = "=="
    NE = "!="
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="   
    
    # Other
    COMMA = ","
    ARROW = "->"
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
            strRepr += f":{self.value}>"
        else:
            strRepr += ">"
        return strRepr
