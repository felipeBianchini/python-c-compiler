from src.symbol_table import SymbolTable

class Visitor:
    def __init__(self, symbol_table=None, parse_tree=None):
        self.symbol_table = symbol_table
        self.parse_tree = parse_tree
        self.current_level = 0
        self.function_table = {}
        self.VALID_OPERATION_NODES = {
            "arithmetic_operation",
            "logical_operation",
            "relational_operation",
            "unary_operation",
            "function_call"
        }
        self.keywords = ["break", "continue"]
        pass

    def start(self):
        includes = '''#include <any>\n#include <cmath>\n# include <iostream>\n\n'''
        code = self.visit(self.parse_tree)
        fmain = "\n\nint main() {\n    return 0;\n}\n"
        return includes + code + fmain

    def visit(self, node):
        if node is None:
            return ""
        
        if isinstance(node, tuple):
            tag = node[0].replace(" ", "_")
            func = getattr(self, f"visitor_{tag}", None)
            if func is None:
                print(f"No visitor for node type: {node[0]}")
                raise TypeError(f"No visitor for {node[0]}")
            return func(node)

        elif isinstance(node, list):
            return "".join(self.visit(n) for n in node)

        # Palabras clave como break/continue
        if node in self.keywords:
            func = getattr(self, f"visitor_{node}", None)
            if func:
                return func(node)

        # Literales simples
        return str(node)

    def check_if_str(self, data):
        return data[0] == "\"" and data[-1] == "\""

    def check_if_var_exists(self, var):
        return self.symbol_table.lookup(var) is not None

    def get_symbol_value(self, symbol):
        sym = self.symbol_table.lookup(symbol)
        if sym is None:
            raise ValueError(f"Symbol {symbol} does not exist")
        return sym.value

    def get_symbol_type(self, symbol):
        sym = self.symbol_table.lookup(symbol)
        if sym is None:
            raise ValueError(f"Symbol {symbol} does not exist")
        return sym.datatype

    def visitor_function_call(self, call):
        _, name, args_node = call
        args = args_node[1]
        if name in self.function_table:
            expected = self.function_table[name]
            given = len(args)
            if given == expected:
                arg_parts = []
                for i in args:
                    first = i[1]
                    if isinstance(first, tuple) and first[0] in self.VALID_OPERATION_NODES:
                        arg_parts.append(self.visitor_operations(first))
                    else:
                        arg_parts.append(self.visit(first))
                cpp_args = ", ".join(arg_parts)
                return f"{name}({cpp_args})"
            else:
                print(f"Error Not enough parameters to call {call[1]}")
        else:
            print(f"Error: {call[1]} does not exist")

    def array_internal(self, array):
        first = True
        types = []
        arrayResult = "{"
        for i in array:
            if not first:
                arrayResult += ", "
            else:
                first = False
            if isinstance(i, list):
                arrayResult += f"std::vector<std::any>({self.array_internal(i)[0]})" 
                types.append("list")
            elif isinstance(i, dict):
                arrayResult += f"std::map<std::string, std::any>({self.map_internal(i)[0]})"
                types.append("dict")
            elif isinstance(i, str):
                if self.check_if_str(i):
                    arrayResult += f'{i}'
                    types.append("str")
                else:
                    if self.check_if_var_exists(i):
                        arrayResult += f"{i}"
                        types.append(self.get_symbol_type(i))
                    else:
                        raise Exception(f"Variable {i} does not exist: {array}")
            else:
                arrayResult += f"{i}"
                types.append(str(type(i).__name__))
        arrayResult += "}"
        return arrayResult, types

    def map_internal(self, map_dict):
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
                valueResult, array_subtype = f"std::vector<std::any>({self.array_internal(value)[0]})"
                current_type = "list"
            elif isinstance(value, dict):
                valueResult, array_subtype = f"std::map<std::string, std::any>({self.map_internal(value)[0]})"
                current_type = "dict"
            elif isinstance(value, str):
                if self.check_if_str(value):
                    valueResult = f'{value}'
                    current_type = "str"
                else:
                    if self.check_if_var_exists(value):
                        valueResult = value
                        current_type = self.get_symbol_type(value)
                    else:
                        raise ValueError(f"Variable {i} does not exist: {map_dict}")
            else:
                valueResult = str(value)
            resultI = ""
            if not isinstance(i, str):
                resultI = str(i)
            elif not self.check_if_str(i):
                if self.check_if_var_exists(i):
                    resultI = str(self.get_symbol_value(i))
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

    def visitor_array_assignment(self, call):
        result = ""
        if call[1] not in self.symbol_table:
            result = "std::vector<std::any> "
        internal_array, internal_types = self.array_internal(call[3])
        result += f"{call[1]} = {internal_array};\n"
        self.symbol_table[self.current_level][call[1]] = {}
        self.symbol_table[self.current_level][call[1]]["type"] = "list"
        self.symbol_table[self.current_level][call[1]]["types"] = internal_types
        return result

    def visitor_dict_assignment(self, call):
        result = ""
        if not call[1] in self.symbol_table:
            result += "std::map<std::string, std::any> "
        internal_map = self.map_internal(call[3])
        result += f"{call[1]} = {internal_map};\n"
        self.symbol_table[self.current_level][call[1]]["type"] = "dict"
        return result

    def visitor_append(self, node):
        __,var, val = node
        result = ""
        if self.check_if_var_exists(var):
            val_result = ""
            if self.get_symbol_type(var) == "list":
                var_result = f"{var}.push_back("
            else:
                raise TypeError(f"Var {var} is not a list, so it cannot be appended")
            
            if isinstance(val, str):
                if not self.check_if_str(val):
                    val = self.get_symbol_value(val)
                else:
                    val = f"\"{val}\""

            var_result += f"{val});"
            return var_result
        else:
            raise ValueError(f"Var {var} does not exist, cannot append")        

    def visitor_operations(self, node):
        if not isinstance(node, tuple):
            return str(node)
        kind = node[0]
        if kind == "arithmetic_operation":
            return self.visitor_arithmetic_operation(node).strip()
        if kind == "logical_operation":
            return self.visitor_logical_operation(node).strip()
        if kind == "relational_operation":
            return self.visitor_relational_operation(node).strip()
        if kind == "unary_operation":
            return self.visitor_unary_operation(node).strip()
        if kind == "function_call":
            return self.visitor_function_call(node)
        raise ValueError(f"Unknown node type: {kind}")

    def visitor_arithmetic_operation(self, call):
        _, left, op, right = call
        left = self.visitor_operations(left)
        right = self.visitor_operations(right)
        if op == "//":
            return f"std::floor({left} / {right})"
        return f"{left} {op} {right}"

    def visitor_unary_operation(self, call):
        _, op, value = call
        if value is True:
            value = "true"
        elif value is False:
            value = "false"
        value = self.visitor_operations(value)
        op = "!" if op == "NOT" else op
        return f"{op}{value}"

    def visitor_logical_operation(self, call):
        _, left, op, right = call
        op = op.lower()
        if op == "and":
            op = "&&"
        elif op == "or":
            op = "||"
        left = self.visitor_operations(left)
        right = self.visitor_operations(right)
        return f"{left} {op} {right}"

    def visitor_relational_operation(self, call):
        _, left, op, right = call
        left = self.visitor_operations(left)
        right = self.visitor_operations(right)
        return f"{left} {op} {right}"

    def visitor_simple_assignment_operation(self, call):
        _, var_name, symbol, value = call
        if isinstance(value, tuple) and value[0] in self.VALID_OPERATION_NODES:
            value_code = self.visitor_operations(value)
            datatype = self.symbol_table.infer_type_from_operation(value)
        else:
            value_code = str(value)
            datatype = self.symbol_table.infer_type_from_value(value)
        self.symbol_table.insert(var_name, datatype, value=value)
        return f"{datatype} {var_name} {symbol} {value_code};\n"


    def visitor_print_call(self, call):
        _, exprs = call
        result = ""
        if isinstance(exprs, tuple) and exprs[0] in self.VALID_OPERATION_NODES:
            value_code = self.visitor_operations(exprs)
            result += f'std::cout << {value_code} << std::endl;\n'
            return result
        elif isinstance(exprs, str):
            if self.check_if_str(exprs):
                exprs = exprs[1:-1]
                expr_code = self.visitor_operations(exprs)
                result += f'std::cout << "{expr_code}" << std::endl;\n'
                return result
            else:
                if self.check_if_var_exists(exprs):
                    result += f'std::cout << {self.get_symbol_value(exprs)} << std::endl;\n'
                    return result
                else:
                    raise ValueError(f"Variable {exprs} does not exist")
        else: 
            expr_code = self.visitor_operations(exprs)
            result += f'std::cout << {expr_code} << std::endl;\n'
            return result

    def visitor_argument(self, node):
        _, name, expr = node
        self.symbol_table.insert(name, "any", value=None)
        if expr is not None:
            value_cpp = self.visit(expr)
            inferred_type = self.symbol_table.infer_type_from_operation(expr)
            self.symbol_table.update_type(name, inferred_type)
            return f"std::any {name} = {value_cpp}"
        return f"std::any {name}"

    def visitor_arguments(self, node):
        _, args = node
        if not args:
            return ""
        return ", ".join(self.visit(a) for a in args)

    def visitor_return(self, node):
        return "return;"

    def visitor_return_expression(self, node):
        _, expr = node
        return f"return {self.visit(expr)};"

    def visitor_complete_function_body(self, node):
        _, sentences, ret = node
        cpp_code = ""
        if sentences:
            cpp_code += self.visit(sentences)
        if ret:
            if cpp_code:
                cpp_code += "\n"
            cpp_code += self.visit(ret)
        return cpp_code

    def visitor_incomplete_function_body(self, node):
        _, body = node
        return self.visit(body)

    def visitor_function(self, node):
        _, name, args, body = node
        args_list = args[1]
        self.function_table[name] = len(args_list)

        # Nuevo scope función
        self.symbol_table.enter_scope(name)

        cpp_args = self.visit(args)
        cpp_body = self.visit(body)
        cpp_body = self.indent(cpp_body, 1)

        # Cerrar scope
        self.symbol_table.exit_scope()

        return f"auto {name}({cpp_args}) {{\n{cpp_body}\n}}"


    def write_if(self, node):
        cond = self.visit(node[1])

        self.symbol_table.enter_scope("if")
        body = self.visit(node[2])
        body = self.indent(body, 1)
        self.symbol_table.exit_scope()

        return f"if ({cond}) {{\n{body}\n}}\n"


    def write_elif(self, node):
        cond = self.visit(node[1])

        self.symbol_table.enter_scope("elif")
        body = self.visit(node[2])
        body = self.indent(body, 1)
        self.symbol_table.exit_scope()

        return f"else if ({cond}) {{\n{body}\n}}\n"


    def write_else(self, node):
        self.symbol_table.enter_scope("else")
        body = self.visit(node[1])
        body = self.indent(body, 1)
        self.symbol_table.exit_scope()
        
        return f"else {{\n{body}\n}}\n"

    def visitor_conditional(self, node):
        result = ""
        if len(node) > 1:
            result += self.write_if(node[1])
        if len(node) > 2:
            for i in node[2]:
                if i == "elif_list":
                    continue
                result += self.write_elif(i[0])
        if len(node) > 3:
            result +=self. write_else(node[3])
        return result

    def visitor_incomplete_block_body(self, node):
        _, body = node
        return self.visit(body)

    def visitor_complete_block_body(self, node):
        _, sentences, ret = node
        cpp_code = ""
        if sentences:
            cpp_code += self.visit(sentences)
        if ret:
            if cpp_code:
                cpp_code += "\n"
            cpp_code += self.visit(ret)
        return cpp_code

    def visitor_in_range_clause(self, node):
        _, var, range_val = node
        self.symbol_table.insert(var, "int", value=None)
        range_cpp = self.visit(range_val)
        inferred_type = self.symbol_table.infer_type_from_operation(range_val)
        if inferred_type == "float":
            range_cpp = f"(int){range_cpp}"
        return f"(int {var} = 0; {var} < {range_cpp}; {var}++)"

    def visitor_for(self, node):
        __, clause = node
        clause_cpp = self.visit(clause)
        result = f"for {clause_cpp}" + " \n"
        return result

    def visitor_while(self, node):
        __, clause = node
        while_clause = self.visit(clause)
        result = f"while ({while_clause})" + " {\n"
        return result

    def visitor_loop(self, node):
        _, loop, body = node
        loop_clause = self.visit(loop)

        self.symbol_table.enter_scope("loop")
        body_cpp = self.visit(body)
        body_cpp = self.indent(body_cpp, 1)
        self.symbol_table.exit_scope()

        return f"{loop_clause} {{\n{body_cpp}\n}}\n"

    def visitor_incomplete_loop_body(self, node):
        _, body = node
        return self.visit(body)

    def visitor_complete_loop_body(self, node):
        _, sentences, ret = node
        cpp_code = ""
        if sentences:
            cpp_code += self.visit(sentences)
        if ret:
            if cpp_code:
                cpp_code += "\n"
            cpp_code += self.visit(ret)
        return cpp_code

    def visitor_assignment_operation(self, node):
        __, op1, operation, op2 = node
        if isinstance(op1, str):
            if not self.check_if_str(op1):
                if not self.check_if_var_exists(op1):
                    raise ValueError("Varibale {op1} does not exist")
        
        if isinstance(self, op2, str):
            if not self.check_if_str(op2):
                if not self.check_if_var_exists(op2):
                    raise ValueError("Varibale {op2} does not exist")
        
        result = f"{op1} {operation} {op2};"
        return result

    def visitor_break(self, node):
        return "break;"

    def visitor_continue(self, node):
        return "continue;"
    
    def indent(self, text, level=1):
        if not text:
            return ""
        pad = "    " * level
        return "\n".join(
            pad + line if line.strip() != "" else ""
            for line in text.split("\n")
        )
