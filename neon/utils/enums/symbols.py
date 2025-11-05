from enum import Enum

class Symbol(Enum):
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    EQUALS = "="
    LESS_THAN = "<"
    GREATER_THAN = ">"
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    COMMA = ","
    SEMICOLON = ";"

    @classmethod
    def all_symbols(cls):
        return [symbol.value for symbol in cls]