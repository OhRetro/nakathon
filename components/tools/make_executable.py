from os import system

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
        "--windows-icon-from-ico=logo.ico",
        "--remove-output" if "--keep-build" not in flags else "",
        "--run" if "--run" in flags else ""
    ]

    _options = " ".join(options)
    system(f"nuitka {_options} nakathon.py")
    
    