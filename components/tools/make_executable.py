from os import system, remove, path
from time import sleep

try:
    import nuitka
except ImportError:
    print("nuitka is not installed.")
    exit(-1)

def make_executable(version: list[int], flags: list[str] = []):
    options = [
        "--standalone",
        "--onefile",
        "--disable-cache=\"all\"",
        "--clean-cache=\"all\"",
        "--quiet",
        "--company-name=OhRetro",
        "--product-name=Nakathon",
        f"--file-version={version}",
        "--copyright=2023",
        f"--output-filename=nakathon_v{version}",
        "--output-dir=build/",
        "--windows-icon-from-ico=logo.ico"
    ]

    _options = " ".join(options)
    system(f"nuitka {_options} nakathon.py")
    
    