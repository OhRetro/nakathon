import wrapper


while True:
    text = input("NakaThon Shell > ")
    result, error = wrapper.run("<stdin>", text)
    
    if error:
        print(error.as_string())
    else:
        print(result)
