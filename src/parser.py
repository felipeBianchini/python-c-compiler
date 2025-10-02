import ply.yacc as yacc
from src.lexer import Lexer

class Parser:
    tokens = Lexer.tokens

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'), 
        ('nonassoc', 'EQUAL', 'NOT_EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MUL', 'DIV', 'INT_DIV', 'MOD'),
        ('right', 'POW'),
    )

    def __init__(self):
        self.parser = yacc.yacc(module=self, debug=True, debugfile='parser.out')
        
    #########################
    #   INITIAL PRODUCTION  #
    #########################

    def p_program(self, p):
        '''program : statement_list
        '''
        print(">> program")
        p[0] = p[1]

    def p_statement_list(self, p):
        '''statement_list : statement_list sentence optional_newline
                          | sentence optional_newline
        '''
        print(">> statement_list")
        if len(p) == 3:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + [p[2]]

    #########################
    #   OTHER PRODUCTIONS   #
    #########################

    def p_empty(self, p):
        'empty :'
        print(">> empty")
        p[0] = None

    def p_optional_newline(self, p):
        '''optional_newline : optional_newline NEWLINE
                            | NEWLINE
                            | empty'''
        print(">> optional_newline")
        p[0] = None

    def p_error(self, p):
        if p:
            token_type = p.type
            token_value = p.value
            lineno = p.lineno
            lexpos = p.lexpos
            print(f"\nSyntax error: unexpected token '{token_value}' (type: {token_type}) at line {lineno}, position {lexpos}")

    ############################################
    #   PRODUCTIONS FOR DATATYPES AND SYMBOLS  #
    ############################################

    def p_data_type(self, p):
        '''data_type : NONE
                     | TRUE
                     | FALSE
        '''
        print(f">> data_type: {p[1]}")
        p[0] = p[1]

    def p_ref_data_type(self, p):
        '''ref_data_type : ID
                         | class_atribute_use         
        ''' 
        print(">> ref_data_type")
        p[0] = p[1]

    def p_number(self, p):
        '''number : INTEGER 
                  | FLOAT'''
        print(">> number")
        p[0] = p[1]

    def p_string(self, p):
        '''string : MULTISTRING
                  | STRING
                  | number_to_string
        '''
        print(">> string")
        p[0] = p[1]

    def p_arithmetic_symbol(self, p):
        '''arithmetic_symbol : PLUS 
                             | MINUS
                             | MUL 
                             | DIV 
                             | INT_DIV 
                             | MOD 
                             | POW'''
        print(">> arithmetic_symbol")
        p[0] = p[1]

    def p_assignment_symbol(self, p):
        '''assignment_symbol : ADD_ASSIGN 
                             | SUB_ASSIGN 
                             | MUL_ASSIGN 
                             | DIV_ASSIGN 
                             | MOD_ASSIGN 
                             | INT_DIV_ASSIGN 
                             | POW_ASSIGN'''
        print(">> assignment_symbol")
        p[0] = p[1]

    def p_relational_symbol(self, p):
        '''relational_symbol : EQUAL 
                             | NOT_EQUAL 
                             | GREATER 
                             | LESS 
                             | GREATER_EQUAL 
                             | LESS_EQUAL'''
        print(">> relational_symbol")
        p[0] = p[1]

    def p_binary_logical_operator(self, p):
        '''binary_logical_operator : AND 
                                   | OR'''
        print(">> binary_logical_operator")
        p[0] = p[1]

    def p_conditional_operator(self, p):
        '''conditional_operator : TRUE 
                                | FALSE'''
        print(">> conditional_operator")
        p[0] = p[1]

    ############################################
    #   PRODUCTIONS FOR SINGLE LINE SENTENCES  #
    ############################################

    def p_sentence(self, p):
        '''sentence : function
                    | class
                    | function_call
                    | operation
        '''
        print(">> sentence")
        p[0] = p[1]

    #############################################
    #   PRODUCTIONS FOR SINGLE LINE OPERATIONS  #
    #############################################

    def p_operation(self, p):
        '''operation : assignment_operation 
                     | simple_assignment_operation 
        '''
        print(">> operation")
        p[0] = p[1]

    def p_simple_assignment_operation(self, p):
        '''simple_assignment_operation : ref_data_type ASSIGN expression
        '''
        print(">> simple_assignment_operation")
        p[0] = ("simple assignment operation", p[1], p[2], p[3])

    def p_assignment_operation(self, p):
        'assignment_operation : ID assignment_symbol number'
        print(">> assignment_operation")
        p[0] = ("assignment operation", p[1], p[2], p[3])

    # Expresiones que retornan valores
    def p_expression(self, p):
        '''expression : 
                      | string_concat
                      | function_call
                      | data_type
        '''
        print(f">> expression: {p[1]}")
        p[0] = p[1]

    def p_logical_expression(self, p):
        '''logical_expression : logical_expression 
        '''
        if len(p) == 2:
            print(f">> logical_expression (simple): {p[1]}")
            p[0] = p[1]
        else:
            print(f">> logical_expression (OR): {p[1]} OR {p[3]}")
            p[0] = ('or', p[1], p[3])

    def p_comparison_expression(self, p):
        ''' comparison_operation : comparison_operation relational_symbol expression
                                 | LPAREN comparison_operation RPAREN
        '''

    ###################################################
    #   PRODUCTIONS FOR STRING OPERATIONS AND PRINTS  #
    ###################################################

    def p_number_to_string(self, p):
        'number_to_string : STR LPAREN number RPAREN'
        print(">> number_to_string")
        p[0] = ('num->str', p[1], p[3])

    def p_string_concat(self, p):
        '''string_concat : string_concat PLUS string
                         | string
        '''
        print(">> string_concat")
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ("concat", p[1], p[3])

    ##############################################################
    #   PRODUCTIONS FOR FUNCTIONS, ARGUMENTS AND FUNCTION CALLS  #
    ##############################################################
    
    def p_argument(self, p):
        '''argument : expression
                    | ID COLON expression
        '''
        print(">> argument")
        if len(p) == 2:
            p[0] = ("argument", p[1], None)
        else:
            p[0] = ("argument", p[1], p[3])

    def p_arguments(self, p):
        '''arguments : argument
                     | arguments COMMA argument
                     | empty
        '''
        print(">> arguments")
        if len(p) == 2:
            result = [] if p[1] is None else [p[1]]
            p[0] = result
        else:
            p[0] = p[1] + [p[3]]

    def p_function_call(self, p):
        '''function_call : ID LPAREN arguments RPAREN
                         | class_atribute_use LPAREN arguments RPAREN
        '''
        print(">> function_call")
        p[0] = ("function_call", p[1], p[3])

    def p_return(self, p):
        '''return : RETURN expression
                  | RETURN 
        '''
        print(">> return")
        if len(p) == 2:
            p[0] = ('return', None)
        else:
            p[0] = ('return expression', p[2])
    
    def p_function_body(self, p):
        '''function_body : function_body sentence return
                         | function_body sentence
                         | sentence
                         | return
        '''
        print(">> function_body")
        if len(p) == 3:
            p[0] = ('complete function body', p[1], p[2])
        else:
            p[0] = ('incomplete function body', p[1])

    def p_function(self, p):
        '''function : DEF ID LPAREN arguments RPAREN COLON NEWLINE INDENT function_body NEWLINE DENT
        '''
        print(">> function")
        p[0] = ("function", p[2], p[4], p[9])

    ###############################
    #   PRODUCTIONS FOR CLASSES   #
    ###############################

    def p_class_arguments(self, p):
        ''' class_arguments : SELF COMMA arguments
                            | SELF
        '''
        print(">> class_arguments")
        if len(p) == 4:
            p[0] = ["self"] + p[3]
        else:
            p[0] = ["self"]

    def p_class_atribute_use(self, p):
        'class_atribute_use : SELF DOT ID'
        print(">> class_atribute_use")
        p[0] = ("class atribute use", p[1], p[3])

    def p_class_method(self, p):
        '''class_method : DEF __INIT__ LPAREN class_arguments RPAREN COLON NEWLINE INDENT function_body DENT
                        | DEF ID LPAREN class_arguments RPAREN COLON NEWLINE INDENT function_body DENT
        '''
        print(">> class_method")
        if len(p) == 13:
            p[0] = ("class method", p[2], p[4], p[9])
        else: 
            p[0] = ("class method", p[2], p[4], p[9], p[10])

    def p_class_part(self, p):
        '''class_part : class_method
        '''
        print(">> class_part")
        p[0] = p[1]

    def p_class_body(self, p):
        '''class_body : class_body class_part
                     | class_part
        '''
        print(">> class_body")
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_class(self, p):
        '''class : CLASS ID COLON NEWLINE INDENT class_body optional_newline DENT'''
        print(">> class")
        p[0] = ('class', p[2], p[6])

    def parse(self, source, lexer):
        result = self.parser.parse(source, lexer=lexer.lex, debug=True)        
        return result
