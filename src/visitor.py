symbol_table = {}
function_table = {
    "random_operation": (1, 2)
}

def visitor_function_call(call):
    if call[1] in function_table:
        if len(call[2]) == len(function_table[call[1]]):
            result = call [1] + "("
            first = True
            for i in call[2]:
                if not first:
                    result +=  ", " + str(i[1])
                else:
                    result += str(i[1])
                    first = False
            result += ");\n"
            return result
        else:
            print(f"Error Not enough parameters to call {call[1]}")
    else:
        print(f"Error: {call[1]} does not exist")