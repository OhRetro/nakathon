from .value import Value
from .number import Number
from .string import String
from .list import List
from .boolean import Boolean
from .null import Null
from .function import Function, BaseFunction
from .builtin_function import BuiltInFunction

def make_value_type(name: str):
    map = {
        "Value": Value,
        "Any": Value,
        "Number": Number,
        "Int": Number,
        "Float": Number,
        "String": String,
        "List": List,
        "Boolean": Boolean,
        "Bool": Boolean,
        "Null": Null,
        "BaseFunction": Function,
        "Function": Function,
        "BuiltInFunction": Function
    }
    
    return map.get(name, None)

def make_value(value):
    map = {
        int: Number,
        float: Number,
        str: String,
        list: List,
        bool: Boolean,
    }
    
    for k, v in map.items():
        if isinstance(value, k): return v(value)
        
    return None

__all__ = [
    Value,
    Number,
    String,
    List,
    Boolean,
    Null,
    BaseFunction,
    Function,
    BuiltInFunction
]