class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        # Tokenization logic goes here
        pass
    
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