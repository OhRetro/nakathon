from ..keyword import Keyword
from ..utils.syntax_template import (WHILE_SYNTAX, FOR_SYNTAX, IF_ELSEIF_ELSE_SYNTAX, FUNC_SYNTAX, LOCAL_SYNTAX,
                                             VAR_SYNTAX, CONST_SYNTAX, TEMP_SYNTAX, VALUE_EXPRESSION, FUNC_SYNTAX_IN_LINE)
from ..wrapper import run

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
    src="https://ohretro.vercel.app/images/nakathon/logo.png" 
    alt="Logo Parody of Python">
</img>

<p style="text-align: center;">
An Interpreted Programming Language made with Python; <br>
with the purpose of to learn and how an interpreted language works.<br>
Syntax based on other languages like JavaScript, C# and etc. <br>
    <a href="https://marketplace.visualstudio.com/items?itemName=ohretro-naka.nakathon-syntax-highlight">
        VSCode Nakathon Syntax Highlight Extension
    </a>
</p>

## Usage

### Running Nakathon

```py
# To run Nakathon you use the following command
python nakathon.py # Windows
python3 nakathon.py # Linux, Mac

# Just like in Python, if you run as is, you will go to the shell
# but if you put file that ends with .nkt, Nakathon will run it
python nakathon.py .\\file_name.nkt # Windows
python3 nakathon.py ./file_name.nkt # Linux, Mac

# If you have the .exe, instead of "python nakathon.py" write "nakathon.exe".

```

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

# You can also set a scoped, or local, variable using the 'local' keyword
{LOCAL_SYNTAX}

# To define & execute a function follow the syntax below
{FUNC_SYNTAX_IN_LINE}

{FUNC_SYNTAX}

```

### Built-in functions

```py
# Print, used to print the value inside the function
Print({VALUE_EXPRESSION})

# Input, used to get user input text
Input(prompt: String = "> ")

# InputNumber, used to get user input number, either int or float
InputNumber(prompt: String = "> ")

# Clear, used to clear the terminal
Clear()

# To Functions, used to convert a value into a string
ToString({VALUE_EXPRESSION})

# Is Functions, used to know if the inputed value is that data type
IsNumber({VALUE_EXPRESSION})
IsString({VALUE_EXPRESSION})
IsList({VALUE_EXPRESSION})
IsFunction({VALUE_EXPRESSION})
IsBoolean({VALUE_EXPRESSION})
IsNull({VALUE_EXPRESSION})

# List Functions, used to alter a list type (examples are down below)
ListAppend(list: List, value: Value)
ListPop(list: List, index: Number)
ListExtend(list: List, list: List)
ListLen(list: List)

# Random Functions
Random()
RandomInt(min: Number, max: Number)
RandomFloat(min: Number, max: Number)

# Misc Functions
Import(filename: string)
Run(filename: string)
Exit(code_number: Number = 0)

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

# list getting list's length
{build_src_and_output('ListLen(["Hello!", "this", "is", "a", "list"])')}

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

### Assign Operators

```py
# plus equals
{build_src_and_output("var var_name += 1", False)}

# minus equals
{build_src_and_output("var var_name -= 1", False)}

# multiplication equals
{build_src_and_output("var var_name *= 1", False)}

# division equals
{build_src_and_output("var var_name /= 1", False)}

# power equals
{build_src_and_output("var var_name **= 1", False)}

# rest of division equals
{build_src_and_output("var var_name %= 1", False)}

```

### For & While Loops

```py
# To use the For Loop follow the syntax below
{FOR_SYNTAX}

# To use the While Loop follow the syntax below
{WHILE_SYNTAX}

```
'''

def make_readme():
    generate_md_file(content)
    
if __name__ == "__main__":
    make_readme()
    