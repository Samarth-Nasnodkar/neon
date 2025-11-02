from utils.enums.token_type import TokenType

class Token:
    token_type: TokenType
    lexeme: str
    line: int
    column: int

    def __repr__(self) -> str:
        token_type = self.token_type.value if self.token_type else "None"
        return f"Token({token_type}, {self.lexeme}, {self.line}, {self.column})"