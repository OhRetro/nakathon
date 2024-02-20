from components.token import TokenType, Keyword
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
    return results if results is not None else error.as_string_simple()

def build_src_and_output(command: str, show_output: bool = True):
    return f"{command} " + f"# -> {simulate_code(command)}" if show_output else ""

content = f'''
# Nakathon (WIP)

An Interpreted Programming Language made with Python;  
with the purpose of to learn and how an interpreted language works

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
{Keyword.SETVAR.value} var_name = <value> # -> <value>
var_name # -> <value>

# You can also set a immutable, also known as a constant, variable using the 'const' keyword
{build_src_and_output(f"{Keyword.SETIMMUTABLEVAR.value} pi = 3.14")}

# There's also temporary variable using the 'temp' keyword
{build_src_and_output(f'{Keyword.SETTEMPVAR.value} temp_var 2 = "I\'m going to stop existing once I\'m referenced 2 times"')}
{build_src_and_output("temp_var")}
{build_src_and_output("temp_var")}
{build_src_and_output("temp_var")}
# The number after the 'temp_var' is the lifetime of the variable, 
# every time it's referenced the lifetime decreases with the exception of the initial reference
# which is while initializing the variable

# To define & execute a function follow the syntax below
{Keyword.SETFUNCTION.value} FuncName() -> <expression> # -> Function
FuncName() # -> <value>

# To define & execute a function with args follow the syntax below
{Keyword.SETFUNCTION.value} FuncName(arg) -> <expression> # -> Function
FuncName(<value>) # -> <value>

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
{build_src_and_output(f"1 {TokenType.EE.value} 1")}

# is not equals
{build_src_and_output(f"1 {TokenType.NE.value} 2 ")}

# is less than
{build_src_and_output(f"1 {TokenType.LT.value} 2")}

# is greater than
{build_src_and_output(f"1 {TokenType.GT.value} 0")}

# is less than or equals
{build_src_and_output(f"{TokenType.MINUS.value}1 {TokenType.LTE.value} 1")}

# is greater than or equals
{build_src_and_output(f"1 {TokenType.GTE.value} 10 ")}

# and
{build_src_and_output(f"1 {TokenType.EE.value} 1 {Keyword.AND.value} 10 {TokenType.NE.value} 10")}

# or
{build_src_and_output(f"2 {TokenType.EE.value} 3 {Keyword.OR.value} 10 {TokenType.NE.value} 9")}

# if, else if and else
{Keyword.IF.value} <condition> {Keyword.THEN.value} <expression> {Keyword.ELSEIF.value} <condition> {Keyword.THEN.value} <expression> {Keyword.ELSE.value} <expression>

```

### While & For Loops

```py
# To use the While Loop follow the syntax below
{Keyword.WHILE.value} <condition> {Keyword.THEN.value} <expression>

# Example of While Loop
{build_src_and_output(f"{Keyword.SETVAR.value} i = 0")}
{build_src_and_output(f"{Keyword.SETVAR.value} numbers = {Keyword.WHILE.value} i < 10 {Keyword.THEN.value} {Keyword.SETVAR.value} i = i {TokenType.PLUS.value} 1")}
{build_src_and_output("numbers")}
{build_src_and_output("i")}

# To use the For Loop follow the syntax below
{Keyword.FOR.value} <var_name> = <start_value> {Keyword.TO.value} <end_value> {Keyword.THEN.value} <expression>
# Or define step count
{Keyword.FOR.value} <var_name> = <start_value> {Keyword.TO.value} <end_value> {Keyword.STEP.value} <step_value> {Keyword.THEN.value} <expression>

# Example of For Loop
{build_src_and_output(f"{Keyword.SETVAR.value} numbers = {Keyword.FOR.value} i = 0 {Keyword.TO.value} 10 {Keyword.THEN.value} i")}
{build_src_and_output("numbers")}
{build_src_and_output("i")}

```
'''

generate_md_file(content)