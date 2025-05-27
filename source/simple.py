import sys
from pathlib import Path
from scanner import Scanner
from tokens import TokenType, Token
from parser import Parser
from interpreter import Interpreter

class Simple:
    
    had_error = False

    # rins the Simple interpreter with the provided source code.    
    def run(source: str):
        try:
            scanner = Scanner(source)
            tokens = scanner.scan_tokens()
            
            parser = Parser(tokens)
            statements = parser.parse()
            
            interpreter = Interpreter()
            interpreter.interpret(statements)
            
        except SyntaxError as e:
            print(f"Syntax error: {e}")
            Simple.had_error = True
        except RuntimeError as e:
            print(f"Runtime error: {e}")
            Simple.had_error = True
    
    # Runs a Simple script from a file. If an error occurs, it exits with code 65.
    def run_file(filename: str):
        path = Path(filename).absolute()
        source = path.read_text()
        Simple.run(source)
        if Simple.had_error:
            sys.exit(65)

    # A simple Read-Eval-Print Loop (REPL) for the Simple interpreter.   
    def repl():
        print("Simple REPL. type 'exit' to quit.")
        while True:
            try:
                line = input("> ")
                if line.lower() == "exit":
                    break
                Simple.run(line)
            except EOFError:
                print("\nExiting REPL.")
                break
            except KeyboardInterrupt:
                print("\nExiting REPL.")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        Simple.run_file(sys.argv[1])
    else:
        Simple.repl()