def convert_to_snake_case(input_string: str) -> str:
    result = ""
    for char in input_string:
        if char.isupper():
            result += "_" + char.lower()
        else:
            result += char

    if result.startswith("_"):
        result = result[1:]
    return result

def index_exists(list_or_tuple: list | tuple, index: int) -> bool:
    try:
        _ = list_or_tuple[index]
        return True
    except IndexError:
        return False
    
def fill_default_args(input_args, defaults, arg_names):
    new_args = [None] * len(arg_names)
    
    print(f"new {new_args}")
    print(f"arg names {arg_names}")
    print(f"arg default {defaults}")
    print(f"input {input_args}")
    
    for i in range(len(new_args)):
        if index_exists(defaults, i):
            new_args[i] = defaults[i]
            
        if index_exists(input_args, i) and (new_args[i] is None):
            new_args[i] = input_args[i]
    
    print(f"new after {new_args}")
    return new_args
                    
def try_get(list, ind, default = None):
    if index_exists(list, ind):
        return list[ind]
    return default
        
        