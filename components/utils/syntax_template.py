from ..token import TokenType, Keyword
from .strings_template import (CONDITION, EXPRESSION, VARIABLE,
                      START_VALUE, END_VALUE, STEP_VALUE,
                      VAR_NAME_EXAMPLE, FUNC_NAME_EXAMPLE,
                      VALUE_EXPRESSION, VALUE_OF)

def token(name: str): return TokenType[name].value
def key(name: str): return Keyword[name].value

# Set Variables/Function
VAR_SYNTAX = f"{key('SETVAR')} {VAR_NAME_EXAMPLE} = {VALUE_EXPRESSION}"
CONST_SYNTAX = f"{key('SETIMMUTABLEVAR')} {VAR_NAME_EXAMPLE} = {VALUE_EXPRESSION}"
TEMP_SYNTAX = f"{key('SETTEMPVAR')} {VAR_NAME_EXAMPLE} {VALUE_OF.format('int')} = {VALUE_EXPRESSION}"
LOCAL_SYNTAX = f"{key('SETSCOPEDVAR')} {VAR_NAME_EXAMPLE} = {VALUE_EXPRESSION}"

FUNC_SYNTAX_IN_LINE = f"{key('SETFUNCTION')} {FUNC_NAME_EXAMPLE}() {token('ARROW')} {EXPRESSION}"

FUNC_SYNTAX = f"""{key('SETFUNCTION')} {FUNC_NAME_EXAMPLE}() {{
    {EXPRESSION}
}}"""


# If 
IF_ELSEIF_ELSE_SYNTAX = f"""if {CONDITION} {{
    {EXPRESSION}
}} else if {{
    {EXPRESSION}
}} else {{
    {EXPRESSION}
}}"""


# For
FOR_SYNTAX = f"""for {VARIABLE} = {START_VALUE} ; {END_VALUE} ; {STEP_VALUE} {{
    {EXPRESSION}
}}"""


# While
WHILE_SYNTAX = f"""while {CONDITION} {{
    {EXPRESSION}
}}"""