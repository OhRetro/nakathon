from enum import Enum

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