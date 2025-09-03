from src.lexer import Lexer
from src.utils import Error

# Read file
with open("tests/test2.py", "r", encoding='utf-8') as f:
    source_code = f.read()

# Create lexer
errors = []
lexer = Lexer(errors=errors)
lexer.build()
lexer.input(source_code)

# Test tokenization
while True:
    token = lexer.token()
    if not token:
        break
    val = str(token.value)
    val = val.replace("\n", " \\n ")
    print(f"{token.type}: {val} (line {token.lineno})")

# Check for errors
if errors:
    print("Lexical errors found:")
    for error in errors:
        print(error)