from expressions import Literal, Unary, Binary, Grouping
from tokens import Token, TokenType

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
    def parse(self):
        return self.expression()
    
    def expression(self):
        return self.addition()

    def addition(self):
        expr = self.multiplication()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.multiplication()
            expr = Binary(expr, operator, right)
        return expr
    
    def multiplication(self):
        expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr
    
    def unary(self):
        if self.match(TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.INTEGER, TokenType.FLOAT):
            return Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        raise ParseError("Expect expression.")
    
    def match(self, *types):
        if self.check(*types):
            self.advance()
            return True
        return False

    def consume(self, expected):
        if self.check(expected):
            return self.advance()
        raise ParseError(f"Expected token '{expected}' but found '{self.peek().type}'.")

    def check(self, *types):
        if self.is_at_end():
            return False
        return self.peek().type in types
    
    def is_at_end(self):
        return self.current >= len(self.tokens)
    
    def peek(self):
        if self.is_at_end():
            return None
        return self.tokens[self.current]
    
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def previous(self):
        return self.tokens[self.current - 1]