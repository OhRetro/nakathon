from sys import argv
from components.wrapper import run, run_external

VERSION = [1,0,0]
fn = len(argv) > 1

if not fn:
    print(f"Welcome to Nakathon v{".".join([str(x) for x in VERSION])}")
    while True:
        text = input("Nakathon Shell > ")
        if not text.strip(): continue 
        result, error = run("<stdin>", text)
            
        if error: print(error.as_string())
        elif result: 
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))
else:
    result, error = run_external(argv[1])
        
    if error: print(error.as_string())
    elif result: 
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))
