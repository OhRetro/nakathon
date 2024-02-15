import run

while True:
    text = input("NakaThon Shell > ")
    result, error = run.run("<stdin>", text)

    if error:
        print(error.as_string())
    else:
        print(result)
