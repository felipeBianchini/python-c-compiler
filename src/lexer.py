import ply.lex as lex
from src.utils import Error
from src.symbol_table import SymbolTable

class Lexer:
    def __init__(self, errors: list[Error], debug=False):
        self.lex = None
        self.data = None
        self.debug = debug
        self.symbol_table = SymbolTable()
        self.reserved_map = {}
        self.errors = errors
        
        # Indentation tracking
        self.indent_stack = [0]  # Stack of indentation levels
        self.pending_tokens = []  # Queue for pending tokens
        self.start = True  # Flag to detect start of line
        self.current_line_indent = 0  # Track current line's indentation
        
        for r in self.reserved:
            self.reserved_map[r.lower()] = r

    reserved = (
        'IF', 'ELSE', 'ELIF', 'WHILE', 'FOR', 'BREAK', 'CONTINUE', 'PASS', 'DEF', 'RETURN',
        'CLASS', 'AND', 'OR', 'NOT', '__INIT__', 'SELF', 'IN', 'RANGE', 'ITER', 'NEXT', 'PRINT',
        'STR'
    )

    tokens = reserved + (
        # Ids
        'ID', 'INTEGER', 'FLOAT', 'STRING', 'MULTISTRING',

        # Arithmetic
        'PLUS', 'MINUS', 'MUL', 'DIV', 'INT_DIV', 'MOD', 'POW',

        # Boolean
        'TRUE', 'FALSE',

        # Relational
        'EQUAL', 'NOT_EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL',

        # Assignment
        'ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'INT_DIV_ASSIGN', 'POW_ASSIGN',

        # Symbols
        'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON', 'COLON', 'DOT',
        
        # Indentation
        'INDENT', 'DENT', 'NEWLINE',

        # Others
        'NONE',
    )

    # Regular expression rules for simple tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MUL = r'\*'
    t_DIV = r'/'
    t_INT_DIV = r'//'
    t_MOD = r'%'
    t_POW = r'\*\*'
    t_EQUAL = r'=='
    t_NOT_EQUAL = r'!='
    t_GREATER = r'>'
    t_LESS = r'<'
    t_GREATER_EQUAL = r'>='
    t_LESS_EQUAL = r'<='
    t_ASSIGN = r'='
    t_ADD_ASSIGN = r'\+='
    t_SUB_ASSIGN = r'-='
    t_MUL_ASSIGN = r'\*='
    t_DIV_ASSIGN = r'/='
    t_MOD_ASSIGN = r'%='
    t_INT_DIV_ASSIGN = r'//='
    t_POW_ASSIGN = r'\*\*='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COLON = r':'
    t_SEMICOLON = r';'
    t_COMMA = r','
    t_DOT = r'\.'
    
    # For ignoring spaces
    t_ignore = ''

    def token(self):
        # Return pending tokens first
        if self.pending_tokens:
            return self.pending_tokens.pop(0)
        
        # Get next token from lexer
        tok = self.lex.token()
        
        # Check for dedentation when we encounter a non-space token at start of line
        if tok and self.start and tok.type not in ('NEWLINE', 'INDENT', 'DENT'):
            self.handle_dedentation()
            self.start = False
            
            # Return pending tokens if any were generated
            if self.pending_tokens:
                # Put the current token back and return pending token
                self.pending_tokens.append(tok)
                return self.pending_tokens.pop(0)
        
        return tok

    def handle_dedentation(self):
        # Handle dedentation when a non-space token appears at start of line
        # Current line indentation was set to 0 since no spaces were processed
        current_indent = 0  # No spaces means indentation level 0
        
        # Generate DENT tokens for each level we need to pop
        while len(self.indent_stack) > 1 and self.indent_stack[-1] > current_indent:
            self.indent_stack.pop()
            dent_token = lex.LexToken()
            dent_token.type = 'DENT'
            dent_token.value = ''
            dent_token.lineno = self.lex.lineno
            dent_token.lexpos = self.lex.lexpos
            self.pending_tokens.append(dent_token)
        
        # Check if we ended up at a valid indentation level
        if len(self.indent_stack) > 0 and self.indent_stack[-1] != current_indent:
            self.errors.append(Error(
                f"Invalid indentation level: expected {self.indent_stack[-1]} spaces, got {current_indent}",
                self.lex.lineno, self.lex.lexpos, 'lexer', self.data
            ))

    def t_NEWLINE(self, t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)
        self.start = True
        self.current_line_indent = 0  # Reset line indentation tracking
        return t

    def t_SPACE(self, t):
        r"""[ ]+"""
        if self.start:
            # At start of line, handle indentation
            return self.handle_indentation(t)
        else:
            # Space in middle is not important
            pass

    def t_TRUE(self, t):
        r'True'
        t.value = bool(t.value)
        return t

    def t_NONE(self, t):
        r'None'
        t.value = None
        return t

    def t_FALSE(self, t):
        r'False'
        t.value = bool(t.value)
        return t

    def t_ID(self, t):
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        if self.debug:
            print(f'DEBUG(LEXER): {t.value.upper()} on line {t.lineno}, position {t.lexpos}')
        t.type = self.reserved_map.get(t.value, 'ID')
        return t

    def t_FLOAT(self, t):
        r"""
            \d+\.\d* |
            \.\d+
        """
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r"-?\d+" # It might include a - at the beginning
        t.value = int(t.value)
        return t

    def t_MULTISTRING(self, t):
        # Does not allow unescaped " or '
        # Allow escape sequences, but initially allows any escape sequence, that´s why there is a validation function for them
        r""" 
            \"\"\"([^\"\\]|\\.)*\"\"\" |
            '''([^'\\]|\\.)*'''
        """
        content = t.value[3:-3]  # Remove quotes
        
        # Check escape sequences
        if not self._validate_escape_sequences(content, t.lineno, t.lexpos):
            return None
        
        t.value = content
        return t
    
    def t_STRING(self, t):
        # Does not allow unescaped " or '
        # Allow escape sequences, but initially allows any escape sequence, that´s why there is a validation function for them
        r"""
            '([^'\\]|\\.)*' |
            \"([^\"\\]|\\.)*\"
        """
        content = t.value[1:-1]  # Remove quotes
        
        # Check escape sequences
        if not self._validate_escape_sequences(content, t.lineno, t.lexpos):
            return None
        
        t.value = content
        return t

    def t_COMMENT(self, t):
        r"""\#.*"""
        pass  # Ignore comments

    def _validate_escape_sequences(self, content, lineno, lexpos):
        # Validates the escape sequences in strings
        i = 0
        while i < len(content):
            if content[i] == '\\':
                if i + 1 >= len(content):
                    self.errors.append(Error(
                        "Invalid escape sequence: string is unterminated",
                        lineno, lexpos + i + 1, 'lexer', self.data
                    ))
                    return False
                
                next_char = content[i + 1]
                valid_escapes = ['n', 't', '\\', '"', "'"]
                
                if next_char not in valid_escapes:
                    self.errors.append(Error(
                        f"Invalid escape sequence: '\\{next_char}'",
                        lineno, lexpos + i + 1, 'lexer', self.data
                    ))
                    return False
                i += 2
            else:
                i += 1
        
        return True

    def handle_indentation(self, t):
        # Handle indentation changes and generate appropriate tokens
        self.start = False
        
        # Calculate indentation level (convert tabs to 4 spaces)
        indent_level = len(t.value.expandtabs(4))
        self.current_line_indent = indent_level
        current_level = self.indent_stack[-1]
        
        # Validate that indentation is a multiple of 4
        if indent_level % 4 != 0:
            self.errors.append(Error(
                f"Invalid indentation: indentation must be a multiple of 4 spaces, got {indent_level}",
                t.lineno, t.lexpos, 'lexer', self.data
            ))
            return None
        
        if indent_level > current_level:
            # Indentation increase - must be exactly 4 spaces more
            if indent_level != current_level + 4:
                self.errors.append(Error(
                    f"Invalid indentation: expected {current_level + 4} spaces (increase by 4), got {indent_level}",
                    t.lineno, t.lexpos, 'lexer', self.data
                ))
                return None
            
            self.indent_stack.append(indent_level)
            t.type = 'INDENT'
            t.value = ''
            return t
            
        elif indent_level < current_level:
            # Indentation decrease - generate DENT tokens
            dent_count = 0
            while self.indent_stack and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                dent_count += 1
            
            # Check if indentation level matches any previous level
            if not self.indent_stack or self.indent_stack[-1] != indent_level:
                # Invalid indentation level
                self.errors.append(Error(
                    f"Invalid indentation level: expected one of {self.indent_stack} spaces, got {indent_level}",
                    t.lineno, t.lexpos, 'lexer', self.data
                ))
                return None
            
            # Create DENT tokens
            for i in range(dent_count):
                dent_token = lex.LexToken()
                dent_token.type = 'DENT'
                dent_token.value = ''
                dent_token.lineno = t.lineno
                dent_token.lexpos = t.lexpos
                self.pending_tokens.append(dent_token)
        
        # Same indentation level - no token needed
        return None

    def t_error(self, t):
        self.errors.append(Error("Illegal character '%s'" % t.value[0], t.lineno, t.lexpos, 'lexer', self.data))
        print(self.errors[-1])
        t.lexer.skip(1)

    def build(self):
        self.lex = lex.lex(module=self)

    def input(self, data):
        # Sets input and declares internal variables
        self.data = data
        self.indent_stack = [0]
        self.pending_tokens = []
        self.start = True
        self.current_line_indent = 0
        self.lex.input(data)