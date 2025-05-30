""" This file defines AST (Abstract Syntax Tree) classes for various expressions in a programming language. """

class Literal:
    def __init__(self, value):
        self.value = value

class Unary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

class Binary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Grouping:
    def __init__(self, expression):
        self.expression = expression

class Input:
    def __init__(self, prompt):
        self.prompt = prompt

class If:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class Print:
    def __init__(self, expression):
        self.expression = expression
        
class Variable:
    def __init__(self, name):
        self.name = name

class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body