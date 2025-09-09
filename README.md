# python-c-compiler

# Students: Felipe Bianchini, C21178. André Salas, C27058

The current version of the project consists of a lexer that takes in a simplified form of Python called Fangless Python and outputs a series of tokens and errors.

## User Guide

To run the lexer you need a text file, it should be written in Fangless Python, but the lexer is able to analyze any text and return the errors found. The tests folder contains examples of code for analyzing.

To choose a text file to analyze, you need to edit tester.py, changing the file path in line 5 of the file. After choosing a file to check, run the lexer using the following command:

    python tester.py

The terminal will show the tokens found, showing: Type, value and line. After the tokens are shown the errors will follow, it will also print their value and line and column alongside the actual line it happens.

## Components

### Lexer

The Lexer is in the file src/lexer.py. It contains a Regex description for the tokens that can be found in the text, these tokens are saved in the "tokens" array. The Regex for each token is declared as t_<TokenName\>. 

The lexer also contains the methods handle_dedentation, which checks for dedentation on lines that do not start on a whitespace, checking against the last line and creating as many DENT tokens as needed. On the case of lines that start in whitespace, the method handle_indentation can create both INDENT and DENT values as needed.

Since PLY doesnt allow t_<TokenName\> methods to return more than one token, a stack was created that allows for the indentation-handling methods to input many tokens in a single method. The "token" method takes into account this stack and return from it when asked for a token unless it is empty.
