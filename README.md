
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
var variable_name = <value> or <expression>

# You can also set a immutable, also known as a constant, variable using the 'const' keyword
const variable_name = <value> or <expression>

# There's also temporary variable using the 'temp' keyword
temp variable_name <value-of-type-int> = <value> or <expression>

# To define & execute a function follow the syntax below
func FunctionName() {
    <expression>
}

# To set & execute a variable function follow the syntax below
var varFunc = func () -> <expression> # -> Variable Function
varFunc() # -> <value>

```

### Built-in functions

```py
# Print, used to print the value inside the function
Print(<value> or <expression>)

# InputString, used to get user input text
InputString()

# InputNumber, used to get user input number, either int or float
InputNumber()

# Clear, used to clear the terminal
Clear()

# Is Functions, used to know if the inputed value is that data type
IsNumber(<value> or <expression>)
IsString(<value> or <expression>)
IsList(<value> or <expression>)
IsFunction(<value> or <expression>)

# List Functions, used to alter a list type (examples are down below)
ListAppend(list, value)
ListPop(list, index)
ListExtend(list, list)

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
10 / 2 # -> 5.0

# Power
2 ** 10 # -> 1024

# Rest of Division
11 % 2 # -> 1

# Parentheses
(4 + 1) * 2 # -> 10

```

### String Methods

```py
# string concatenation
"Hello," + "world!" # -> "Hello,world!"

"Hello, world! " * 2 # -> "Hello, world! Hello, world! "

```

### List Methods

```py
# list pushing a new item
[] + 1 # -> [1]
# or
var list = [] # -> []
ListAppend(list, 1) # -> [1]
list # -> [1]

# list removing item by it's index
["Hello!", 43, -20, 3.14] - 2 # -> [Hello!, 43, 3.14]
# or
var list = ["Hello!", 43, -20, 3.14] # -> [Hello!, 43, -20, 3.14]
ListPop(list, 2) # -> -20
list # -> [Hello!, 43, 3.14]

# list merge with another list
[1 , 2, 3] * [4, 5, 6] # -> [1, 2, 3, 4, 5, 6]
# or
var list = [1, 2, 3] # -> [1, 2, 3]
ListExtend(list, [4, 5, 6]) # -> [1, 2, 3, 4, 5, 6]
list # -> [1, 2, 3, 4, 5, 6]

# list returning a item by it's index
["Hello!", "this", "is", "a", "list"] / 1 # -> "this"

```

### Conditions

```py
# is equals
1 == 1 # -> true

# is not equals
1 != 2  # -> true

# is less than
1 < 2 # -> true

# is greater than
1 > 0 # -> true

# is less than or equals
-1 <= 1 # -> true

# is greater than or equals
1 >= 10  # -> false

# and
1 == 1 && 10 != 10 # -> false

# or
2 == 3 || 10 != 9 # -> true

# if, else if and else
if <condition> {
    <expression>
} else if {
    <expression>
} else {
    <expression>
}

```

### For & While Loops

```py
# To use the For Loop follow the syntax below
for <variable> = <start-value> to <end-value> step <step-value> {
    <expression>
}

# To use the While Loop follow the syntax below
while <condition> {
    <expression>
}

```
