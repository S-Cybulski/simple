from expressions import *

class Interpreter:
    """
    Executes the parsed statements by evaluating expressions and managing the environment for variable storage and retrieval.
    """
    def __init__(self):
        self.environment = Environment()
    
    # Interpret a list of statements, executing each one in sequence.
    def interpret(self, statements):
        for statement in statements:
            self.execute(statement)
    
    # Execute a single statement, handling different types of statements like Print, Assign, While, If, etc.
    def execute(self, statement):
        if isinstance(statement, Print):
            value = self.evaluate(statement.expression)
            print(value)

        elif isinstance(statement, Assign):
            value = self.evaluate(statement.value)
            self.environment.assign(statement.name.lexeme, value)
            return value

        elif isinstance(statement, While):
            while self.evaluate(statement.condition):
                for stmt in statement.body:
                    self.execute(stmt)
        
        elif isinstance(statement, If):
            if self.evaluate(statement.condition):
                for stmt in statement.then_branch:
                    self.execute(stmt)
            elif statement.else_branch:
                for stmt in statement.else_branch:
                    self.execute(stmt)
        
        else:
            self.evaluate(statement)
    
    # Evaluate an expression, handling different types of expressions like Literal, Unary, Binary, Grouping, Variable, Assign, and Input.
    def evaluate(self, expr):
        if isinstance(expr, Literal):
            return expr.value

        elif isinstance(expr, Grouping):
            return self.evaluate(expr.expression)

        elif isinstance(expr, Unary):
            right = self.evaluate(expr.right)
            operator = expr.operator.lexeme

            if operator == '-':
                return -right
            elif operator == '!':
                return not right
            raise RuntimeError(f"Unknown unary operator {operator}")

        elif isinstance(expr, Binary):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            operator = expr.operator.lexeme

            if operator == '+':
                return left + right
            elif operator == '-':
                return left - right
            elif operator == '*':
                return left * right
            elif operator == '/':
                if right == 0:
                    raise RuntimeError("Division by zero.")
                return left / right
            elif operator == '<':
                return left < right
            elif operator == '<=':
                return left <= right
            elif operator == '>':
                return left > right
            elif operator == '>=':
                return left >= right
            elif operator == '==':
                return left == right
            elif operator == '!=':
                return left != right
            elif operator == 'AND':
                return bool(left) and bool(right)
            elif operator == 'OR':
                return bool(left) or bool(right)
            else:
                raise RuntimeError(f"Unknown binary operator {operator}")
        elif isinstance(expr, Variable):
            return self.environment.get(expr.name.lexeme)

        elif isinstance(expr, Assign):
            value = self.evaluate(expr.value)
            self.environment.assign(expr.name.lexeme, value)
            return value
        
        elif isinstance(expr, Input):
            return self.evaluate_input(expr)
        else:
            raise RuntimeError(f"Unknown expression type {type(expr)}")
    
    def evaluate_input(self, expr):
        prompt = self.evaluate(expr.prompt)
        return input(str(prompt))

class Environment:
    """
    Manages variable storage and retrieval, allowing for variable assignment and lookup.
    """
    def __init__(self):
        self.values = {}

    def get(self, name):
        if name in self.values:
            return self.values[name]
        raise RuntimeError(f"Undefined variable '{name}'.")

    def assign(self, name, value):
        self.values[name] = value