symbol_table = {"a" : {"value" : 0}}
function_table = {}
VALID_OPERATION_NODES = {
    "arithmetic_operation",
    "logical_operation",
    "relational_operation",
    "unary_operation",
    "function_call"
}

def check_if_str(data):
    return data[0] == "\"" and data[-1] == "\""

def check_if_var_exists(var):
    return var in symbol_table
    # TODO: Make it so this table can check if a variable is available in local scope

def get_symbol_value(symbol):
    print(symbol)
    symbol = str(symbol)
    return symbol_table[symbol]["value"]

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

def array_internal(array):
    first = True
    arrayResult = "{"
    for i in array:
        if not first:
            arrayResult += ", "
        else:
            first = False
        if isinstance(i, list):
            arrayResult += f"std::vector<std::any>({array_internal(i)})"  # Fixed: += not =
        elif isinstance(i, dict):
            arrayResult += f"std::map<std::string, std::any>({map_internal(i)})"
        elif isinstance(i, str):
            if check_if_str(i):
                arrayResult += f'{i}'
            else:
                if check_if_var_exists(i):
                    arrayResult += f"{i}"
                else:
                    raise Exception(f"Variable {i} does not exist: {array}")
        else:
            arrayResult += f"{i}"
    arrayResult += "}"
    return arrayResult

def map_internal(map_dict):
    first = True
    mapResult = "{"
    for i in map_dict:
        if not first:
            mapResult += ", "
        else:
            first = False
        
        value = map_dict[i]
        if isinstance(value, list):
            valueResult = f"std::vector<std::any>({array_internal(value)})"
        elif isinstance(value, dict):
            valueResult = f"std::map<std::string, std::any>({map_internal(value)})"
        elif isinstance(value, str):
            if check_if_str(value):
                valueResult = f'{value}'
            else:
                if check_if_var_exists(value):
                    valueResult = value
                else:
                    raise ValueError(f"Variable {i} does not exist: {map_dict}")
        else:
            valueResult = str(value)
        resultI = ""
        if not isinstance(i, str):
            resultI = str(i)
        elif not check_if_str(i):
            if check_if_var_exists(i):
                resultI = str(get_symbol_value(i))
            else:
                raise ValueError(f"Variable does not exist: {i}: {map_dict}")
        if not (resultI[0] == "\"" and resultI[-1] == "\""):
            resultI = f"\"{resultI}\""
        mapResult += "{" + f'{resultI}, {valueResult}' + "}"
    mapResult += "}"
    return mapResult

def visitor_array_assignment(call):
    result = ""
    if call[1] not in symbol_table:
        result = "std::vector<std::any> "
    internal_array = array_internal(call[3])
    result += f"{call[1]} = {internal_array};\n"
    return result

def visitor_dict_assignment(call):
    result = ""
    if not call[1] in symbol_table:
        result += "std::map<std::string, std::any> "
    internal_map = map_internal(call[3])
    result += f"{call[1]} = {internal_map};\n"
    return result

def visitor_operations(node):
    if not isinstance(node, tuple):
        return str(node)
    kind = node[0]
    if kind == "arithmetic_operation":
        return visitor_arithmetic_operation(node).strip()
    if kind == "logical_operation":
        return visitor_logical_operation(node).strip()
    if kind == "relational_operation":
        return visitor_relational_operation(node).strip()
    if kind == "unary_operation":
        return visitor_unary_operation(node).strip()
    if kind == "function_call":
        return visitor_function_call(node).strip()[:-1]
    raise ValueError(f"Unknown node type: {kind}")

def visitor_arithmetic_operation(call):
    _, left, op, right = call
    left = visitor_operations(left)
    right = visitor_operations(right)
    return f"{left} {op} {right}\n"

def visitor_unary_operation(call):
    _, op, value = call
    if value is True:
        value = "true"
    elif value is False:
        value = "false"
    value = visitor_operations(value)
    op = "!" if op == "NOT" else op
    return f"{op}{value}\n"

def visitor_logical_operation(call):
    _, left, op, right = call
    op = op.lower()
    if op == "and":
        op = "&&"
    elif op == "or":
        op = "||"
    left = visitor_operations(left)
    right = visitor_operations(right)
    return f"{left} {op} {right}\n"

def visitor_relational_operation(call):
    _, left, op, right = call
    left = visitor_operations(left)
    right = visitor_operations(right)
    return f"{left} {op} {right}\n"

def visitor_assignment(call):
    _, var_name, symbol, value = call

    # Caso 1: operaciÃ³n, usar std::any
    if isinstance(value, tuple) and value[0] in VALID_OPERATION_NODES:
        value_code = visitor_operations(value)
        return f"std::any {var_name} {symbol} {value_code};\n"

    # Caso 2: literal, usar el tipo correcto en C++
    # bool
    if isinstance(value, bool):
        cpp_value = "true" if value else "false"
        return f"bool {var_name} {symbol} {cpp_value};\n"

    # entero
    if isinstance(value, int):
        return f"int {var_name} {symbol} {value};\n"

    # float
    if isinstance(value, float):
        return f"double {var_name} {symbol} {value};\n"

    # string
    if isinstance(value, str):
        # escapar comillas si es necesario
        escaped = value.replace('"', '\\"')
        return f'std::string {var_name} {symbol} "{escaped}";\n'

    return f'std::any {var_name} {symbol} "{value}";\n'


def visitor_print(call):
    _, exprs = call
    result = ""
    if isinstance(exprs, tuple) and exprs[0] in VALID_OPERATION_NODES:
        value_code = visitor_operations(exprs)
        return 'std::cout << ' + value_code + ' << std::endl;\n'
    elif isinstance(exprs, str): 
        expr_code = visitor_operations(exprs)
        result += 'std::cout << "' + expr_code + '" << std::endl;\n'
        return result
    else: 
        expr_code = visitor_operations(exprs)
        result += 'std::cout << ' + expr_code + ' << std::endl;\n'
        return result
