from sys import argv
from components.wrapper import run, run_external

VERSION = [1,1,1]

theres_args = len(argv) > 1
is_running_a_script = theres_args and not argv[1].startswith("--") and argv[1].endswith(".nkt")

if not is_running_a_script and not theres_args:
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
elif is_running_a_script:
    result, error = run_external(argv[1])
        
    if error: print(error.as_string())
    elif result: 
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))
            
elif not is_running_a_script and theres_args:
    if "--readme" in argv:
        from components.tools.make_readme import make_readme
        make_readme()
        
    if "--exec" in argv:
        from components.tools.make_executable import make_executable
        make_executable(VERSION)
