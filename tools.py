from sys import argv
from nakathon import __version__ as nkt_version
from components.tools.make_readme import make_readme
from components.tools.make_executable import make_executable

_version = ".".join([str(x) for x in nkt_version])

tool_map = {
    "readme": (make_readme, ()),
    "exec": (make_executable, ([_version]))
}

if len(argv) > 1:
    if argv[1] != "all":
        _function = tool_map[argv[1]][0]
        _args = tool_map[argv[1]][1]
        _function(*_args)

    else:
        for _, v in tool_map.items():
            _function = v[0]
            _args = v[1]
            _function(*_args)

else:
    print("All available tools:")
    print("\n".join(tool_map.keys()))