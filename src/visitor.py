symbol_table = {0: {"a" : {"value" : 0, "type" : "int"}},
                1: {"a" : {"value" : 0, "type" : "int"}},
                }
current_level = 0
function_table = {}
VALID_OPERATION_NODES = {
    "arithmetic_operation",
    "logical_operation",
    "relational_operation",
    "unary_operation",
    "function_call"
}
keywords = ["break", "continue"]

def visit(node):
    if node is None:
        return ""
    if isinstance(node, tuple):
        tag = node[0].replace(" ", "_")
        func = globals().get(f"visitor_{tag}", None)
        if func is None:
            print(f"No visitor for node type: {node[0]}")
            raise TypeError()
        return func(node)

    if isinstance(node, list):
        return "\n".join(visit(n) for n in node)

    if node in keywords:
        func = globals().get(f"visitor_{node}", None)
        return func(node)

    return str(node)

def check_if_str(data):
    return data[0] == "\"" and data[-1] == "\""

def check_if_var_exists(var):
    i = current_level
    
    while (i >= 0):
        if var in symbol_table[i]:
            return True
        else:
            i -= 1
    return False

def get_symbol_value(symbol):
    i = current_level
    symbol = str(symbol)
    while (i >= 0):
        if symbol in symbol_table[i]:
            if symbol_table[i][symbol]["type"] == "nan":
                return symbol
            else:
                return symbol_table[i][symbol]["value"]
        else:
            i -= 1
    raise ValueError(f"Symbol {symbol} does not exist")

def get_symbol_type(symbol):
    symbol = str(symbol)
    i = current_level

    while(i >= 0):
        if symbol in symbol_table[i]:
            return symbol_table[i][symbol]["type"]
        else:
            i -= 1
    raise ValueError(f"Symbol {symbol} does not exist")

def visitor_function_call(call):
    _, name, args_node = call
    args = args_node[1]
    if name in function_table:
        expected = function_table[name]
        given = len(args)
        if given == expected:
            arg_parts = []
            for i in args:
                first = i[1]
                if isinstance(first, tuple) and first[0] in VALID_OPERATION_NODES:
                    arg_parts.append(visitor_operations(first))
                else:
                    arg_parts.append(visit(first))
            cpp_args = ", ".join(arg_parts)
            return f"{name}({cpp_args})"
        else:
            print(f"Error Not enough parameters to call {call[1]}")
    else:
        print(f"Error: {call[1]} does not exist")

def array_internal(array):
    first = True
    types = []
    arrayResult = "{"
    for i in array:
        if not first:
            arrayResult += ", "
        else:
            first = False
        if isinstance(i, list):
            arrayResult += f"std::vector<std::any>({array_internal(i)[0]})" 
            types.append("list")
        elif isinstance(i, dict):
            arrayResult += f"std::map<std::string, std::any>({map_internal(i)[0]})"
            types.append("dict")
        elif isinstance(i, str):
            if check_if_str(i):
                arrayResult += f'{i}'
                types.append("str")
            else:
                if check_if_var_exists(i):
                    arrayResult += f"{i}"
                    types.append(get_symbol_type(i))
                else:
                    raise Exception(f"Variable {i} does not exist: {array}")
        else:
            arrayResult += f"{i}"
            types.append(str(type(i).__name__))
    arrayResult += "}"
    return arrayResult, types

def map_internal(map_dict):
    first = True
    types = {}
    mapResult = "{"
    current_type = ""
    array_subtype = ""
    for i in map_dict:
        if not first:
            mapResult += ", "
        else:
            first = False
        
        value = map_dict[i]
        if isinstance(value, list):
            valueResult, array_subtype = f"std::vector<std::any>({array_internal(value)[0]})"
            current_type = "list"
        elif isinstance(value, dict):
            valueResult, array_subtype = f"std::map<std::string, std::any>({map_internal(value)[0]})"
            current_type = "dict"
        elif isinstance(value, str):
            if check_if_str(value):
                valueResult = f'{value}'
                current_type = "str"
            else:
                if check_if_var_exists(value):
                    valueResult = value
                    current_type = get_symbol_type(value)
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
        else:
            resultI = i
        if not (resultI[0] == "\"" and resultI[-1] == "\""):
            resultI = f"\"{resultI}\""
        mapResult += "{" + f'{resultI}, {valueResult}' + "}"
        types[resultI] = {}
        types[resultI]["type"] = current_type
        if current_type == "dict" or current_type == "list":
            types[resultI]["types"] = array_subtype
    mapResult += "}"
    return mapResult, types

