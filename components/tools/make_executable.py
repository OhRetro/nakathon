from os import system

def make_executable(version: list[int]):
    options = [
        "--standalone",
        "--onefile",
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
    
    