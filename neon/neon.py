from lexer.lexer import Lexer

def main():
    source_code = """
    if x > 10.0 {
        print("x is greater than 10")
    } else {
        print("x is 10 or less")
    }
    """
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    for token in tokens:
        print(f"Token Type: {token.token_type}, Lexeme: '{token.lexeme}', Line: {token.line}, Column: {token.column}")

if __name__ == "__main__":
    main()