def visitor_array_assignment(call):
    result = ""
    if call[1] not in symbol_table:
        result = "std::vector<std::any> "
    internal_array, internal_types = array_internal(call[3])
    result += f"{call[1]} = {internal_array};\n"
    symbol_table[current_level][call[1]] = {}
    symbol_table[current_level][call[1]]["type"] = "list"
    symbol_table[current_level][call[1]]["types"] = internal_types
    return result

def visitor_dict_assignment(call):
    result = ""
    if not call[1] in symbol_table:
        result += "std::map<std::string, std::any> "
    internal_map = map_internal(call[3])
    result += f"{call[1]} = {internal_map};\n"
    symbol_table[current_level][call[1]]["type"] = "dict"
    return result

def visitor_append(node):
    __,var, val = node
    result = ""
    if check_if_var_exists(var):
        val_result = ""
        if get_symbol_type(var) == "list":
            var_result = f"{var}.push_back("
        else:
            raise TypeError(f"Var {var} is not a list, so it cannot be appended")
        
        if isinstance(val, str):
            if not check_if_str(val):
                val = get_symbol_value(val)
            else:
                val = f"\"{val}\""

        var_result += f"{val});"
        return var_result
    else:
        raise ValueError(f"Var {var} does not exist, cannot append")        


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
        return visitor_function_call(node)
    raise ValueError(f"Unknown node type: {kind}")

def visitor_arithmetic_operation(call):
    _, left, op, right = call
    left = visitor_operations(left)
    right = visitor_operations(right)
    return f"{left} {op} {right}"

def visitor_unary_operation(call):
    _, op, value = call
    if value is True:
        value = "true"
    elif value is False:
        value = "false"
    value = visitor_operations(value)
    op = "!" if op == "NOT" else op
    return f"{op}{value}"

def visitor_logical_operation(call):
    _, left, op, right = call
    op = op.lower()
    if op == "and":
        op = "&&"
    elif op == "or":
        op = "||"
    left = visitor_operations(left)
    right = visitor_operations(right)
    return f"{left} {op} {right}"

def visitor_relational_operation(call):
    _, left, op, right = call
    left = visitor_operations(left)
    right = visitor_operations(right)
    return f"{left} {op} {right}"

def visitor_simple_assignment_operation(call):
    _, var_name, symbol, value = call
    if isinstance(value, tuple) and value[0] in VALID_OPERATION_NODES:
        value_code = visitor_operations(value)
        return f"std::any {var_name} {symbol} {value_code};\n"
    if isinstance(value, bool):
        cpp_value = "true" if value else "false"
        return f"bool {var_name} {symbol} {cpp_value};\n"
    if isinstance(value, int):
        return f"int {var_name} {symbol} {value};\n"
    if isinstance(value, float):
        return f"double {var_name} {symbol} {value};\n"
    if isinstance(value, str):
        escaped = value.replace('"', '\\"')
        return f'std::string {var_name} {symbol} "{escaped}";\n'
    return f'std::any {var_name} {symbol} "{value}";\n'

def visitor_print_call(call):
    _, exprs = call
    result = ""
    if isinstance(exprs, tuple) and exprs[0] in VALID_OPERATION_NODES:
        value_code = visitor_operations(exprs)
        result += f'std::cout << {value_code} << std::endl;\n'
        return result
    elif isinstance(exprs, str):
        if check_if_str(exprs):
            exprs = exprs[1:-1]
            expr_code = visitor_operations(exprs)
            result += f'std::cout << "{expr_code}" << std::endl;\n'
            return result
        else:
            if check_if_var_exists(exprs):
                result += f'std::cout << {get_symbol_value(exprs)} << std::endl;\n'
                return result
            else:
                raise ValueError(f"Variable {exprs} does not exist")
    else: 
        expr_code = visitor_operations(exprs)
        result += f'std::cout << {expr_code} << std::endl;\n'
        return result

def visitor_argument(node):
    _, first, second = node
    symbol_table[current_level][first] = {}
    symbol_table[current_level][first]["type"] = "nan"
    symbol_table[current_level][first]["value"] = "nan"
    return f"std::any {visit(first)}"

def visitor_arguments(node):
    _, args = node
    if not args:
        return ""
    return ", ".join(visit(a) for a in args)

def visitor_return(node):
    return "return;"

def visitor_return_expression(node):
    _, expr = node
    return f"return {visit(expr)};"

def visitor_complete_function_body(node):
    _, sentences, ret = node
    cpp_code = ""
    if sentences:
        cpp_code += visit(sentences)
    if ret:
        if cpp_code:
            cpp_code += "\n"
        cpp_code += visit(ret)
    return cpp_code

def visitor_incomplete_function_body(node):
    _, body = node
    return visit(body)

