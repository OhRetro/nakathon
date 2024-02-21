from ..token import TokenType, Keyword
from .strings_template import (CONDITION, EXPRESSION, VARIABLE,
                      START_VALUE, END_VALUE, STEP_VALUE,
                      VAR_NAME_EXAMPLE, FUNC_NAME_EXAMPLE, VAR_FUNC_NAME_EXAMPLE)

def token(name: str): return TokenType[name].value
def key(name: str): return Keyword[name].value
def tab_space(): return " " * 4

# Set Function
FUNC_SYNTAX_IN_LINE = f"{key("SETFUNCTION")} {FUNC_NAME_EXAMPLE}() {token("ARROW")} {EXPRESSION}"

FUNC_SYNTAX = f"""{key("SETFUNCTION")} {FUNC_NAME_EXAMPLE}() {{
    {EXPRESSION}
}}"""


# If 
IF_ELSEIF_ELSE_SYNTAX_IN_LINE = f"if {CONDITION} {{ {EXPRESSION} }} elseif {CONDITION} {{ {EXPRESSION} }} else {{ {EXPRESSION} }}"

IF_ELSEIF_ELSE_SYNTAX = f"""if {CONDITION} {{
    {EXPRESSION}
}} else if {{
    {EXPRESSION}
}} else {{
    {EXPRESSION}
}}"""


# For
FOR_SYNTAX_IN_LINE = f"for {VARIABLE} = {START_VALUE} to {END_VALUE} step {STEP_VALUE} {{ {EXPRESSION} }}"

FOR_SYNTAX = f"""for {VARIABLE} = {START_VALUE} to {END_VALUE} step {STEP_VALUE} {{
    {EXPRESSION}
}}"""


# While
WHILE_SYNTAX_IN_LINE = f"while {CONDITION} {{ {EXPRESSION} }}"

WHILE_SYNTAX = f"""while {CONDITION} {{
    {EXPRESSION}
}}"""