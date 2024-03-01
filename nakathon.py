from sys import argv
from components.utils.misc import get_abs_path
from components.wrapper import run, set_global
from components.datatypes.all import String
from components.utils.misc import set_console_title

VERSION = [1, 5, 0]

def start():
    theres_args = len(argv) > 1
    is_running_a_script = theres_args and not argv[1].startswith("--")
    _version = ".".join([str(x) for x in VERSION])
    
    set_global("NAKATHON_VERSION", String(f"v{_version}"))

    set_console_title(f"Nakathon v{_version}")
    
    if not is_running_a_script and not theres_args:
        print(f"Welcome to Nakathon v{_version}")
        while True:
            try:
                text = input("Nakathon Shell > ")
                if not text.strip(): continue 
                result, error = run("<stdin>", text, "<Shell>")
                    
                if error: print(error.as_string())
                elif result: 
                    if len(result.elements) == 1:
                        print(repr(result.elements[0]))
                    else:
                        print(repr(result))
            except KeyboardInterrupt:
                print("\nExiting...")
                break
                    
    elif is_running_a_script:
        fn = argv[1]
        try:
            with open(fn, "r", encoding="utf-8") as f:
                script = f.read()
        except Exception as e:
            raise Exception(
                f"Failed to load script \"{fn}\"\n" + str(e)
            )

        _, error = run(fn, script, "<External>", True, cwd=get_abs_path(fn))
        if error: print(error.as_string())
                
    elif not is_running_a_script and theres_args:
        if argv[1] == "--version":
            print(f"v{_version}")

if __name__ == "__main__":
    start()
