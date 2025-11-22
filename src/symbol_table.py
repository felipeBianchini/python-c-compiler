class Symbol:
    def __init__(self, name, type_data, scope, line=None, value=None, category='variable'):
        self.name = name
        self.type_data = type_data
        self.scope = scope
        self.line = line
        self.value = value
        self.category = category
    
    def __repr__(self):
        return f"Symbol({self.name}, {self.type_data}, {self.category}, scope={self.scope})"


class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scopes = ['global']
        self.current_scope = 'global'
        self.scope_counter = 0

    def enter_scope(self, scope_name=None):
        if scope_name is None:
            self.scope_counter += 1
            scope_name = f"scope_{self.scope_counter}"
        self.scopes.append(scope_name)
        self.current_scope = scope_name
        return scope_name
    
    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
            self.current_scope = self.scopes[-1]
    
    def insert(self, name, type_data, line=None, value=None, category='variable'):
        key = f"{self.current_scope}::{name}"
        self.symbols[key] = Symbol(name, type_data, self.current_scope, line, value, category)
        return self.symbols[key]
    
    def lookup(self, name):
        for scope in reversed(self.scopes):
            key = f"{scope}::{name}"
            if key in self.symbols:
                return self.symbols[key]
        return None
    
    def lookup_current_scope(self, name):
        return self.symbols.get(f"{self.current_scope}::{name}")
    
    def update_type(self, name, new_type):
        symbol = self.lookup(name)
        if symbol:
            symbol.type_data = new_type
    
    def infer_type_from_value(self, value):
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
        return 'unknown'
    
    def infer_type_from_operation(self, op):
        if not isinstance(op, tuple):
            return self.infer_type_from_value(op)

        op_type = op[0]

        if op_type == 'arithmetic_operation':
            left = self.infer_type_from_operation(op[1])
            right = self.infer_type_from_operation(op[3])
            operator = op[2]
            if operator == '/' or left == 'float' or right == 'float':
                return 'float'
            if left == 'int' and right == 'int':
                return 'int'
            return 'number'
        
        if op_type in ('relational_operation', 'logical_operation', 'unary_operation'):
            return 'bool'

        if op_type == 'function_call':
            func = op[1]
            builtin = {'len': 'int', 'int': 'int', 'float': 'float', 'str': 'str'}
            if func in builtin:
                return builtin[func]
            symbol = self.lookup(func)
            return symbol.type_data if symbol else 'unknown'

        if op_type == 'array assignment':
            return 'list'
        if op_type == 'dictionary assignment':
            return 'dict'

        if op_type == 'access_id':
            var_name = op[1]
            symbol = self.lookup(var_name)
            if symbol:
                if symbol.type_data in ('list', 'str'):
                    return 'element'
                if symbol.type_data == 'dict':
                    return 'value'
            return 'unknown'

        if isinstance(op, str):
            symbol = self.lookup(op)
            return symbol.type_data if symbol else 'unknown'

        return 'unknown'

    def check_type_compatibility(self, type1, type2, operator=None):
        if type1 in ('int', 'float', 'number') and type2 in ('int', 'float', 'number'):
            return 'float' if 'float' in (type1, type2) else 'int'
        if operator == '+' and type1 == type2 == 'str':
            return 'str'
        if type1 == type2:
            return type1
        return None
    
    def print_table(self):
        print("\nTABLA DE SÍMBOLOS\n" + "="*80)
        for s in self.symbols.values():
            print(f"{s.name:<12} {s.type_data:<10} {s.category:<10} {s.scope:<12}")
        print("="*80)

    def print_summary(self):
        print(f"\nSímbolos totales: {len(self.symbols)}")
