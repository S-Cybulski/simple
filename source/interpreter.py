from expressions import Literal, Unary, Binary, Grouping, Variable, Assign, Print

class Interpreter:
    def __init__(self):
        self.environment = Environment()
        
    def interpret(self, statements):
        for statement in statements:
            self.execute(statement)
    
    def execute(self, statement):
        if isinstance(statement, Print):
            value = self.evaluate(statement.expression)
            print(value)

        elif isinstance(statement, Assign):
            value = self.evaluate(statement.value)
            self.environment.assign(statement.name.lexeme, value)
            return value
        
        else:
            self.evaluate(statement)
        
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
        else:
            raise RuntimeError(f"Unknown expression type {type(expr)}")

class Environment:
    def __init__(self):
        self.values = {}

    def get(self, name):
        if name in self.values:
            return self.values[name]
        raise RuntimeError(f"Undefined variable '{name}'.")

    def assign(self, name, value):
        self.values[name] = value