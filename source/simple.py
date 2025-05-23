import sys
from pathlib import Path
from scanner import Scanner
from tokens import TokenType, Token

class Simple:
    had_error = False
    
    def run(source: str):
        try:
            scanner = Scanner(source)
            tokens = scanner.scan_tokens()
            for token in tokens:
                print(token)
        except SyntaxError as e:
            print(f"Syntax error: {e}")
            had_error = True
    
    def run_file(filename: str):
        path = Path(filename).absolute()
        source = path.read_text()
        Simple.run(source)
        if Simple.had_error:
            sys.exit(65)
            
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