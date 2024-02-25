from os import system

def make_executable(version: list[int]):
    options = "--standalone --onefile"
    options += " --company-name=OhRetro"
    options += " --product-name=Nakathon"
    options += f" --file-version={version}"
    options += " --output-dir=build/"
    options += " --windows-icon-from-ico=logo.ico"

    system(f"nuitka {options} nakathon.py")