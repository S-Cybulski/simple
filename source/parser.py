from expressions import *
from tokens import Token, TokenType

class ParseError(Exception):
    pass

class Parser:
    """
    A simple parser that converts a list of tokens into an Abstract Syntax Tree (AST).
    It supports parsing expressions, statements, and control flow structures like if-else and while loops.
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
    # Parses the entire input and returns a list of statements.
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
    
    # Parses a single statement, which can be a print statement, while loop, if statement, or an expression.
    def statement(self):
        if self.match(TokenType.PRINT):
            expr = self.expression()
            return Print(expr)
        elif self.match(TokenType.WHILE):
            return self.while_statement()
        elif self.match(TokenType.IF):
            return self.if_statement()
        return self.expression()

    # Parses a print statement, which outputs the value of an expression.
    def print_statement(self):
        value = self.expression()
        return Print(value)
    
    # Parses a while statement, which executes a block of code as long as a condition is true.
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

    # Parses an if statement, which executes a block of code if a condition is true, and optionally another block if the condition is false.
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
    
    # Parses an expression statement, which is an expression followed by a newline.
    def expression_statement(self):
        expr = self.expression()
        return expr
    
    def expression(self):
        return self.assignment()
    
    # Parses an assignment expression, which can assign a value to a variable.
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

    # Parses an expression with addition and multiplication operations.
    def addition(self):
        expr = self.multiplication()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.multiplication()
            expr = Binary(expr, operator, right)
        return expr
    
    # Parses an expression with multiplication and division operations.
    def multiplication(self):
        expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr
    
    # Parses unary expressions, which can be negation or logical NOT.
    def unary(self):
        if self.match(TokenType.MINUS, TokenType.BANG):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    # Parses primary expressions, which can be literals, variables, groupings, or input statements.
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
    
    # Matches the current token against the provided types and advances if it matches.
    def match(self, *types):
        if self.check(*types):
            self.advance()
            return True
        return False
    
    # Consumes the current token if it matches the expected type, otherwise raises a ParseError with a message.
    def consume(self, expected, message):
        if self.check(expected):
            return self.advance()
        raise ParseError(message)

    # Checks if the current token matches any of the provided types.
    def check(self, *types):
        if self.is_at_end():
            return False
        return self.peek().type in types
    
    # Checks if the parser has reached the end of the input.
    def is_at_end(self):
        return self.current >= len(self.tokens)
    
    # Returns the current token without advancing.
    def peek(self):
        if self.is_at_end():
            return None
        return self.tokens[self.current]
    
    # Advances to the next token and returns the previous token.
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    # Returns the previous token, which is the token before the current one.
    def previous(self):
        return self.tokens[self.current - 1]
    
    # Parses logical expressions with OR and AND operations.
    def logic_or(self):
        expr = self.logic_and()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.logic_and()
            expr = Binary(expr, operator, right)
        return expr
    
    # Parses logical expressions with AND operations.
    def logic_and(self):
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Binary(expr, operator, right)
        return expr

    # Parses equality expressions with == and != operators.
    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    # Parses comparison expressions with >, >=, <, and <= operators.
    def comparison(self):
        expr = self.addition()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.addition()
            expr = Binary(expr, operator, right)
        return expr