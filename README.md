
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
python nakathon.py .\file_name.nkt # Windows
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
var variable_name = <value> or <expression>

# You can also set a immutable, also known as a constant, variable using the 'const' keyword
const VARIABLE_NAME = <value> or <expression>

# There's also temporary variable using the 'temp' keyword
temp variable_name <value-of-type-int> = <value> or <expression>

# You can also set a scoped, or local, variable using the 'local' keyword
local variable_name = <value> or <expression>

# To define & execute a function follow the syntax below
func FunctionName() -> <expression>

func FunctionName() {
    <expression>
}

```

### Built-in functions

```py
# Print, used to print the value inside the function
Print(value: Any)

# Input, used to get user input text
Input(prompt: String = "> ")

# InputNumber, used to get user input number, either int or float
InputNumber(prompt: String = "> ")

# Clear, used to clear the terminal
Clear()

# To Functions, used to convert a value into a string
ToString(value: Any)

# Is Functions, used to know if the inputed value is that data type
IsNumber(value: Any)
IsString(value: Any)
IsList(value: Any)
IsFunction(value: Any)
IsBoolean(value: Any)
IsNull(value: Any)

# List Functions, used to alter a list type (examples are down below)
ListAppend(list: List, value: Any)
ListPop(list: List, index: Number)
ListExtend(list: List, list: List)
ListLen(list: List)

# Random Functions
Random()
RandomInt(min: Number, max: Number)
RandomFloat(min: Number, max: Number)

# Misc Functions
Import(filename: String, namespace: String)
Run(filename: String)
Exit(code_number: Number = 0)

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
["Hello!", 43, -20, 3.14] - 2 # -> ["Hello!", 43, 3.14]
# or
var list = ["Hello!", 43, -20, 3.14] # -> ["Hello!", 43, -20, 3.14]
ListPop(list, 2) # -> -20
list # -> ["Hello!", 43, 3.14]

# list merge with another list
[1 , 2, 3] * [4, 5, 6] # -> [1, 2, 3, 4, 5, 6]
# or
var list = [1, 2, 3] # -> [1, 2, 3]
ListExtend(list, [4, 5, 6]) # -> [1, 2, 3, 4, 5, 6]
list # -> [1, 2, 3, 4, 5, 6]

# list returning a item by it's index
["Hello!", "this", "is", "a", "list"] / 1 # -> "this"

# list getting list's length
ListLen(["Hello!", "this", "is", "a", "list"]) # -> 5

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

### Assign Operators

```py
# plus equals
var var_name += 1 

# minus equals
var var_name -= 1 

# multiplication equals
var var_name *= 1 

# division equals
var var_name /= 1 

# power equals
var var_name **= 1 

# rest of division equals
var var_name %= 1 

```

### For & While Loops

```py
# To use the For Loop follow the syntax below
for <variable> = <start-value> ; <end-value> ; <step-value> {
    <expression>
}

# To use the While Loop follow the syntax below
while <condition> {
    <expression>
}

```
