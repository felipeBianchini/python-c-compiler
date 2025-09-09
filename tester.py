from src.lexer import Lexer
from src.utils import Error

# Read file
with open("tests/test_oficial.py", "r", encoding='utf-8') as f:
    source_code = f.read()

# Create lexer
errors = [] # An empty error queue is created and sent to the lexer
lexer = Lexer(errors=errors)
lexer.build()
lexer.input(source_code)

# Check tokens
while True:
    token = lexer.token()
    if not token:
        break # End while when the lexer returns a null
    val = str(token.value)
    val = val.replace("\n", " \\n ") # \n replaced for reading purposes
    print(f"{token.type}: {val} (line {token.lineno})")

# Check for errors
if errors:
    print("Lexical errors found:")
    for error in errors:
        print(error)