from .Value import Value
from .Number import Number
from .String import String
from .List import List
from .Boolean import Boolean
from .Null import Null
from .Function import Function, BaseFunction
from .BuiltInFunction import BuiltInFunction
from .Class import Class
from .Object import Object
from .Instance import Instance

def make_value_type(name: str) -> Value:
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
        "BuiltInFunction": Function,
        "Class": Class
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
    "make_value_type",
    "make_value"
    "Value",
    "Number",
    "String",
    "List",
    "Boolean",
    "Null",
    "BaseFunction",
    "Function",
    "BuiltInFunction",
    "Class"
]