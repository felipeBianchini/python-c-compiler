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

    # basic data types
    def p_data_type(self, p):
        '''data_type : NONE
                     | TRUE
                     | FALSE
        '''
        print(f">> data_type: {p[1]}")
        p[0] = p[1]

    # referentiable data types
    def p_ref_data_type(self, p):
        '''ref_data_type : ID
                         | objects_use         
        ''' 
        print(">> ref_data_type")
        p[0] = p[1]

    # for the use of objects
    # object.data
    def p_objects_use(self, p):
        'objects_use : ID DOT ID'
        print(">> objects_use")
        p[0] = ("class atribute use", p[1], p[3])

    # numbers
    def p_number(self, p):
        '''number : INTEGER 
                  | FLOAT'''
        print(">> number")
        p[0] = p[1]

    # strings
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

    #################################
    #   PRODUCTIONS FOR SENTENCES  #
    ################################

    # TODO: Add for, while, if
    # for a sentence, includes basically everything that can be done
    def p_sentence(self, p):
        '''sentence : function
                    | class
                    | function_call
                    | operation
        '''
        print(">> sentence")
        p[0] = p[1]

    # recursive rule for a group of sentences
    def p_sentences(self, p):
        '''sentences : sentence optional_newline
                     | sentences sentence optional_newline
        '''
        if len(p) == 3:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    #############################################
    #   PRODUCTIONS FOR SINGLE LINE OPERATIONS  #
    #############################################

    # single line operations
    # include two types of assignment operations
    def p_operation(self, p):
        '''operation : assignment_operation 
                     | simple_assignment_operation 
        '''
        print(">> operation")
        p[0] = p[1]

    # assignment operation that only involves =
    # only referentiable data can be assigned a value
    def p_simple_assignment_operation(self, p):
        '''simple_assignment_operation : ref_data_type ASSIGN expression
        '''
        print(">> simple_assignment_operation")
        p[0] = ("simple assignment operation", p[1], p[2], p[3])

    # other types of assignment operations
    # the other assignment symbols only work between a referentiable data and a number
    def p_assignment_operation(self, p):
        'assignment_operation : ID assignment_symbol number'
        print(">> assignment_operation")
        p[0] = ("assignment operation", p[1], p[2], p[3])

    # all types of operations and statements that return a value
    def p_expression(self, p):
        '''expression : ret_value_operation
                      | string_concat
                      | function_call
        '''
        print(f">> expression: {p[1]}")
        p[0] = p[1]

    # this works for all types of operations that return a value
    # includes arithmethic, logical and relational operations
    # they can all be combined since Python allows it
    def p_ret_value_operation(self, p):
        '''ret_value_operation : ret_value_operation arithmetic_symbol ret_value_operation
                               | ret_value_operation binary_logical_operator ret_value_operation
                               | ret_value_operation relational_symbol ret_value_operation
                               | LPAREN ret_value_operation RPAREN
                               | NOT ret_value_operation
                               | number
                               | ref_data_type
                               | data_type
        '''
        print(">> ret_value_operation")
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = ("unary_operation", "NOT", p[2])
        elif len(p) == 4:
            if p[1] == '(':
                p[0] = p[2]
            else:
                operator = p[2]
                if operator in ('+', '-', '*', '/', '//', '%', '**'):
                    p[0] = ("arithmetic_operation", p[1], operator, p[3])
                elif operator in ('AND', 'OR'): 
                    p[0] = ("logical_operation", p[1], operator, p[3])
                elif operator in ('==', '!=', '<', '>', '<=', '>='):
                    p[0] = ("relational_operation", p[1], operator, p[3])
                else:
                    p[0] = ("other_operation", p[1], operator, p[3])

    ###################################################
    #   PRODUCTIONS FOR STRING OPERATIONS AND PRINTS  #
    ###################################################

    # for str(number)
    def p_number_to_string(self, p):
        'number_to_string : STR LPAREN number RPAREN'
        print(">> number_to_string")
        p[0] = ('num->str', p[1], p[3])

    # string concatenation
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
    
    # a single argument
    # takes into account self defined arguments
    def p_argument(self, p):
        '''argument : expression
                    | ID COLON expression
        '''
        print(">> argument")
        if len(p) == 2:
            p[0] = ("argument", p[1], None)
        else:
            p[0] = ("argument", p[1], p[3])

    # recursive rule for arguments
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

    # for function calls
    # works for simple, normal function calls and function calls inside classes
    def p_function_call(self, p):
        '''function_call : ID LPAREN arguments RPAREN
                         | objects_use LPAREN arguments RPAREN
        '''
        print(">> function_call")
        p[0] = ("function_call", p[1], p[3])

    # for returns
    # works for both empty returns and return with a value
    def p_return(self, p):
        '''return : RETURN expression
                  | RETURN 
        '''
        print(">> return")
        if len(p) == 2:
            p[0] = ('return', None)
        else:
            p[0] = ('return expression', p[2])
    
    # for optional returns
    def p_optional_return(self, p):
        '''optional_return : return
                           | empty
        '''
        p[0] = p[1]

    # recursive rule for function body
    # takes into account that not all functions have a body and not all functions have returns
    def p_function_body(self, p):
        '''function_body : sentences optional_return NEWLINE
                         | return NEWLINE
                         | PASS NEWLINE
        '''
        print(">> function_body")
        if len(p) == 4:
            p[0] = ('complete function body', p[1], p[2])
        else:
            p[0] = ('incomplete function body', p[1])

    # for functions
    def p_function(self, p):
        '''function : DEF ID LPAREN arguments RPAREN COLON NEWLINE INDENT function_body DENT
        '''
        print(">> function")
        p[0] = ("function", p[2], p[4], p[9])

    ###############################
    #   PRODUCTIONS FOR CLASSES   #
    ###############################

    # for the body of a class
    def p_class_body(self, p):
        '''class_body : sentences
        '''
        print(">> class_body")
        p[0] = p[1]

    # for complete classes
    def p_class(self, p):
        '''class : CLASS ID COLON NEWLINE INDENT class_body DENT'''
        print(">> class")
        p[0] = ('class', p[2], p[6])

    def parse(self, source, lexer):
        result = self.parser.parse(source, lexer=lexer.lex, debug=True)        
        return result
