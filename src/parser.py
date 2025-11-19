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
        ('left', 'IN')
    )

    def __init__(self):
        self.parser = yacc.yacc(module=self, debug=True, debugfile='parser.out')
        
    #########################
    #   INITIAL PRODUCTION  #
    #########################

    def p_program(self, p):
        '''program : optional_newline statement_list
        '''
        print(">> program")
        p[0] = p[2]

    def p_statement_list(self, p):
        '''statement_list : statement_list sentence optional_newline
                          | sentence optional_newline
        '''
        print(">> statement_list")
        if len(p) == 3:
            p[0] = [p[1]]
        else:
            p[1].append(p[2])
            p[0] = p[1]

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
        if len(p) > 1 and p[1] == '\n':
            print(">> optional_newline (Real)")
        else:
            print(">> optional_newline (Empty)")
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
                  | string_part
        '''
        print(f">> string {p[1]}")
        p[0] = p[1]

    def p_string_part(self, p):
        '''string_part : string_concat LBRACKET INTEGER COLON INTEGER RBRACKET
                       | string_concat LBRACKET INTEGER RBRACKET
        '''
        
        if len(p) == 7:
            p[0] = p[1][p[3]:p[5]]
        else:
            p[0] = p[1][p[3]]

        print(f">> string_part {p[0]}")

    def p_list(self, p):
        '''list : ret_value_operation
                | string
                | list COMMA string
                | list COMMA ret_value_operation
        '''
        if len(p) == 2:
            print(f">> list {p[1]}")
        else:
            print(f">> list {p[1]}, {p[3]}")
            if type(p[1]) != list:
                p[1] = [p[1]]
            p[1].append(p[3])
        
        p[0] = p[1]
    
    def p_array(self, p):
        '''array : LBRACKET list RBRACKET
        '''
        print(f">> array {p[2]}")
        p[0] = p[2]

    def p_set(self, p):
        '''set : LBRACE list RBRACE
        '''
        print(f">> set {p[2]}")
        p[0] = p[2]

    def p_dict_set(self, p):
        '''dict_set : dict
                    | set
        '''
        p[0] = p[1]

    def p_tuple(self, p):
        '''tuple : LPAREN list RPAREN
        '''
        print(f">> tuple {p[2]}")
        p[0] = p[2]

    def p_dict_trash(self,p):
        '''dict_trash : NEWLINE
                      | INDENT
                      | DENT
                      | dict_trash dict_trash
        '''
        print(">> dict trash")
        p[0] = None
    
    def p_optional_dict_trash(self, p):
        '''optional_dict_trash : dict_trash
                               | empty
        '''
        print(">> optional_dict_trash")
        p[0] = None

    def p_dict(self, p):
        '''dict : LBRACE optional_dict_trash dict_items_opt optional_dict_trash RBRACE
        '''
        print(">> dict")
        p[0] = p[3] if p[3] is not None else {}

    def p_dict_items_opt(self, p):
        '''dict_items_opt : dict_items
                          | empty'''
        print(">> dict_items_opt")
        p[0] = p[1]

    def p_dict_items(self, p):
        '''dict_items : dict_item
                      | dict_items COMMA optional_dict_trash dict_item
        '''
        print(">> dict_items")
        if len(p) == 2:
            p[0] = {p[1][0]: p[1][1]}
        else:
            p[0] = p[1]
            p[0][p[4][0]] = p[4][1]

    def p_dict_item(self, p):
        '''dict_item : key COLON ret_value_operation
                     | key COLON final_string
                     | key COLON array
                     | key COLON dict
                     | key COLON tuple
        '''
        print(f">> dict item {p[3]}")
        p[0] = (p[1], p[3])

    def p_key(self, p):
        '''key : final_string
               | ret_value_operation
        '''
        print(f">> key {p[1]}")
        p[0] = p[1]

    def p_next(self, p):
        '''next_clause : NEXT LPAREN ref_data_type RPAREN
        '''
        print(f">> next_clause {p[3]}")
        p[0] = ('NEXT', p[3])

    def p_access_id(self, p):
        '''access_id : ID LBRACKET INTEGER RBRACKET
                     | ID LBRACKET INTEGER COLON INTEGER RBRACKET
                     | ID LBRACKET ref_data_type RBRACKET
                     | ID LBRACKET final_string RBRACKET

        '''
        if len(p) == 7:
            print(f">> access_id {p[1]} {p[3]} {p[5]}")
            p[0] = ("access_id", p[1], p[3], p[5])
        else:
            print(f">> access_id {p[1]} {p[3]}")
            p[0] = ("access_id", p[1], p[3])

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

    # for a sentence, includes basically everything that can be done
    def p_sentence(self, p):
        '''sentence : function
                    | class
                    | function_call
                    | operation
                    | conditional
                    | print
                    | loop
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
    
    def p_print(self, p):
        '''print : PRINT LPAREN expression RPAREN
        '''
        print(f">> print {p[3]}")
        p[0] = ("print_call", p[3])

    #############################################
    #   PRODUCTIONS FOR SINGLE LINE OPERATIONS  #
    #############################################

    # single line operations
    # include two types of assignment operations
    def p_operation(self, p):
        '''operation : assignment_operation 
                     | simple_assignment_operation 
                     | array_assignment
                     | iter_assignment
                     | dict_assignment
        '''
        print(">> operation")
        p[0] = p[1]

    def p_assign_iter(self, p):
        '''iter_assignment : ref_data_type ASSIGN ITER LPAREN ref_data_type RPAREN
                           | ref_data_type ASSIGN ITER LPAREN expression RPAREN
        '''
        print(">> iter_assignment")
        p[0] = (p[1], p[5])

    def p_assign_dict(self, p):
        '''dict_assignment : ref_data_type ASSIGN dict
        '''
        print(">> dict_assignment")
        p[0] = (p[1], p[3])

    def p_assign_array(self, p):
        '''array_assignment : ref_data_type ASSIGN array
                            | ref_data_type ASSIGN tuple
                            | ref_data_type ASSIGN dict_set
        '''
        print(">> array_assignment")
        if isinstance(p[3], dict):
            p[0] = ("dictionary assignment", p[1], p[2], p[3])
        else:    
            p[0] = ("array assignment", p[1], p[2], p[3])

    def p_simple_assignment_operation(self, p):
        '''simple_assignment_operation : ref_data_type ASSIGN expression
        '''
        print(">> simple_assignment_operation")
        p[0] = ("simple_assignment_operation", p[1], p[2], p[3])

    # other types of assignment operations
    # the other assignment symbols only work between a referentiable data and a number
    def p_assignment_operation(self, p):
        'assignment_operation : ID assignment_symbol number'
        print(">> assignment_operation")
        p[0] = ("assignment_operation", p[1], p[2], p[3])

    # all types of operations and statements that return a value
    def p_expression(self, p):
        '''expression : ret_value_operation
                      | final_string
                      | next_clause
                      | array
                      | tuple
                      | dict_set
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
                               | function_call
                               | check_in_collection
                               | access_id
        '''
        print(">> ret_value_operation ")
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
                elif operator in ('and', 'or'): 
                    p[0] = ("logical_operation", p[1], operator, p[3])
                elif operator in ('==', '!=', '<', '>', '<=', '>='):
                    p[0] = ("relational_operation", p[1], operator, p[3])
                else:
                    p[0] = ("other_operation", p[1], operator, p[3])

    def p_check_in_collection(self, p):
        'check_in_collection : ret_value_operation IN ref_data_type'
        p[0] = ('in', p[1], p[3])

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
                         | LPAREN string_concat PLUS string RPAREN
                         | string
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 6:
            p[0] = p[2] + p[4]
        else:
            p[0] = p[1] + p[3]
        print(f">> String concat: {p[0]}")

    def p_final_string(self, p):
        '''final_string : string_concat
        '''
        p[0] = f"\"{p[1]}\""
        print(f">> final_string: {p[0]}")

    ##############################################################
    #   PRODUCTIONS FOR FUNCTIONS, ARGUMENTS AND FUNCTION CALLS  #
    ##############################################################
    
    # a single argument
    # takes into account self defined arguments
    def p_argument(self, p):
        '''argument : expression
                    | ID COLON expression
                    | ID ASSIGN expression
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
                         | sentences
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

    def p_block_body(self, p):
        '''block_body : sentences optional_return optional_newline
                      | return optional_newline
                      | PASS optional_newline
        '''
        print(">> block_body")
        if len(p) == 3:
            p[0] = ('complete block body', p[1], p[2])
        else:
            p[0] = ('incomplete block body', p[1])

    ################################
    # PRODUCTIONS FOR IF-ELIF-ELSE #
    ################################

    def p_conditional(self, p):
        '''conditional : if_clause INDENT block_body DENT elif_list else_clause
                       | if_clause INDENT block_body DENT elif_list
                       | if_clause INDENT block_body DENT else_clause
                       | if_clause INDENT block_body DENT
        '''
        print(f">> conditional")
        if len(p) == 5:
            # Just if
            p[0] = ('conditional', ('if', p[1], p[3]))
        elif len(p) == 6:
            # if + elif(s) OR if + else
            p[0] = ('conditional', ('if', p[1], p[3]), p[5])
        else:
            # if + elif(s) + else
            p[0] = ('conditional', ('if', p[1], p[3]), p[5], p[6])

    def p_elif_list(self, p):
        '''elif_list : elif_list elif_clause INDENT block_body DENT
                     | elif_clause INDENT block_body DENT
        '''
        print(">> elif_list")
        if len(p) == 5:
            # Single elif
            p[0] = ('elif_list', [('elif', p[1], p[3])])
        else:
            # Multiple elifs
            if p[1][0] == 'elif_list':
                p[0] = ('elif_list', p[1][1] + [('elif', p[2], p[4])])
            else:
                p[0] = ('elif_list', [p[1], ('elif', p[2], p[4])])

    def p_if_clause(self, p):
        '''if_clause : IF ret_value_operation COLON NEWLINE
        '''
        print(">> if_clause")
        p[0] = p[2]

    def p_elif_clause(self, p):
        '''elif_clause : ELIF ret_value_operation COLON NEWLINE
        '''
        print(">> elif_clause")
        p[0] = p[2]

    def p_else_clause(self, p):
        '''else_clause : ELSE COLON NEWLINE INDENT block_body DENT
        '''
        print(">> else_clause")
        p[0] = ('else', p[5])

    ###############################
    #   PRODUCTIONS FOR LOOPS     #
    ###############################

    def p_in_clause(self, p):
        '''in_clause : ID IN ref_data_type
                     | ID IN expression
                     | ID IN RANGE LPAREN ret_value_operation RPAREN
        '''
        if len(p) == 4:
            print(f">> in_clause {p[1]}, {p[3]}")
            p[0] = ('in_clause', p[1], p[3])
        else:
            print(f">> in_range_clause {p[1]}, {p[5]}")
            p[0] = ('in_range_clause', p[1], p[5])

    def p_for_clause(self, p):
        '''for_clause : FOR in_clause COLON NEWLINE
        '''
        print(">> for_clause")
        p[0] = ('for', p[2])

    def p_while_clause(self, p):
        '''while_clause : WHILE ret_value_operation COLON NEWLINE
        '''
        print(">> while_clause")
        p[0] = ('while', p[2])

    # Loop-specific statement that includes break/continue
    def p_loop_statement(self, p):
        '''loop_statement : function
                          | class
                          | function_call
                          | operation
                          | loop_conditional
                          | print
                          | loop
                          | BREAK
                          | CONTINUE
        '''
        print(f">> loop_statement: {p[1]}")
        p[0] = p[1]

    # Loop statements can be repeated
    def p_loop_statements(self, p):
        '''loop_statements : loop_statement optional_newline
                           | loop_statements loop_statement optional_newline
        '''
        if len(p) == 3:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    # Loop body is similar to block_body but allows break/continue
    def p_loop_body(self, p):
        '''loop_body : loop_statements optional_return
                     | return
                     | PASS
        '''
        print(f">> loop_body")
        if len(p) == 3:
            p[0] = ('complete loop body', p[1], p[2])
        else:
            p[0] = ('simple loop body', p[1])

    # Conditionals inside loops
    def p_loop_conditional(self, p):
        '''loop_conditional : loop_if_clause INDENT loop_body DENT loop_elif_list loop_else_clause
                            | loop_if_clause INDENT loop_body DENT loop_elif_list
                            | loop_if_clause INDENT loop_body DENT loop_else_clause
                            | loop_if_clause INDENT loop_body DENT
        '''
        print(f">> loop_conditional")
        if len(p) == 5:
            p[0] = ('loop_conditional', ('if', p[1], p[3]))
        elif len(p) == 6:
            p[0] = ('loop_conditional', ('if', p[1], p[3]), p[5])
        elif len(p) == 7:
            p[0] = ('loop_conditional', ('if', p[1], p[3]), p[5], p[6])

    def p_loop_elif_list(self, p):
        '''loop_elif_list : loop_elif_list loop_elif_clause INDENT loop_body DENT
                          | loop_elif_clause INDENT loop_body DENT
        '''
        print(">> loop_elif_list")
        if len(p) == 5:
            p[0] = ('elif_list', [('elif', p[1], p[3])])
        else:
            if p[1][0] == 'elif_list':
                p[0] = ('elif_list', p[1][1] + [('elif', p[2], p[4])])
            else:
                p[0] = ('elif_list', [p[1], ('elif', p[2], p[4])])

    def p_loop_if_clause(self, p):
        '''loop_if_clause : IF ret_value_operation COLON NEWLINE
        '''
        print(">> loop_if_clause")
        p[0] = p[2]

    def p_loop_elif_clause(self, p):
        '''loop_elif_clause : ELIF ret_value_operation COLON NEWLINE
        '''
        print(">> loop_elif_clause")
        p[0] = p[2]

    def p_loop_else_clause(self, p):
        '''loop_else_clause : ELSE COLON NEWLINE INDENT loop_body DENT
        '''
        print(">> loop_else_clause")
        p[0] = ('else', p[5])

    def p_loop(self, p):
        '''loop : for_clause INDENT loop_body DENT
                | while_clause INDENT loop_body DENT
        '''
        print(f">> loop {p[1]}, {p[3]}")
        p[0] = ("loop", p[1], p[3])

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
