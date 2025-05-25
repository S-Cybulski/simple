from enum import Enum
from typing import Any

class TokenType(Enum):
    # literal types
    NUMBER = 'NUMBER'
    INTEGER = 'INT'
    FLOAT = 'FLOAT'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    
    # single-character tokens operators
    PLUS = '+'
    MINUS = '-'
    STAR = '*'
    SLASH = '/'
    BANG = '!'
    EQUAL = '='
    GREATER = '>'
    LESS = '<'
    
    #two-character tokens operators
    BANG_EQUAL = '!='
    EQUAL_EQUAL = '=='
    GREATER_EQUAL = '>='
    LESS_EQUAL = '<='
    
    #logical tokens operators
    AND = 'AND'
    OR = 'OR'

    #single-character tokens grouping
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'

    #special tokens
    EOF = ''

class Token:
    def __init__(
            self,
            typ: TokenType,
            lexeme: str,
            literal: Any = None,
            line: int = 0
    ) -> None:
        self.type = typ
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type.name} '{self.lexeme}' ({self.literal}) on line {self.line}"
