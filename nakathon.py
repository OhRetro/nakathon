from sys import argv
from components.wrapper import run, set_global
from components.values.all import String

VERSION = [1,3,0]

def start():
    theres_args = len(argv) > 1
    is_running_a_script = theres_args and not argv[1].startswith("--")
    _version = ".".join([str(x) for x in VERSION])
    
    set_global("NAKATHON_VERSION", String(f"v{_version}"))

    if not is_running_a_script and not theres_args:
        print(f"Welcome to Nakathon v{_version}")
        while True:
            text = input("Nakathon Shell > ")
            if not text.strip(): continue 
            result, error = run("<stdin>", text, "<Shell>")
                
            if error: print(error.as_string())
            elif result: 
                if len(result.elements) == 1:
                    print(repr(result.elements[0]))
                else:
                    print(repr(result))
                    
    elif is_running_a_script:
        fn = argv[1]
        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            raise Exception(
                f"Failed to load script \"{fn}\"\n" + str(e)
            )

        _, error = run(fn, script, "<External>", True)
        if error: print(error.as_string())
                
    elif not is_running_a_script and theres_args:
        if "--readme" in argv:
            from components.tools.make_readme import make_readme
            make_readme()
            
        if "--exec" in argv:
            from components.tools.make_executable import make_executable
            make_executable(VERSION)

if __name__ == "__main__":
    start()
