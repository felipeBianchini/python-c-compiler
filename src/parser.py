import ply.yacc as yacc
from src.lexer import Lexer

class Parser:
    tokens = Lexer.tokens

    def __init__(self):
        self.parser = yacc.yacc(module=self, debug=True)

    # initial production
    def p_program(self, p):
        '''program : complete_sentence program
                   | complete_sentence
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    # production for a complete sentence including possible newlines
    def p_complete_sentence(self, p):
        'complete_sentence : sentence optional_newline'
        p[0] = p[1]

    # production for complete sentences
    # this includes single line operations and compound sentences
    # TODO: Add loops and if sentences
    def p_sentence(self, p):
        '''sentence : operation
                     | function
                     | function_call
                     | class
        '''
        p[0] = p[1]

    # recursive production for complete sentences
    def p_complete_sentences(self, p):
        '''complete_sentences : complete_sentences complete_sentence 
                              | complete_sentence            
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    # for empty rules
    def p_empty(self, p):
        'empty :'
        p[0] = None

    # production for newlines
    def p_optional_newline(self, p):
        '''optional_newline : NEWLINE
                            | empty'''
        p[0] = None

    # for error handling
    def p_error(self, p):
        if p:
            token_type = p.type
            token_value = p.value
            lineno = p.lineno
            lexpos = p.lexpos
            print(f"\nSyntax error: unexpected token '{token_value}' (type: {token_type}) at line {lineno}, position {lexpos}")

    # datatypes
    def p_data_type(self, p):
        '''data_type : ID
                     | INTEGER
                     | FLOAT
                     | STRING
                     | MULTISTRING
                     | NONE
        '''
        p[0] = p[1]

    # production for any number
    def p_number(self, p):
        '''number : INTEGER 
                  | FLOAT'''
        p[0] = p[1]

    # production for any string
    def p_text(self, p):
        '''text : STRING 
                | MULTISTRING
                | number_to_string'''
        p[0] = p[1]

    # production for all arithmetic symbols
    def p_arithmetic_symbol(self, p):
        '''arithmetic_symbol : PLUS 
                             | MINUS
                             | MUL 
                             | DIV 
                             | INT_DIV 
                             | MOD 
                             | POW'''
        p[0] = p[1]

    # production for all assignment symbols
    def p_assignment_symbol(self, p):
        '''assignment_symbol : ASSIGN 
                             | ADD_ASSIGN 
                             | SUB_ASSIGN 
                             | MUL_ASSIGN 
                             | DIV_ASSIGN 
                             | MOD_ASSIGN 
                             | INT_DIV_ASSIGN 
                             | POW_ASSIGN'''
        p[0] = p[1]

    # production for all relational symbols
    def p_relational_symbol(self, p):
        '''relational_symbol : EQUAL 
                             | NOT_EQUAL 
                             | GREATER 
                             | LESS 
                             | GREATER_EQUAL 
                             | LESS_EQUAL'''
        p[0] = p[1]

    # production for logical operators
    def p_logical_operator(self, p):
        '''logical_operator : AND 
                            | NOT 
                            | OR'''
        p[0] = p[1]

    # production for conditional operators
    def p_conditional_operator(self, p):
        '''conditional_operator : TRUE 
                                | FALSE'''
        p[0] = p[1]

    # production for string method that converts numbers to strings
    # str(number)
    def p_number_to_string(self, p):
        'number_to_string : STR LPAREN number RPAREN'
        p[0] = str(p[1])

    # assignment operations
    def p_assignment_operation(self, p):
        'assignment_operation : ID assignment_symbol data_type'
        p[0] = ("assignment operation", p[1], p[2], p[3])

    # arithmetic operations
    # TODO: It is possible to add strings too
    def p_arithmetic_operation(self, p):
        '''arithmetic_operation : arithmetic_operation arithmetic_symbol arithmetic_operation
                                | LPAREN arithmetic_operation RPAREN
                                | number 
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4 and p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = ("arithmetic operation", p[1], p[2], p[3])

    # relational operators
    def p_relational_operation(self, p):
        '''relational_operation : ID relational_symbol ID
                               | number relational_symbol number
                               | text relational_symbol text
        '''
        p[0] = ("relational operation", p[1], p[2], p[3])

    # production for all types of one single line operations
    def p_operation(self, p):
        '''operation : relational_operation 
                     | arithmetic_operation 
                     | assignment_operation'''
        p[0] = p[1]

    # production for a single function argument
    def p_argument(self, p):
        '''argument : ID
                    | data_type
                    | ID COLON data_type
                    | SELF
        '''
        if len(p) == 2:
            p[0] = ("param", p[1], None)
        else:
            p[0] = ("param", p[1], p[3])

    # production for a group of function arguments
    def p_arguments(self, p):
        '''arguments : argument
                     | arguments COMMA argument
                     | empty
        '''
        if len(p) == 2:
            p[0] = [] if p[1] is None else [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    # function calls
    def p_function_call(self, p):
        'function_call : ID LPAREN arguments RPAREN'
        p[0] = ("function_call", p[1], p[3])

    # production for a function
    # TODO: Add loops and if statements
    def p_function(self, p):
        '''function : DEF ID LPAREN arguments RPAREN COLON NEWLINE INDENT complete_sentences DENT'''
        p[0] = ("function", p[2])

    # production for a class constructor method
    def p_class_constructor(self, p):
        '''class_constructor : DEF __INIT__ LPAREN arguments RPAREN COLON'''

    # production for a class
    def p_class(self, p):
        '''class : '''

    def parse(self, source, lexer):
        return self.parser.parse(source, lexer=lexer.lex)