def visitor_function(node):
    _, name, args, body = node
    args_list = args[1]
    function_table[name] = len(args_list)
    global current_level
    current_level += 1
    symbol_table[current_level] = {}
    cpp_args = visit(args)
    cpp_body = visit(body)
    cpp_body = indent(cpp_body, current_level)
    current_level -= 1
    symbol_table[current_level] = {}
    return f"auto {name}({cpp_args})" + " {\n" + f"{cpp_body}\n" + "}"

def indent(text, level=1):
    pad = "    " * level
    return "\n".join(pad + line for line in text.split("\n") if line.strip() != "")

def write_if(node):
    global current_level 
    current_level += 1
    symbol_table[current_level] = {}
    
    if_clause = f"if ({visit(node[1])})" + " {\n"
    result_body = visit(node[2])
    result_body = indent(result_body, current_level)
    
    symbol_table[current_level] = {}
    current_level -= 1
    result = f"{if_clause}{result_body}\n{"}"}\n"
    return result

def write_elif(node):
    global current_level
    current_level += 1
    symbol_table[current_level] = {}
    
    elif_clause = f"else if ({visit(node[1])})" + " {\n"
    result_body = visit(node[2])
    result_body = indent(result_body, current_level)
    symbol_table[current_level] = {}
    result = f"{elif_clause}{result_body}\n{"}"}\n"
    
    symbol_table[current_level] = {}
    current_level -= 1
    return result

def write_else(node):
    global current_level
    current_level += 1
    symbol_table[current_level] = {}
    
    result_body = visit(node[1])
    result_body = indent(result_body, current_level)
    result = f"else {"{"}\n{result_body}\n{"}"}"

    symbol_table[current_level] = {}
    current_level -= 1
    return result

def visitor_conditional(node):
    result = ""
    if len(node) > 1:
        result += write_if(node[1])
    if len(node) > 2:
        for i in node[2]:
            if i == "elif_list":
                continue
            result += write_elif(i[0])
    if len(node) > 3:
        result += write_else(node[3])
    return result

def visitor_incomplete_block_body(node):
    _, body = node
    return visit(body)

def visitor_complete_block_body(node):
    _, sentences, ret = node
    cpp_code = ""
    if sentences:
        cpp_code += visit(sentences)
    if ret:
        if cpp_code:
            cpp_code += "\n"
        cpp_code += visit(ret)
    return cpp_code

def visitor_in_range_clause(node):
    ____, var, range_val = node
    symbol_table[current_level][var] = {}
    symbol_table[current_level][var]["type"] = "int"
    symbol_table[current_level][var]["value"] = var 
    result = f"(int {var}; {var} <= {range_val}; {var}++)"
    return result

def visitor_for(node):
    __, clause = node
    clause_cpp = visit(clause)
    result = f"for {clause_cpp}" + " {\n"
    return result

def visitor_while(node):
    __, clause = node
    while_clause = visit(clause)
    result = f"while ({while_clause})" + " {\n"
    return result

def visitor_loop(node):
    __, loop, body = node
    global current_level
    current_level += 1
    symbol_table[current_level] = {}

    
    loop_clause = visit(loop)
    body_cpp = visit(body)
    body_cpp = indent(body_cpp, current_level)
    result = f"{loop_clause}" + f"{body_cpp}\n" + "}\n"
    symbol_table[current_level] = {}
    current_level -= 1
    return result

def visitor_incomplete_loop_body(node):
    _, body = node
    return visit(body)

def visitor_complete_loop_body(node):
    _, sentences, ret = node
    cpp_code = ""
    if sentences:
        cpp_code += visit(sentences)
    if ret:
        if cpp_code:
            cpp_code += "\n"
        cpp_code += visit(ret)
    return cpp_code

def visitor_assignment_operation(node):
    __, op1, operation, op2 = node
    if isinstance(op1, str):
        if not check_if_str(op1):
            if not check_if_var_exists(op1):
                raise ValueError("Varibale {op1} does not exist")
    
    if isinstance(op2, str):
        if not check_if_str(op2):
            if not check_if_var_exists(op2):
                raise ValueError("Varibale {op2} does not exist")
    
    result = f"{op1} {operation} {op2};"
    return result

def visitor_break(node):
    return "break;"

def visitor_continue(node):
    return "continue;"
    
query = ('function', 'sexo', ('arguments', [('argument', 'a', None)]), ('incomplete function body', [('loop', ('while', ('relational_operation', 'a', '<', 5)), ('complete loop body', [('print_call', 'a'), ('assignment_operation', 'a', '+=', 1)], None))]))
print(visit(query))
visit(('array assignment', 'a', '=', [1, 2]))
print(symbol_table)
query = ('append', 'a', 3)
print(visit(query))