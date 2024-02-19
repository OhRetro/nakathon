import wrapper

while True:
    text = input("Nakathon Shell > ")
    if not text.strip(): continue 
    result, error = wrapper.run("<stdin>", text)
        
    if error: print(error.as_string())
    elif result: 
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))
