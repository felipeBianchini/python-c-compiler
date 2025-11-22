from re import DEBUG
from src.lexer import Lexer
from src.parser import Parser
from src.utils import Error
from src.symbol_table import SymbolTable
from src.visitor import Visitor

# Read file
with open("tests/a.py", "r", encoding='utf-8') as f:
    source_code = f.read()

# Create Lexer
errors = [] # An empty error queue is created and sent to the lexer
lexer = Lexer(errors=errors)
lexer.build()
lexer.input(source_code)

# Create Parser
parser = Parser()
parseTree = parser.parser.parse(source_code, lexer=lexer)
#print(parseTree)
'''
def print_list(tree, num = 0):
    for i in tree:
        if isinstance(i, list):
            print(f"Block Start {num + 1}\n")
            print_list(i, num + 1)
            print(f"Block_end{num+ 1}")
        else:
            print(i)
            print()

print("Full tree:")
for i in result:
    print(i)
    print()
'''

visitor = Visitor(symbol_table=parser.symtab, parse_tree=parseTree)
newCode = visitor.start()
print(newCode)