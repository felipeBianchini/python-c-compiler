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
    #                       #
    #   INITIAL PRODUCTION  #
    #                       #
    #########################

    def p_program(self, p):
        '''program : complete_sentence program
                   | complete_sentence
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    #########################
    #                       #
    #   OTHER PRODUCTIONS   #
    #                       #
    #########################

    def p_empty(self, p):
        'empty :'
        p[0] = None

    def p_optional_newline(self, p):
        '''optional_newline : NEWLINE
                            | empty'''
        p[0] = None

    def p_error(self, p):
        if p:
            token_type = p.type
            token_value = p.value
            lineno = p.lineno
            lexpos = p.lexpos
            print(f"\nSyntax error: unexpected token '{token_value}' (type: {token_type}) at line {lineno}, position {lexpos}")

    ############################################
    #                                          #
    #   PRODUCTIONS FOR DATATYPES AND SYMBOLS  #
    #                                          #
    ############################################

    def p_data_type(self, p):
        '''data_type : r_operation
                     | string_concat
                     | class_atribute_use
                     | NONE
        '''
        p[0] = p[1]

    def p_ref_data_type(self, p):
        '''ref_data_type : ID
                         | class_atribute_use         
        ''' 
        p[0] = p[1]

    def p_number(self, p):
        '''number : INTEGER 
                  | FLOAT'''
        p[0] = p[1]

    def p_string(self, p):
        '''string : MULTISTRING
                  | number_to_string
        '''
        p[0] = p[1]

    def p_arithmetic_symbol(self, p):
        '''arithmetic_symbol : PLUS 
                             | MINUS
                             | MUL 
                             | DIV 
                             | INT_DIV 
                             | MOD 
                             | POW'''
        p[0] = p[1]

    def p_assignment_symbol(self, p):
        '''assignment_symbol : ADD_ASSIGN 
                             | SUB_ASSIGN 
                             | MUL_ASSIGN 
                             | DIV_ASSIGN 
                             | MOD_ASSIGN 
                             | INT_DIV_ASSIGN 
                             | POW_ASSIGN'''
        p[0] = p[1]

    def p_relational_symbol(self, p):
        '''relational_symbol : EQUAL 
                             | NOT_EQUAL 
                             | GREATER 
                             | LESS 
                             | GREATER_EQUAL 
                             | LESS_EQUAL'''
        p[0] = p[1]

    def p_binary_logical_operator(self, p):
        '''binary_logical_operator : AND 
                                   | OR'''
        p[0] = p[1]

    def p_conditional_operator(self, p):
        '''conditional_operator : TRUE 
                                | FALSE'''
        p[0] = p[1]

    ############################################
    #                                          #
    #   PRODUCTIONS FOR SINGLE LINE SENTENCES  #
    #                                          #
    ############################################

    def p_sentence(self, p):
        '''sentence : operation
                     | function
                     | function_call
                     | class
        '''
        p[0] = p[1]

    def p_complete_sentence(self, p):
        'complete_sentence : sentence optional_newline'
        p[0] = p[1]

    def p_complete_sentences(self, p):
        '''complete_sentences : complete_sentence complete_sentences
                              | complete_sentence            
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    #############################################
    #                                           #
    #   PRODUCTIONS FOR SINGLE LINE OPERATIONS  #
    #                                           #
    #############################################

    def p_operation(self, p):
        '''operation : assignment_operation 
                     | simple_assignment_operation 
                     | r_operation
        '''
        print("p_operation")
        p[0] = p[1]

    def p_r_operation(self, p):
        '''r_operation : arithmetic_operation 
                       | binary_logical_operation
        '''
        p[0] = p[1]

    def p_simple_assignment_operation(self, p):
        '''simple_assignment_operation : ref_data_type ASSIGN data_type
                                       | ref_data_type ASSIGN r_operation
        '''
        p[0] = ("simple assignment operation", p[1], p[2], p[3])

    def p_assignment_operation(self, p):
        'assignment_operation : ID assignment_symbol number'
        p[0] = ("assignment operation", p[1], p[2], p[3])

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

    def p_relational_operation(self, p):
        '''relational_operation : LPAREN relational_operation RPAREN
                                | data_type relational_symbol data_type
        '''
        if len(p) == 4 and p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = ("relational operation", p[1], p[2], p[3])

    def p_unary_logical_operation(self, p):
        '''unary_logical_operation : NOT unary_logical_operation
                                   | LPAREN unary_logical_operation RPAREN
                                   | relational_operation
                                   | ID
                                   | conditional_operator
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = ('NOT', p[2])
        else:
            p[0] = p[2]

    def p_binary_logical_operation(self, p):
        '''binary_logical_operation : binary_logical_operation binary_logical_operator binary_logical_operation
                                    | LPAREN binary_logical_operation RPAREN
                                    | unary_logical_operation
        '''
        if len(p) == 4:
            if p[1] == '(':
                p[0] = p[2]
            else:
                p[0] = ("binary logical operation",  p[1], p[2], p[3])
        else:
            p[0] = p[1]

    ###################################################
    #                                                 #
    #   PRODUCTIONS FOR STRING OPERATIONS AND PRINTS  #
    #                                                 #
    ###################################################

    def p_number_to_string(self, p):
        'number_to_string : STR LPAREN number RPAREN'
        p[0] = ('num->str', p[1], p[3])

    def p_string_concat(self, p):
        '''string_concat : string_concat PLUS string
                         | string
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ("concat", p[1], p[3])

    ##############################################################
    #                                                            #
    #   PRODUCTIONS FOR FUNCTIONS, ARGUMENTS AND FUNCTION CALLS  #
    #                                                            #
    ##############################################################

    def p_argument(self, p):
        '''argument : ID
                    | ID COLON data_type
        '''
        if len(p) == 2:
            p[0] = ("argument", p[1], None)
        else:
            p[0] = ("argument", p[1], p[3])

    def p_arguments(self, p):
        '''arguments : argument
                     | arguments COMMA argument
                     | empty
        '''
        if len(p) == 2:
            result = [] if p[1] is None else [p[1]]
            p[0] = result
        else:
            p[0] = p[1] + [p[3]]

    def p_function_call(self, p):
        '''function_call : ID LPAREN arguments RPAREN
                         | class_atribute_use LPAREN arguments RPAREN
        '''
        print("p_function_call")
        p[0] = ("function_call", p[1], p[3])

    def p_return(self, p):
        '''return : RETURN
                  | RETURN data_type
                  | RETURN r_operation
        '''
        if len(p) == 2:
            p[0] = ('return', None)
        else:
            p[0] = ('return', p[2])

    def p_optional_return(self, p):
        '''optional_return : return
                           | empty
        '''
        p[0] = p[1]

    def p_function(self, p):
        '''function : DEF ID LPAREN arguments RPAREN COLON NEWLINE INDENT complete_sentences optional_return DENT'''
        print("p_function")

        p[0] = ("function", p[2], p[4], p[9], p[10])

    ###############################
    #                             #
    #   PRODUCTIONS FOR CLASSES   #
    #                             #
    ###############################

    def p_class_arguments(self, p):
        ''' class_arguments : SELF COMMA arguments
                            | SELF
        '''
        if len(p) == 4:
            p[0] = ["self"] + p[3]
        else:
            p[0] = ["self"]

    def p_class_atribute_use(self, p):
        'class_atribute_use : SELF DOT ID'
        p[0] = ("class atribute use", p[1], p[3])

    def p_class_method(self, p):
        '''class_method : DEF __INIT__ LPAREN class_arguments RPAREN COLON NEWLINE INDENT complete_sentences DENT
                        | DEF ID LPAREN class_arguments RPAREN COLON NEWLINE INDENT complete_sentences optional_return DENT
        '''
        if len(p) == 11:
            p[0] = ("class method", p[2], p[4], p[9])
        else: 
            p[0] = ("class method", p[2], p[4], p[9], p[10])

    def p_class_part(self, p):
        '''class_part : class_method
                      | complete_sentences
        '''
        p[0] = p[1]

    def p_class_parts(self, p):
        '''class_parts : class_parts class_part
                       | class_part
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_class(self, p):
        '''class : CLASS ID COLON NEWLINE INDENT class_parts DENT'''
        print("p_class")

        p[0] = ('class', p[2], p[6])

    def parse(self, source, lexer):
        result = self.parser.parse(source, lexer=lexer.lex, debug=True)
        return result
