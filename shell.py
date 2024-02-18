import wrapper

while True:
    text = input("Nakathon Shell > ")
    if not text: continue 
    result, error = wrapper.run("<stdin>", text)
        
    if error: print(error.as_string())
    elif result: print(result)
