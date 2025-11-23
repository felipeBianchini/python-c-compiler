class Symbol:
    def __init__(self, name, datatype, scope, line=None, value=None, category='variable'):
        # basic unit for a variable, stores its information
        self.name = name
        self.datatype = datatype
        self.scope = scope
        self.line = line
        self.value = value
        self.category = category

class SymbolTable:
    def __init__(self):
        # initialize the symbol table
        self.symbols = {}
        self.scopes = ['global']
        self.current_scope = 'global'
        self.scope_counter = 0

    def getSymbolType(self, name):
        if not isinstance(name, str):
            return type(name).__name__
        elif name[0] == "\"" and name[-1] == "\"":
            return "std::string"
        for scope in reversed(self.scopes):
            key = f"{scope}::{name}"
            if key in self.symbols:
                return self.symbols[key].datatype
        return None
    
    def enter_scope(self, scope_name=None):
        # enters and creates a new scope
        if scope_name is None:
            self.scope_counter += 1
            scope_name = f"scope_{self.scope_counter}"
        self.scopes.append(scope_name)
        self.current_scope = scope_name
        return scope_name
    
    def exit_scope(self):
        # exits current scope and returns to previous
        if len(self.scopes) > 1:
            self.scopes.pop()
            self.current_scope = self.scopes[-1]
    
    def insert(self, name, datatype, line=None, value=None, category='variable'):
        # inserts a new symbol into the table
        key = f"{self.current_scope}::{name}"
        self.symbols[key] = Symbol(name, datatype, self.current_scope, line, value, category)
        return self.symbols[key]
    
    def lookup(self, name):
        # searches for a symbol in all scopes from current to global
        for scope in reversed(self.scopes):
            key = f"{scope}::{name}"
            if key in self.symbols:
                return self.symbols[key]
        return None
    
    def lookup_current_scope(self, name):
        # searches for a symbol only in the current scope
        return self.symbols.get(f"{self.current_scope}::{name}")
    
    def update_type(self, name, new_type):
        # updates the datatype of an existing symbol
        symbol = self.lookup(name)
        if symbol:
            symbol.datatype = new_type
    
    def infer_type_from_value(self, value):
        # infers the datatype based on a literal value
        if value is None or value == 'None':
            return 'None'
        if isinstance(value, bool) or value in ('True', 'False'):
            return 'bool'
        if isinstance(value, int):
            return 'int'
        if isinstance(value, float):
            return 'float'
        if isinstance(value, str):
            return 'str'
        if isinstance(value, list):
            return 'list'
        if isinstance(value, dict):
            return 'dict'
        if isinstance(value, set):
            return 'set'
        search = self.lookup(value)
        if search != None:
            return search.datatype
        return 'any'
    
    def infer_type_from_operation(self, op):
        # infers the datatype resulting from an operation
        if not isinstance(op, tuple):
            return self.infer_type_from_value(op)
        op_type = op[0]
        if op_type == 'arithmetic_operation':
            left = self.infer_type_from_operation(op[1])
            operator = op[2]
            right = self.infer_type_from_operation(op[3])
            # this operator always returns int
            if operator == '//':
                    return 'int'
            # if only one operand is float, result is float
            if left == 'float' or right == 'float':
                return 'float'
            # if both operands are int, result is int
            if left == 'int' and right == 'int':
                return 'int'
            # default to int for mixed or unknown numeric types
            return 'int'
        # all these operations result in boolean type
        if op_type in ('relational_operation', 'logical_operation', 'unary_operation'):
            return 'bool'
        # function calls return the function's return type
        if op_type == 'function_call':
            func = op[1]
            symbol = self.lookup(func)
            return symbol.datatype if symbol else 'any'
        # data structures
        if op_type == 'array assignment':
            return 'list'
        if op_type == 'dictionary assignment':
            return 'dict'
        if op_type == 'access_id':
            var_name = op[1]
            symbol = self.lookup(var_name)
            if symbol:
                if symbol.datatype in ('list', 'str'):
                    return 'element'
                if symbol.datatype == 'dict':
                    return 'value'
            return 'any'
        if isinstance(op, str):
            symbol = self.lookup(op)
            return symbol.datatype if symbol else 'any'
        return 'any'

    def check_type_compatibility(self, type1, type2, operator=None):
        # checks if two types are compatible for an operation
        if type1 in ('int', 'float', 'number') and type2 in ('int', 'float', 'number'):
            return 'float' if 'float' in (type1, type2) else 'int'
        if operator == '+' and type1 == type2 == 'str':
            return 'str'
        if type1 == type2:
            return type1
        return None
    
    def print_table(self):
        # Imprime todos los símbolos registrados en una tabla legible
        print("\nTABLA DE SÍMBOLOS\n" + "="*80)
        for s in self.symbols.values():
            print(f"{s.name:<12} {s.datatype:<10} {s.category:<10} {s.scope:<12}")
        print("="*80)

    def print_summary(self):
        # Muestra cuántos símbolos hay registrados en total
        print(f"\nSímbolos totales: {len(self.symbols)}")
