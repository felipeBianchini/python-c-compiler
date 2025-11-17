"""
Parser minimalista que SOLO reconoce:
- Funciones con parámetros y return
- Variables con tipado dinámico
- if/elif/else
- while loops
- for loops con range()
- Operadores: +, -, *, /, %, ==, !=, <, >, <=, >=, and, or, not
- Llamadas a funciones
- print()
"""

import ply.yacc as yacc
from src.lexer import Lexer
from src.ast_nodes import *

class Parser:
    tokens = Lexer.tokens

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'), 
        ('nonassoc', 'EQUAL', 'NOT_EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MUL', 'DIV', 'MOD'),
    )

    def __init__(self):
        self.parser = yacc.yacc(module=self, debug=True, debugfile='parser.out')
        
    #########################
    #   PROGRAMA PRINCIPAL  #
    #########################

    def p_program(self, p):
        '''program : statement_list
        '''
        p[0] = Program(p[1] if p[1] else [])

    def p_statement_list(self, p):
        '''statement_list : statement_list statement
                          | statement
                          | empty
        '''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            p[0] = (p[1] if p[1] else []) + ([p[2]] if p[2] else [])

    def p_empty(self, p):
        'empty :'
        p[0] = None

    #########################
    #   SENTENCIAS          #
    #########################

    def p_statement(self, p):
        '''statement : function_def
                     | assignment
                     | if_statement
                     | while_statement
                     | for_statement
                     | return_statement
                     | expression_statement
                     | PASS
                     | BREAK
                     | CONTINUE
        '''
        if isinstance(p[1], str):
            if p[1] == 'pass':
                p[0] = Pass(p.lineno(1))
            elif p[1] == 'break':
                p[0] = Break(p.lineno(1))
            elif p[1] == 'continue':
                p[0] = Continue(p.lineno(1))
            else:
                p[0] = None
        else:
            p[0] = p[1]

    #########################
    #   FUNCIONES           #
    #########################

    def p_function_def(self, p):
        '''function_def : DEF ID LPAREN params RPAREN COLON suite
        '''
        p[0] = FunctionDef(
            name=p[2],
            params=p[4] if p[4] else [],
            body=p[7] if p[7] else [],
            lineno=p.lineno(1)
        )

    def p_params(self, p):
        '''params : param_list
                  | empty
        '''
        p[0] = p[1]

    def p_param_list(self, p):
        '''param_list : param_list COMMA ID
                      | ID
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_return_statement(self, p):
        '''return_statement : RETURN expression
                            | RETURN
        '''
        if len(p) == 3:
            p[0] = Return(p[2], p.lineno(1))
        else:
            p[0] = Return(None, p.lineno(1))

    #########################
    #   ASIGNACIONES        #
    #########################

    def p_assignment(self, p):
        '''assignment : ID ASSIGN expression
        '''
        p[0] = Assignment(
            target=p[1],
            value=p[3],
            lineno=p.lineno(1)
        )

    #########################
    #   CONDICIONALES       #
    #########################

    def p_if_statement(self, p):
        '''if_statement : IF expression COLON suite elif_clauses else_clause
                        | IF expression COLON suite elif_clauses
                        | IF expression COLON suite else_clause
                        | IF expression COLON suite
        '''
        elif_parts = []
        else_body = None
        
        if len(p) == 7:
            elif_parts = p[5] if p[5] else []
            else_body = p[6]
        elif len(p) == 6:
            if isinstance(p[5], list):
                elif_parts = p[5]
            else:
                else_body = p[5]
        
        p[0] = If(
            condition=p[2],
            then_body=p[4],
            elif_parts=elif_parts,
            else_body=else_body,
            lineno=p.lineno(1)
        )

    def p_elif_clauses(self, p):
        '''elif_clauses : elif_clauses ELIF expression COLON suite
                        | ELIF expression COLON suite
        '''
        if len(p) == 6:
            p[0] = p[1] + [(p[3], p[5])]
        else:
            p[0] = [(p[2], p[4])]

    def p_else_clause(self, p):
        '''else_clause : ELSE COLON suite
        '''
        p[0] = p[3]

    #########################
    #   BUCLES              #
    #########################

    def p_while_statement(self, p):
        '''while_statement : WHILE expression COLON suite
        '''
        p[0] = While(
            condition=p[2],
            body=p[4],
            lineno=p.lineno(1)
        )

    def p_for_statement(self, p):
        '''for_statement : FOR ID IN expression COLON suite
        '''
        p[0] = For(
            target=p[2],
            iterable=p[4],
            body=p[6],
            lineno=p.lineno(1)
        )

    #########################
    #   SUITE (BLOQUE)      #
    #########################

    def p_suite(self, p):
        '''suite : simple_stmt
                 | NEWLINE INDENT statement_list DEDENT
        '''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] else []
        else:
            p[0] = p[3] if p[3] else []

    def p_simple_stmt(self, p):
        '''simple_stmt : statement NEWLINE
        '''
        p[0] = p[1]

    #########################
    #   EXPRESIONES         #
    #########################

    def p_expression_statement(self, p):
        '''expression_statement : expression
        '''
        # Solo si es una llamada a función (ej: print())
        if isinstance(p[1], FunctionCall):
            p[0] = ExpressionStatement(p[1], p.lineno(1))
        else:
            p[0] = None

    def p_expression(self, p):
        '''expression : or_expr
        '''
        p[0] = p[1]

    def p_or_expr(self, p):
        '''or_expr : or_expr OR and_expr
                   | and_expr
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], 'or', p[3], p.lineno(2))

    def p_and_expr(self, p):
        '''and_expr : and_expr AND not_expr
                    | not_expr
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], 'and', p[3], p.lineno(2))

    def p_not_expr(self, p):
        '''not_expr : NOT not_expr
                    | comparison
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = UnaryOp('not', p[2], p.lineno(1))

    def p_comparison(self, p):
        '''comparison : arith_expr comp_op arith_expr
                      | arith_expr
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3], p.lineno(2))

    def p_comp_op(self, p):
        '''comp_op : EQUAL
                   | NOT_EQUAL
                   | LESS
                   | GREATER
                   | LESS_EQUAL
                   | GREATER_EQUAL
        '''
        p[0] = p[1]

    def p_arith_expr(self, p):
        '''arith_expr : arith_expr PLUS term
                      | arith_expr MINUS term
                      | term
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3], p.lineno(2))

    def p_term(self, p):
        '''term : term MUL factor
                | term DIV factor
                | term MOD factor
                | factor
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3], p.lineno(2))

    def p_factor(self, p):
        '''factor : PLUS factor
                  | MINUS factor
                  | atom
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p[1] == '-':
                p[0] = UnaryOp('-', p[2], p.lineno(1))
            else:
                p[0] = p[2]

    def p_atom(self, p):
        '''atom : ID
                | number
                | string
                | TRUE
                | FALSE
                | NONE
                | function_call
                | LPAREN expression RPAREN
        '''
        if len(p) == 2:
            if isinstance(p[1], str):
                if p[1] in ('True', 'False'):
                    p[0] = Literal(p[1] == 'True', 'bool', p.lineno(1))
                elif p[1] == 'None':
                    p[0] = Literal(None, 'none', p.lineno(1))
                else:
                    # Es un ID
                    p[0] = Identifier(p[1], p.lineno(1))
            else:
                p[0] = p[1]
        else:
            p[0] = p[2]

    def p_number(self, p):
        '''number : INTEGER
                  | FLOAT
        '''
        if isinstance(p[1], float):
            p[0] = Literal(p[1], 'float', p.lineno(1))
        else:
            p[0] = Literal(p[1], 'int', p.lineno(1))

    def p_string(self, p):
        '''string : STRING
        '''
        p[0] = Literal(p[1], 'str', p.lineno(1))

    #########################
    #   LLAMADAS A FUNCIÓN  #
    #########################

    def p_function_call(self, p):
        '''function_call : ID LPAREN arguments RPAREN
        '''
        p[0] = FunctionCall(
            name=p[1],
            args=p[3] if p[3] else [],
            lineno=p.lineno(1)
        )

    def p_arguments(self, p):
        '''arguments : argument_list
                     | empty
        '''
        p[0] = p[1]

    def p_argument_list(self, p):
        '''argument_list : argument_list COMMA expression
                         | expression
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    #########################
    #   ERROR               #
    #########################

    def p_error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}: unexpected '{p.value}' ({p.type})")
        else:
            print("Syntax error at EOF")

    def parse(self, source, lexer):
        result = self.parser.parse(source, lexer=lexer.lex, debug=True)        
        return result