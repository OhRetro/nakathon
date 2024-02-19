from components.token import TokenType, Keyword

def generate_md_file(content):
    try:
        with open("README.md", "w", encoding="utf-8") as file:
            file.write(content)
        print(f"README.md generated")
    except Exception as e:
        print(f"Error: {e}")

content = f'''
# Nakathon (WIP)

An Interpreted Programming Language made with Python;  
with the purpose of to learn and how an interpreted language works;  
based on the BASIC syntax.

## Usage

note: there's no actual comment syntax implemented yet

note: the only way to execute the expression at the moment is by the shell.py

### Data Types

```py
# int
1
{TokenType.MINUS.value}1

# float
1.0
{TokenType.MINUS.value}1.0

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
{Keyword.SETIMMUTABLEVAR.value} pi = 3.14

# There's also temporary variable using the 'temp' keyword
{Keyword.SETTEMPVAR.value} temp_var 2 = "I'm going stop to exist once I'm referenced 2 times"
temp_var # -> "I'm going stop to exist once I'm referenced 2 times"
temp_var # -> "I'm going stop to exist once I'm referenced 2 times"
temp_var # -> Error: temp_var not defined
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
Print("Hello, world!") -> Hello, world!

# InputString, used to get user input text
InputString() -> <what the user typed>

# InputNumber, used to get user input number, either int or float
InputNumber() -> <what the user typed>

# Clear, used to clear the terminal
Clear() -> null

# Is Functions, used to know if the inputed value is that data type
IsNumber(1.1) -> true
IsString(5) -> false
IsList([]) -> true
IsFunction(Print) -> true

# List Functions, used to alter a list type (examples are down below)
ListAppend()
ListPop()
ListExtend()

```

### Number Methods (Mathematics & Arithmetic)

```py
# Addition
5 {TokenType.PLUS.value} 5 # -> 10

# Subtraction
10 {TokenType.MINUS.value} 0.5 # -> 9.5

# Multiplication
2 {TokenType.MUL.value} 10 # -> 20

# Division
10 {TokenType.DIV.value} 2 # -> 5

# Power
2 {TokenType.POWER.value} 10 # -> 1024

# Rest of Division
11 {TokenType.DIVREST.value} 2 # -> 1

# Parentheses
(4 {TokenType.PLUS.value} 1) {TokenType.MUL.value} 2 # -> 10

```

### String Methods

```py
# string concat
"Hello, " {TokenType.PLUS.value} "World!" # -> "Hello, World!"

# string repeat
"Hello, World!" {TokenType.MUL.value} 2 # -> "Hello, World!Hello, World!"

```

### List Methods

```py
# list pushing a new item
[] {TokenType.PLUS.value} 1 # -> [1]
# or
{Keyword.SETVAR.value} list = []
ListAppend(list, 1) # -> [1]
list # -> [1]

# list removing item by it's index
["Hello!", 43, {TokenType.MINUS.value}20, 3.14] {TokenType.MINUS.value} 2 # -> ["Hello!", 43, 3.14]
# or
{Keyword.SETVAR.value} list = ["Hello!", 43, {TokenType.MINUS.value}20, 3.14]
ListPop(list, 2) # -> {TokenType.MINUS.value}20
list # -> ["Hello!", 43, 3.14]

# list merge with another list
[1 , 2, 3] {TokenType.MUL.value} [4, 5, 6] # -> [1, 2, 3, 4, 5, 6]
# or
{Keyword.SETVAR.value} list = [1, 2, 3]
ListExtend(list, [4, 5, 6]) # -> [1, 2, 3, 4, 5, 6]
list # -> [1, 2, 3, 4, 5, 6]

# list returning a item by it's index
["Hello!", "this", "is", "a", "list"] {TokenType.DIV.value} 1 # -> "this"

```

### Conditions

```py
# is equals
1 {TokenType.EE.value} 1 # -> 1

# is not equals
1 {TokenType.NE.value} 1 # -> 0

# is less than
1 {TokenType.LT.value} 2 # -> 1

# is greater than
1 {TokenType.GT.value} 0 # -> 1

# is less than or equals
{TokenType.MINUS.value}1 {TokenType.LTE.value} 1 # -> 1

# is greater than or equals
1 {TokenType.GTE.value} 10 # -> 0

# and
1 {TokenType.EE.value} 1 {Keyword.AND.value} 10 {TokenType.NE.value} 10 # -> 0

# or
2 {TokenType.EE.value} 3 {Keyword.OR.value} 10 {TokenType.NE.value} 9 # -> 1

# if, else if and else
{Keyword.IF.value} <condition> {Keyword.THEN.value} <expression> {Keyword.ELSEIF.value} <condition> {Keyword.THEN.value} <expression> {Keyword.ELSE.value} <expression>

```

### While & For Loops

```py
# To use the While Loop follow the syntax below
{Keyword.WHILE.value} <condition> {Keyword.THEN.value} <expression>

# Example of While Loop
{Keyword.SETVAR.value} i = 0
{Keyword.SETVAR.value} numbers = {Keyword.WHILE.value} i < 100 {Keyword.THEN.value} {Keyword.SETVAR.value} i = i {TokenType.PLUS.value} 1 # -> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers # -> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
i # -> 10

# To use the For Loop follow the syntax below
{Keyword.FOR.value} <var_name> = <start_value> {Keyword.TO.value} <end_value> {Keyword.THEN.value} <expression>
# Or define step count
{Keyword.FOR.value} <var_name> = <start_value> {Keyword.TO.value} <end_value> {Keyword.STEP.value} <step_value> {Keyword.THEN.value} <expression>

# Example of For Loop
{Keyword.SETVAR.value} numbers = {Keyword.FOR.value} i = 0 {Keyword.TO.value} 10 {Keyword.THEN.value} i # -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
numbers # -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
i # -> 9

```
'''

generate_md_file(content)