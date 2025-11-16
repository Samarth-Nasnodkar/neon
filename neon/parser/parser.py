from typing import Optional
from lexer.lexer import Lexer
from visualize.visualizer import Visualizer
from utils.models.token import Token
from utils.models.pnode import PNode
from utils.enums.token_type import TokenType
from utils.enums.node_type import NodeType


class Parser:

    HIGHEST_PRECEDENCE = 'pl2'

    def __init__(self, source: str) -> None:
        self.tokens = Lexer(source).tokenize()
        self.current = 0
    
    @property
    def peek(self) -> Token:
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return Token.make({"token_type": "EOF", "lexeme": "", "line": -1, "column": -1})

    @property
    def token(self) -> Token:
        token = self.peek
        self.advance()
        return token
    
    def visualize(self) -> None:
        root = self.parse()
        if root is None:
            raise SyntaxError("Failed to parse the source code.")
        
        visualizer = Visualizer(root)
        visualizer.draw()

    def advance(self) -> None:
        self.current += 1

    def parse(self) -> Optional[PNode]:
        parse_method = getattr(self, f"parse_{self.HIGHEST_PRECEDENCE}")
        kwargs = {"depth": 0}

        return parse_method(**kwargs)
    
    def parse_atom(self, depth: int) -> PNode:
        """
        Attempts to parse an atomic expression.
        An atomic expression can be:
        1. IDENTIFIER
        2. INT
        3. FLOAT
        4. STRING

        Grammar:
        ATOM ::= IDENTIFIER
               | INT
               | FLOAT
               | STRING
               | SYMBOL('(') PL2 SYMBOL(')')
        """
        token = self.peek
        if token.token_type in [TokenType.IDENTIFIER, TokenType.INT, TokenType.FLOAT, TokenType.STRING]:
            self.token
            return PNode(
                node_type=NodeType.ATOM,
                token=token,
                depth=depth
            )
        elif token.token_type == TokenType.SYMBOL and token.lexeme == '(':
            self.token  # consume '('
            expr_node = self.parse_pl2(depth + 1)
            closing_token = self.peek
            if closing_token.token_type == TokenType.SYMBOL and closing_token.lexeme == ')':
                self.token  # consume ')'
                return expr_node
            else:
                raise SyntaxError(f"Expected ')' at line {closing_token.line}, column {closing_token.column}.")
        
        raise SyntaxError(f"Unexpected token {token.lexeme} at line {token.line}, column {token.column}. Expected an atomic expression.")
    
    def parse_pl1(self, depth: int) -> PNode:
        """
        Attempts to parse Precedence Level 1 expressions.
        PL1 expressions can be:
        1. Atomic expressions
        2. Multiplicative expressions
        3. Divisive expressions
        4. Modulus expressions

        Grammar:
        PL1 ::= ATOM
               | PL1 SYMBOL('*') PL1
               | PL1 SYMBOL('/') PL1
               | PL1 SYMBOL('%') PL1
        """
        def pl1_sub(depth: int) -> PNode:
            """
            Helper function to parse without left recursion.
            Grammar (without left recursion):
            PL1 ::= ATOM PL1'
            PL1' ::= SYMBOL('*') ATOM PL1'
                    | SYMBOL('/') ATOM PL1'
                    | SYMBOL('%') ATOM PL1'
                    | ε
            
            This helper function parses the PL1' rule.
            """
            left = self.parse_atom(depth + 1)

            token = self.peek
            if token.token_type == TokenType.SYMBOL and token.lexeme in ['*', '/', '%']:
                self.token  # consume operator
                right = pl1_sub(depth + 1)
                operator_node = PNode(
                    node_type=NodeType.BINARY_OPERATION,
                    token=token,
                    depth=depth, 
                    children=[left, right]
                )
                return operator_node
            else:
                return left
        
        return pl1_sub(depth)
        
    def parse_pl2(self, depth: int) -> PNode:
        """
        Attempts to parse Precedence Level 2 expressions.
        PL2 expressions can be:
        1. PL1 expressions
        2. Additive expressions
        3. Subtractive expressions

        Grammar:
        PL2 ::= PL1
               | PL1 SYMBOL('+') PL1
               | PL1 SYMBOL('-') PL1
        """
        def pl2_sub(depth: int) -> PNode:
            """
            Helper function to parse without left recursion.
            Grammar (without left recursion):
            PL2 ::= PL1 PL2'
            PL2' ::= SYMBOL('+') PL1 PL2'
                    | SYMBOL('-') PL1 PL2'
                    | ε
            
            This helper function parses the PL2' rule.
            """
            left = self.parse_pl1(depth + 1)

            token = self.peek
            if token.token_type == TokenType.SYMBOL and token.lexeme in ['+', '-']:
                self.token  # consume operator
                right = pl2_sub(depth + 1)
                operator_node = PNode(
                    node_type=NodeType.BINARY_OPERATION,
                    token=token,
                    depth=depth,
                    children=[left, right]
                )
                return operator_node
            else:
                return left
            
        return pl2_sub(depth)