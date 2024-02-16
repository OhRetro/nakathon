def expected_symbols(list):
    error_message_str = "Expected "
    expected_chars = list
    
    if len(expected_chars) < 2:
        error_message_str += f"'{expected_chars[0].value}'"
        return error_message_str
    
    for i in expected_chars:
        if i != expected_chars[-1] and i != expected_chars[-2]:
            error_message_str += f"'{i.value}', "
        else:
            break
        
    error_message_str += f"'{expected_chars[-2].value}' or '{expected_chars[-1].value}'"
    
    return error_message_str

