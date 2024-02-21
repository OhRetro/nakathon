from components.token import TokenType, Keyword
from components.utils.syntax_template import (WHILE_SYNTAX_IN_LINE, FOR_SYNTAX_IN_LINE,
                                             WHILE_SYNTAX, FOR_SYNTAX,
                                             IF_ELSEIF_ELSE_SYNTAX_IN_LINE, IF_ELSEIF_ELSE_SYNTAX,
                                             FUNC_SYNTAX_IN_LINE, FUNC_SYNTAX)
from components.wrapper import run

def generate_md_file(content):
    try:
        with open("README.md", "w", encoding="utf-8") as file:
            file.write(content)
        print(f"README.md generated")
    except Exception as e:
        print(f"Error: {e}")

def simulate_code(command: str):
    results, error = run("generate_readme.py", command, "Generating README.md")
    if results is not None:
        results = results.value[0].__repr__() if len(results.value) <= 1 else results.value
        
    return results if results is not None else error.as_string_simple()

def build_src_and_output(command: str, show_output: bool = True):
    command_result = simulate_code(command)
    return f"{command} " + (f"# -> {command_result}" if show_output else "")

content = f'''
<img 
    style="display: block; 
           margin-left: auto;
           margin-right: auto;
           width: 100%;"
    src="./logo_parody.png" 
    alt="Logo Parody of Python">
</img>

<p style="text-align: center;">
An Interpreted Programming Language made with Python; <br>
with the purpose of to learn and how an interpreted language works.<br>
Syntax based on other languages like JavaScript, C# and etc.
</p>

## Usage

To Run on the shell run the following command: `python nakathon.py`  
To Run an external file run the following command: `python nakathon.py *file*.nk`

### Data Types

```py
# int
1
-1

# float
1.0
-1.0

# string
"Hello, World!"

# list
[]

```

### Variables & Functions

The Variable/Function name can be in ``snake_case``, ``camelCase`` or ``PascalCase``

```py
# To set & refer a variable follow the syntax below
{build_src_and_output(f'{Keyword.SETVAR.value} var_name = "Any of the Data types"')}
{build_src_and_output("var_name")}

# You can also set a immutable, also known as a constant, variable using the 'const' keyword
{build_src_and_output(f"{Keyword.SETIMMUTABLEVAR.value} pi = 3.14")}

# There's also temporary variable using the 'temp' keyword
{build_src_and_output(f'{Keyword.SETTEMPVAR.value} temp_var 2 = "I\'m going to stop existing once I\'m referenced 2 times"', 0)}
{build_src_and_output("temp_var")}
{build_src_and_output("temp_var")}
{build_src_and_output("temp_var")}
# The number after the 'temp_var' is the lifetime of the variable, 
# every time it's referenced the lifetime decreases with the exception of the initial reference
# which is while initializing the variable

# To define & execute a function follow the syntax below
{FUNC_SYNTAX}

# To set & execute a variable function follow the syntax below
{Keyword.SETVAR.value} varFunc = func () -> <expression> # -> Variable Function
varFunc() # -> <value>

```

### Built-in functions

```py
# Print, used to print the value inside the function
{build_src_and_output('Print("Hello, world!")')}

# InputString, used to get user input text
InputString() # -> <what the user typed>

# InputNumber, used to get user input number, either int or float
InputNumber() # -> <what the user typed>

# Clear, used to clear the terminal
Clear() # -> null

# To Functions, used to convert values into another value type
{build_src_and_output("ToString(1)")}

# Is Functions, used to know if the inputed value is that data type
{build_src_and_output("IsNumber(1.1)")}
{build_src_and_output('IsString("hi")')}
{build_src_and_output("IsList([])")}
{build_src_and_output("IsFunction(Print)")}

# List Functions, used to alter a list type (examples are down below)
ListAppend()
ListPop()
ListExtend()

```

### Number Methods (Mathematics & Arithmetic)

```py
# Addition
{build_src_and_output("5 + 5")}

# Subtraction
{build_src_and_output("10 - 0.5")}

# Multiplication
{build_src_and_output("2 * 10")}

# Division
{build_src_and_output("10 / 2")}

# Power
{build_src_and_output("2 ** 10")}

# Rest of Division
{build_src_and_output("11 % 2")}

# Parentheses
{build_src_and_output("(4 + 1) * 2")}

```

### String Methods

```py
# string concat
{build_src_and_output('"Hello, " + "world!"')}

# string repeat
{build_src_and_output('"Hello, world!" * 2')}

```

### List Methods

```py
# list pushing a new item
{build_src_and_output("[] + 1")}
# or
{build_src_and_output(f"{Keyword.SETVAR.value} list = []")}
{build_src_and_output("ListAppend(list, 1)")}
{build_src_and_output("list")}

# list removing item by it's index
{build_src_and_output('["Hello!", 43, -20, 3.14] - 2')}
# or
{build_src_and_output(f'{Keyword.SETVAR.value} list = ["Hello!", 43, -20, 3.14]')}
{build_src_and_output("ListPop(list, 2)")}
{build_src_and_output("list")}

# list merge with another list
{build_src_and_output("[1 , 2, 3] * [4, 5, 6]")}
# or
{build_src_and_output(f"{Keyword.SETVAR.value} list = [1, 2, 3]")}
{build_src_and_output("ListExtend(list, [4, 5, 6])")}
{build_src_and_output("list")}

# list returning a item by it's index
{build_src_and_output('["Hello!", "this", "is", "a", "list"] / 1')}

```

### Conditions

```py
# is equals
{build_src_and_output("1 == 1")}

# is not equals
{build_src_and_output("1 != 2 ")}

# is less than
{build_src_and_output("1 < 2")}

# is greater than
{build_src_and_output("1 > 0")}

# is less than or equals
{build_src_and_output("-1 <= 1")}

# is greater than or equals
{build_src_and_output("1 >= 10 ")}

# and
{build_src_and_output("1 == 1 && 10 != 10")}

# or
{build_src_and_output("2 == 3 || 10 != 9")}

# if, else if and else
{IF_ELSEIF_ELSE_SYNTAX}

```

### For & While Loops

```py
# To use the For Loop follow the syntax below
{FOR_SYNTAX}

# To use the While Loop follow the syntax below
{WHILE_SYNTAX}

```
'''

generate_md_file(content)