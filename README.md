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

# You can also set a immutable, also known as constant, variable using the 'const' keyword
const pi = 3.14
# not implemented yet, the concept is there

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
var numbers = WHILE i < 100 then var i = i + 1 # -> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers # -> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
i # -> 10

# To use the For Loop follow the syntax below
for <var_name> = <start_value> to <end_value> then <expression>
# Or to define step count
for <var_name> = <start_value> to <end_value> step <step_value> then <expression>

# Example of For Loop
var numbers = for i = 0 to 10 then i # -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
numbers # -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
i # -> 9

```

### Not Documented Yet (IGNORE)

global_symbol_table.set("PRINT", BuiltInFunction.print)
global_symbol_table.set("PRINT_RET", BuiltInFunction.print_ret)
global_symbol_table.set("INPUT", BuiltInFunction.input)
global_symbol_table.set("INPUT_INT", BuiltInFunction.input_int)
global_symbol_table.set("CLEAR", BuiltInFunction.clear)
global_symbol_table.set("IS_NUM", BuiltInFunction.is_number)
global_symbol_table.set("IS_STR", BuiltInFunction.is_string)
global_symbol_table.set("IS_LIST", BuiltInFunction.is_list)
global_symbol_table.set("IS_FUN", BuiltInFunction.is_function)
