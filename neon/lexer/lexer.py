from typing import Optional
from utils.models.token import Token
from utils.enums.keywords import Keyword
from utils.enums.token_type import TokenType
from utils.enums.symbols import Symbol

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens = []
        while self.position < len(self.source):
            current_char = self.char
            
            if current_char.isspace():
                self.get  # Consume whitespace
                continue
            
            token, err = self._tokenize_next()
            if err:
                raise Exception(f"Lexing error at line {self.line}, column {self.column}: {err}")
            tokens.append(token)

        return tokens
    
    @property
    def char(self) -> str:
        if self.position < len(self.source):
            return self.source[self.position]
        return ''
    
    @property
    def get(self) -> str:
        if self.position < len(self.source):
            current_char = self.source[self.position]
            self.position += 1
            
            if current_char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            
            return current_char
        return ''
    
    def _tokenize_next(self) -> tuple[Optional[Token], Optional[str]]:
        current_char = self.get
        
        # Example tokenization logic (to be expanded)
        if current_char.isalpha():
            lexeme = current_char
            while self.char.isalnum():
                lexeme += self.get
            token = Token()
            keyword = Keyword.get_keyword(lexeme)
            token.token_type = TokenType.IDENTIFIER if keyword is None else TokenType.KEYWORD
            token.lexeme = lexeme
            token.line = self.line
            token.column = self.column - len(lexeme)
            return token, None
        elif current_char.isdigit():
            lexeme = current_char
            dot_found = False
            while self.char.isdigit() or (not dot_found and self.char == '.'):
                if self.char == '.':
                    if dot_found:
                        return None, "Invalid number format"
                    dot_found = True
                lexeme += self.get
            token = Token()
            token.token_type = TokenType.INT if not dot_found else TokenType.FLOAT
            token.lexeme = lexeme
            token.line = self.line
            token.column = self.column - len(lexeme)
            return token, None
        elif current_char == '"' or current_char == "'":
            quote_type = current_char
            lexeme = ''
            while self.char != quote_type and self.char != '':
                lexeme += self.get
            if self.char == '':
                return None, "Unterminated string literal"
            self.get  # Consume closing quote
            token = Token()
            token.token_type = TokenType.STRING
            token.lexeme = lexeme
            token.line = self.line
            token.column = self.column - len(lexeme) - 2  # -2 for quotes
            return token, None
        elif current_char in Symbol.all_symbols():
            token = Token()
            token.token_type = TokenType.SYMBOL
            token.lexeme = current_char
            token.line = self.line
            token.column = self.column - 1
            return token, None
        elif current_char == '\n':
            token = Token()
            token.token_type = TokenType.EOL
            token.lexeme = '\\n'
            token.line = self.line - 1
            token.column = self.column - 1
            return token, None
        elif current_char == '':
            token = Token()
            token.token_type = TokenType.EOF
            token.lexeme = ''
            token.line = self.line
            token.column = self.column
            return token, None
        
        # Handle other token types...
        
        return None, f"Unrecognized character: {current_char}"