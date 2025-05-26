from tokens import Token, TokenType

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
    
    def is_at_end(self):
        return self.current >= len(self.source)
    
    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def add_token(self, typ, literal=None):
        text = self.source[self.start:self.current]
        token = Token(typ, text, literal, self.line)
        self.tokens.append(token)

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
    
    def match(self, expected: str):
        if self.is_at_end() or self.peek() != expected:
            return False

        self.advance()
        return True
    
    def identifier(self):
        
        keywords = {
            "TRUE": (TokenType.TRUE, True),
            "FALSE": (TokenType.FALSE, False),
            "AND": (TokenType.AND, None),
            "OR": (TokenType.OR, None),
            "PRINT": (TokenType.PRINT, None),
            "WHILE": (TokenType.WHILE, None)
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
        
    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens