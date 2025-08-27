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
        for r in self.reserved:
            self.reserved_map[r.lower()] = r

    reserved = (
        'IF', 'ELSE', 'ELIF', 'WHILE', 'FOR', 'BREAK', 'CONTINUE', 'PASS', 'DEF', 'RETURN', 'PASS',
        'CLASS', 'TRUE', 'FALSE', 'AND', 'OR', 'NOT',
    )

    tokens = reserved + (
        # Identifiers (variables, functions, numbers, strings)
        'ID', 'INTEGER', 'FLOAT', 'STRING',

        # Arithmetic operators
        'PLUS', 'MINUS', 'MUL', 'DIV', 'INT_DIV', 'MOD', 'POW',

        # Relational operator
        'EQUAL', 'NOT_EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL',

        # Assignment operators
        'ASSIGN', 'ADD_ASSIGN', 'SUBS_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'INT_DIV_ASSIGN', 'POW_ASSIGN',

        # Delimiters and symbols
         'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON', 'COLON', 'DOT',
    )

    # Regular expression rules for simple tokens
    # Operators
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
    t_LPAREN = r'('
    t_RPAREN = r')'
    t_LBRACKET = r'['
    t_RBRACKET = r']'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_COLON = r':'
    t_SEMICOLON = r';'
    t_COMMA = r','
    t_DOT = r'.'
    t_ignore = ' \t'

    def t_ID(self, t):
        r"[a-zA-Z][a-zA-Z0-9_]*"
        if self.debug:
            print(f'DEBUG(LEXER): {t.value.upper()} on line {t.lineno}, position {t.lexpos}')
        t.type = self.reserved_map.get(t.value, 'ID')
        return t

    def t_INTEGER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t
    
    def t_FLOAT(self, t):
        r"""
            \d+\.\d* |
            \.\d+
        """
        t.value = float(t.value)
        return t

    def t_STRING(self, t):
        r"""
            '([^'\\]|\\.)*' |
            \"([^\"\\]|\\.)*\"
        """
        t.value = str(t)
        return t

    # TODO: Revisar de aqui para abajo
    # TODO: Comentarios
    # TODO: Indentación
    # TODO: Manejo de errores léxicos
    # TODO: Doc interna y externa

    def t_NEWLINE(self, t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    def t_COMMENT(self, t):
        r"""\%.*"""
        pass

    def t_error(self, t):
        self.errors.append(Error("Illegal character '%s'" % t.value[0], t.lineno, t.lexpos, 'lexer', self.data))
        print(self.errors[-1])
        t.lexer.skip(1)

    def build(self, ):
        self.lex = lex.lex(module=self)