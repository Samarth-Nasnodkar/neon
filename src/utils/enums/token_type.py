from enum import Enum

class TokenType(Enum):
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"
    SYMBOL = "SYMBOL"
    EOL = "EOL"
    EOF = "EOF"