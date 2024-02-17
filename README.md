# Nakathon (WIP)

An Interpreted Programming Language made with Python;  
with the purpose of to learn and how an interpreted language works;  
based on the BASIC syntax.

## Usage

note: there's no actual comment syntax implemented yet

note: the only way to execute the syntax at the moment is by the shell.py

### Data Types & Their Methods

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

### Int/Float Methods (Mathematics & Arithmetic)

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
[] + <value_type> # -> [<value_type>]

# list removing item by it's index
["Hello!", 43, -20, 3.14] - 2 # -> ["Hello!", 43, 3.14]

# list merge with another list
[1 , 2, 3] * [4, 5, 6] # -> [1, 2, 3, 4, 5, 6]

# list returning a item by it's index
["Hello!", "this", "is", "a", "list"] / 1 # -> "this"

```

### Variables & Functions

The Variable/Function name can be in ``snake_case``, ``camelCase`` or ``PascalCase``

```py
# To set & refer a variable follow the syntax below
VAR var_name = <value_type> # -> <value_type>
var_name # -> <value_type>

# To define & execute a function follow the syntax below
FUN funcName() -> <expression> # -> Function
funcName() # -> <value_type>

# To define & execute a function with args follow the syntax below
FUN FuncName(arg) -> <expression> # -> Function
FuncName(<value_type>) # -> <value_type>

# To set & execute a variable function follow the syntax below
VAR VarFunc = FUN () -> <expression> # -> Variable Function
VarFunc() # -> <value_type>

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
1 == 1 AND 10 != 10 # -> 0

# or
2 == 3 OR 10 != 9 # -> 1

```

### While & For Loops

```py
# To use the While Loop follow the syntax below
WHILE <condition> THEN <expression>

# Example of While Loop
VAR i = 0
VAR numbers = WHILE i < 100 THEN VAR i = i + 1 # -> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers # -> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
i # -> 10

# To use the For Loop follow the syntax below
FOR <var_name> = <start_value> TO <end_value> THEN <expression>
# Or to define step count
FOR <var_name> = <start_value> TO <end_value> STEP <step_value> THEN <expression>

# Example of For Loop
VAR numbers = FOR i = 0 TO 10 THEN i # -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
numbers # -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
i # -> 9

```
