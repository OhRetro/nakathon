from os import system
from datetime import date

def make_executable(version: list[int]):
    today = date.today()
    day_month = today.strftime("%d%m%y")

    options = [
        "--standalone",
        "--onefile",
        "--quiet",
        "--company-name=OhRetro",
        "--product-name=Nakathon",
        f"--file-version={version}",
        "--copyright=2023",
        f"--output-filename=nakathon_v{version}.{day_month}",
        "--output-dir=build/",
        "--windows-icon-from-ico=logo.ico"
    ]

    _options = " ".join(options)
    system(f"nuitka {_options} nakathon.py")
    
    