from os import system

def make_executable(version: list[int]):
    options = "--standalone --onefile --follow-imports"
    options += " --company-name=OhRetro"
    options += " --product-name=Nakathon"
    options += f" --file-version={version}"
    
    options += " --windows-icon-from-ico=logo.ico"

    system(f"nuitka {options} nakathon.py")