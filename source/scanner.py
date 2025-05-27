from tokens import Token, TokenType

class Scanner:
    """
    A simple scanner that tokenizes a source code string.
    It recognizes various token types such as operators, literals, identifiers, and control flow keywords.
    """
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
    
    # Checks if the scanner has reached the end of the source code.
    def is_at_end(self):
        return self.current >= len(self.source)
    
    # Advances the current position in the source code and returns the character at that position.
    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char

    # Returns the previous character in the source code without advancing.
    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    # Returns the character after the current position without advancing.
    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    # Adds a token to the list of tokens with the specified type and optional literal value.
    def add_token(self, typ, literal=None):
        text = self.source[self.start:self.current]
        token = Token(typ, text, literal, self.line)
        self.tokens.append(token)

    # Scans the next character in the source code and determines its token type.
    def scan_token(self):
        char =self.advance()
        if char in ' \r\t':
            return
        elif char == '\n':
            self.line += 1
        elif char == '+':
            self.add_token(TokenType.PLUS)
        elif char == '-':
            self.add_token(TokenType.MINUS)
        elif char == '*':
            self.add_token(TokenType.STAR)
        elif char == '/':
            self.add_token(TokenType.SLASH)
        elif char == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif char == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif char == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif char == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif char == '"':
            self.string()
        elif char.isdigit():
            self.number()
        elif char == '=':
            if self.match('='):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif char == '!':
            if self.match('='):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif char == '<':
            if self.match('='):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif char == '>':
            if self.match('='):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif char.isalpha():
            self.identifier()
        else:
            raise SyntaxError(f'Unexpected character: {char} at line {self.line}')
    
    # Parses a number from the source code, which can be an integer or a float.
    def number(self):
        while self.peek().isdigit():
            self.advance()

        is_float = False
        
        if self.peek() == '.' and self.peek_next().isdigit():
            is_float = True
            self.advance()
            while self.peek().isdigit():
                self.advance()
        
        text = self.source[self.start:self.current]
        value = float(text) if is_float else int(text)
        token_type = TokenType.FLOAT if is_float else TokenType.INTEGER
        self.add_token(token_type, value)
    
    # Parses a string literal from the source code, which is enclosed in double quotes.
    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            raise SyntaxError(f"Unterminated string at line {self.line}")

        self.advance()
        
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)
    
    # Matches the next character in the source code with the expected character.
    def match(self, expected: str):
        if self.is_at_end() or self.peek() != expected:
            return False

        self.advance()
        return True
    
    # Parses identifiers and keywords from the source code.
    def identifier(self):
        
        keywords = {
            "TRUE": (TokenType.TRUE, True),
            "FALSE": (TokenType.FALSE, False),
            "AND": (TokenType.AND, None),
            "OR": (TokenType.OR, None),
            "PRINT": (TokenType.PRINT, None),
            "WHILE": (TokenType.WHILE, None),
            "IF": (TokenType.IF, None),
            "ELSE": (TokenType.ELSE, None),
            "INPUT": (TokenType.INPUT, None)
        }
        
        while self.peek().isalnum():
            self.advance()

        text = self.source[self.start:self.current]
        result = keywords.get(text)
        

        if result:
            type_, literal = result
            self.add_token(type_, literal)
        else:
            self.add_token(TokenType.IDENTIFIER, text)
    
    # Scans the entire source code and returns a list of tokens.
    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens