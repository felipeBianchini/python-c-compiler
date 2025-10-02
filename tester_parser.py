from re import DEBUG
from src.lexer import Lexer
from src.parser import Parser
from src.utils import Error

# Read file
with open("tests/test1.py", "r", encoding='utf-8') as f:
    source_code = f.read()

# Create Lexer
errors = [] # An empty error queue is created and sent to the lexer
lexer = Lexer(errors=errors)
lexer.build()
lexer.input(source_code)

# Create Parser
parser = Parser()
result = parser.parser.parse(source_code, lexer=lexer)
print(result)