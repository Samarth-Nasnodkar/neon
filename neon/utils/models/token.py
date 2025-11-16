from utils.enums.token_type import TokenType

class Token:
    token_type: TokenType
    lexeme: str
    line: int
    column: int

    def __repr__(self) -> str:
        token_type = self.token_type.value if self.token_type else "None"
        return f"Token({token_type}, {self.lexeme}, {self.line}, {self.column})"
    
    @staticmethod
    def make(data: dict) -> "Token":
        token = Token()
        token.token_type = TokenType(data.get("token_type", ""))
        token.lexeme = data.get("lexeme", "")
        token.line = data.get("line", 0)
        token.column = data.get("column", 0)
        return token
    
    @staticmethod
    def empty() -> "Token":
        return Token.make({"token_type": "EOF", "lexeme": "", "line": -1, "column": -1})