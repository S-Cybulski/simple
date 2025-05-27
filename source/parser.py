from expressions import *
from tokens import Token, TokenType

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
    def parse(self):
        statements = []
        while not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            statements.append(self.statement())
            if self.match(TokenType.NEWLINE):
                continue
            if self.check(TokenType.EOF):
                break
        return statements
    
    def statement(self):
        if self.match(TokenType.PRINT):
            expr = self.expression()
            return Print(expr)
        elif self.match(TokenType.WHILE):
            return self.while_statement()
        elif self.match(TokenType.IF):
            return self.if_statement()
        return self.expression()
    
    def print_statement(self):
        value = self.expression()
        return Print(value)
    
    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before while body.")
        
        body = []
        
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            body.append(self.statement())
        
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after while body.")
        
        return While(condition, body)

    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before if body.")
        
        then_branch = []
        
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            then_branch.append(self.statement())
        
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after if body.")
        
        else_branch = None
        if self.match(TokenType.ELSE):
            self.consume(TokenType.LEFT_BRACE, "Expect '{' before else body.")
            else_branch = []
            while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
                else_branch.append(self.statement())
            self.consume(TokenType.RIGHT_BRACE, "Expect '}' after else body.")
        
        return If(condition, then_branch, else_branch)
    
    def expression_statement(self):
        expr = self.expression()
        return expr
    
    def expression(self):
        return self.assignment()
    
    def assignment(self):
        expr = self.logic_or()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            raise ParseError("Invalid assignment target.")

        return expr

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
        if self.match(TokenType.MINUS, TokenType.BANG):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.INTEGER, TokenType.FLOAT):
            return Literal(self.previous().literal)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        if self.match(TokenType.INPUT):
            self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'INPUT'")
            prompt = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after input prompt.")
            return Input(prompt)
        
        raise ParseError("Expect expression.")
    
    def match(self, *types):
        if self.check(*types):
            self.advance()
            return True
        return False

    def consume(self, expected, message):
        if self.check(expected):
            return self.advance()
        raise ParseError(message)

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
    
    def logic_or(self):
        expr = self.logic_and()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.logic_and()
            expr = Binary(expr, operator, right)
        return expr
    
    def logic_and(self):
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Binary(expr, operator, right)
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.addition()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.addition()
            expr = Binary(expr, operator, right)
        return expr