from re import DEBUG
from src.lexer import Lexer
from src.parser import Parser
from src.utils import Error
from src.symbol_table import SymbolTable
from src.visitor import Visitor
import tkinter as tk
from tkinter import filedialog

# Read file
input_path = "tests/a.py"
with open(input_path, "r", encoding='utf-8') as f:
    source_code = f.read()

# Create Lexer
errors = [] # An empty error queue is created and sent to the lexer
lexer = Lexer(errors=errors)
lexer.build()
lexer.input(source_code)

# Create Parser
parser = Parser()
parseTree = parser.parser.parse(source_code, lexer=lexer)
for i in parseTree:
    print(i)

#Create Visitor for code generation
#try:
symtab = SymbolTable()
visitor = Visitor(symbol_table=symtab, parse_tree=parseTree)
newCode = visitor.start()
output_path = input_path.replace("py", "cpp")
file = open(output_path, "w")
file.write(newCode)
#except Exception as e:
 #   print(e)
