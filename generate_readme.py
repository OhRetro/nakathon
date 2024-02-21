from components.token import TokenType, Keyword
from components.utils.syntax_template import (WHILE_SYNTAX, FOR_SYNTAX, IF_ELSEIF_ELSE_SYNTAX, FUNC_SYNTAX,
                                             VAR_SYNTAX, CONST_SYNTAX, TEMP_SYNTAX, VALUE_EXPRESSION, VALUE_OF)
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

## COMMENTS CRASHES THE INTERPRETER, DON'T USE THEM

## Usage

To Run on the shell run the following command: `python nakathon.py`  
To Run an external file run the following command: `python nakathon.py *file*.nk`

### Data Types

```py
# int
1

# float
1.0

# string
"String"

# list
[]

```

### Variables & Functions

The Variable/Function name can be in ``snake_case``, ``camelCase`` or ``PascalCase``

```py
# To set & refer a variable follow the syntax below
{VAR_SYNTAX}

# You can also set a immutable, also known as a constant, variable using the 'const' keyword
{CONST_SYNTAX}

# There's also temporary variable using the 'temp' keyword
{TEMP_SYNTAX}

# To define & execute a function follow the syntax below
{FUNC_SYNTAX}

# To set & execute a variable function follow the syntax below
{Keyword.SETVAR.value} varFunc = func () -> <expression> # -> Variable Function
varFunc() # -> <value>

```

### Built-in functions

```py
# Print, used to print the value inside the function
Print({VALUE_EXPRESSION})

# InputString, used to get user input text
InputString()

# InputNumber, used to get user input number, either int or float
InputNumber()

# Clear, used to clear the terminal
Clear()

# Is Functions, used to know if the inputed value is that data type
IsNumber({VALUE_EXPRESSION})
IsString({VALUE_EXPRESSION})
IsList({VALUE_EXPRESSION})
IsFunction({VALUE_EXPRESSION})

# List Functions, used to alter a list type (examples are down below)
ListAppend(list, value)
ListPop(list, index)
ListExtend(list, list)

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
# string concatenation
{build_src_and_output('"Hello," + "world!"')}

{build_src_and_output('"Hello, world! " * 2')}

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