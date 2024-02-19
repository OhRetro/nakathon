
# Nakathon (WIP)

An Interpreted Programming Language made with Python;  
with the purpose of to learn and how an interpreted language works;  
based on the BASIC syntax.

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
var var_name = <value> # -> <value>
var_name # -> <value>

# You can also set a immutable, also known as a constant, variable using the 'const' keyword
const pi = 3.14

# There's also temporary variable using the 'temp' keyword
temp temp_var 2 = "I'm going stop to exist once I'm referenced 2 times"
temp_var # -> "I'm going stop to exist once I'm referenced 2 times"
temp_var # -> "I'm going stop to exist once I'm referenced 2 times"
temp_var # -> Error: temp_var not defined
# The number after the 'temp_var' is the lifetime of the variable, 
# every time it's referenced the lifetime decreases with the exception of the initial reference
# which is while initializing the variable

# To define & execute a function follow the syntax below
func FuncName() -> <expression> # -> Function
FuncName() # -> <value>

# To define & execute a function with args follow the syntax below
func FuncName(arg) -> <expression> # -> Function
FuncName(<value>) # -> <value>

# To set & execute a variable function follow the syntax below
var varFunc = func () -> <expression> # -> Variable Function
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
5 + 5 # -> 10

# Subtraction
10 - 0.5 # -> 9.5

# Multiplication
2 * 10 # -> 20

# Division
10 / 2 # -> 5

# Power
2 ** 10 # -> 1024

# Rest of Division
11 % 2 # -> 1

# Parentheses
(4 + 1) * 2 # -> 10

```

### String Methods

```py
# string concat
"Hello, " + "World!" # -> "Hello, World!"

# string repeat
"Hello, World!" * 2 # -> "Hello, World!Hello, World!"

```

### List Methods

```py
# list pushing a new item
[] + 1 # -> [1]
# or
var list = []
ListAppend(list, 1) # -> [1]
list # -> [1]

# list removing item by it's index
["Hello!", 43, -20, 3.14] - 2 # -> ["Hello!", 43, 3.14]
# or
var list = ["Hello!", 43, -20, 3.14]
ListPop(list, 2) # -> -20
list # -> ["Hello!", 43, 3.14]

# list merge with another list
[1 , 2, 3] * [4, 5, 6] # -> [1, 2, 3, 4, 5, 6]
# or
var list = [1, 2, 3]
ListExtend(list, [4, 5, 6]) # -> [1, 2, 3, 4, 5, 6]
list # -> [1, 2, 3, 4, 5, 6]

# list returning a item by it's index
["Hello!", "this", "is", "a", "list"] / 1 # -> "this"

```

### Conditions

```py
# is equals
1 == 1 # -> 1

# is not equals
1 != 1 # -> 0

# is less than
1 < 2 # -> 1

# is greater than
1 > 0 # -> 1

# is less than or equals
-1 <= 1 # -> 1

# is greater than or equals
1 >= 10 # -> 0

# and
1 == 1 && 10 != 10 # -> 0

# or
2 == 3 || 10 != 9 # -> 1

# if, else if and else
if <condition> then <expression> else if <condition> then <expression> else <expression>

```

### While & For Loops

```py
# To use the While Loop follow the syntax below
while <condition> then <expression>

# Example of While Loop
var i = 0
var numbers = while i < 100 then var i = i + 1 # -> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers # -> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
i # -> 10

# To use the For Loop follow the syntax below
for <var_name> = <start_value> to <end_value> then <expression>
# Or define step count
for <var_name> = <start_value> to <end_value> step <step_value> then <expression>

# Example of For Loop
var numbers = for i = 0 to 10 then i # -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
numbers # -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
i # -> 9

```
