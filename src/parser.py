import ply.yacc as yacc
from src.lexer import Lexer

class Parser:
    tokens = Lexer.tokens

    def __init__(self):
        self.parser = yacc.yacc(module=self, debug=True)

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
            p[0] = p[1] + [p[2]]

    #########################
    #                       #
    #   OTHER PRODUCTIONS   #
    #                       #
    #########################

    # for empty rules
    def p_empty(self, p):
        'empty :'
        p[0] = None

    # for optional newlines
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


    ############################################
    #                                          #
    #   PRODUCTIONS FOR DATATYPES AND SYMBOLS  #
    #                                          #
    ############################################

    # production for all datatypes
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
    def p_string(self, p):
        '''string : STRING 
                  | MULTISTRING
                  | number_to_string
        '''
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

    # production for all logical operators
    # NOT is unary
    def p_binary_logical_operator(self, p):
        '''binary_logical_operator : AND 
                                   | OR'''
        p[0] = p[1]

    # production for conditional operators
    def p_conditional_operator(self, p):
        '''conditional_operator : TRUE 
                                | FALSE'''
        p[0] = p[1]

    ############################################
    #                                          #
    #   PRODUCTIONS FOR SINGLE LINE SENTENCES  #
    #                                          #
    ############################################

    # production for complete sentences
    # this includes single line operations and compound sentences (functions, loops, ifs, classes)
    # TODO: Add loops and if sentences
    def p_sentence(self, p):
        '''sentence : operation
                     | function
                     | function_call
                     | class
        '''
        p[0] = p[1]

    # production for a complete sentence including possible newlines
    def p_complete_sentence(self, p):
        'complete_sentence : sentence optional_newline'
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

    #############################################
    #                                           #
    #   PRODUCTIONS FOR SINGLE LINE OPERATIONS  #
    #                                           #
    #############################################

    # production for all types of one single line operations
    def p_operation(self, p):
        '''operation : relational_operation 
                     | arithmetic_operation 
                     | assignment_operation
                     | unary_logical_operation
                     | binary_logical_operation'''
        p[0] = p[1]

    # production for assignment operations
    def p_assignment_operation(self, p):
        'assignment_operation : ID assignment_symbol data_type'
        p[0] = ("assignment operation", p[1], p[2], p[3])

    # production for arithmetic operations
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

    # production for relational operations
    def p_relational_operation(self, p):
        '''relational_operation : LPAREN relational_operation RPAREN
                                | data_type relational_symbol data_type
        '''
        if len(p) == 4 and p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = ("relational operation", p[1], p[2], p[3])

    # production for unary logical operations
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
            p[0] = p[1]

    # production for binary logical operations
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

    # production for string method that converts numbers to strings
    # str(number)
    def p_number_to_string(self, p):
        'number_to_string : STR LPAREN number RPAREN'
        p[0] = ('num->str', p[1], p[3])

    def p_string_concat(self, p):
        '''string_concat : string_concat ADD string
                        | string
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ("concat", p[1], p[3])

    # TODO
    def p_print(self, p):
        '''print : '''

    ##############################################################
    #                                                            #
    #   PRODUCTIONS FOR fUNCTIONS, ARGUMENTS AND FUNCTION CALLS  #
    #                                                            #
    ##############################################################

    # production for a single function argument
    def p_argument(self, p):
        '''argument : ID
                    | data_type
                    | ID COLON data_type
        '''
        if len(p) == 2:
            p[0] = ("argument", p[1], None)
        else:
            p[0] = ("argument", p[1], p[3])

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

    # production for function calls
    def p_function_call(self, p):
        'function_call : ID LPAREN arguments RPAREN'
        p[0] = ("function_call", p[1], p[3])

    # production for a function
    def p_function(self, p):
        '''function : DEF ID LPAREN arguments RPAREN COLON NEWLINE INDENT complete_sentences DENT'''
        p[0] = ("function", p[2])

    ###############################
    #                             #
    #   PRODUCTIONS FOR CLASSES   #
    #                             #
    ###############################

    # TODO: include ifs and loops
    def p_class_action(self, p):
        '''class_action : class_atribute_use
                        | class_method_use
                        |  
                        | PASS      
        '''
        p[0] = p[1]

    def p_class_atribute_use(self, p):
        'class_atribute_use : SELF DOT ID'
        p[0] = ("class atribute use", p[1], p[3])

    def p_class_method_use(self, p):
        'class_method_use : SELF DOT ID LPAREN arguments RPAREN'
        p[0] = ("class method use", p[1], p[3])

    def p_class_constructor_atributes(self, p):
        'class_constructor_atributes : SELF DOT ID EQUAL data_type' 
        p[0] = ("class constructor atributes", p[1], p[3])

    # production for a class constructor method
    def p_class_constructor(self, p):
        '''class_constructor : DEF __INIT__ LPAREN arguments RPAREN COLON INDENT class_action DENT'''
        p[0] = ("class constructor", p[2])

    def p_class_method(self, p):
        '''class_method : DEF ID LPAREN arguments RPAREN COLON NEWLINE INDENT complete_sentences DENT'''
        p[0] = ("class method", p[2])

    # production for a class
    def p_class(self, p):
        '''class : '''

    # TODO
    ##########################################
    #                                        #
    #   PRODUCTIONS FOR IF STATEMENTS LOOP   #
    #                                        #
    ##########################################

    # TODO
    ##############################
    #                            #
    #   PRODUCTIONS WHILE LOOP   #
    #                            #
    ##############################

    # TODO
    ############################
    #                          #
    #   PRODUCTIONS FOR LOOP   #
    #                          #
    ############################

    def parse(self, source, lexer):
        return self.parser.parse(source, lexer=lexer.lex)
