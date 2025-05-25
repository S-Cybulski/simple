from expressions import Literal, Unary, Binary, Grouping

class Interpreter:
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

        else:
            raise RuntimeError(f"Unknown expression type {type(expr)}")
