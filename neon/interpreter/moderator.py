from typing import Any
from utils.models.pnode import PNode
from utils.enums.node_type import NodeType
from utils.enums.token_type import TokenType

class Moderator:

    @staticmethod
    def get_atomic_value(node: PNode) -> Any:
        """
        Retrieves the value of an atomic expression node.
        Assumes the node is of type ATOM.

        Args:
            node (PNode): The parse tree node representing an atomic expression.

        Returns:
            str: The lexeme of the atomic expression.
        """
        if node.node_type != NodeType.ATOM:
            raise ValueError("Node is not of type ATOM.")
        
        token = node.token
        if token.token_type == TokenType.IDENTIFIER:
            return token.lexeme  # Variable name

        ATOMIC_CASTS = {
            TokenType.INT: int,
            TokenType.FLOAT: float,
            TokenType.STRING: str
        }

        if token.token_type in ATOMIC_CASTS:
            return ATOMIC_CASTS[token.token_type](token.lexeme)

        raise ValueError(f"Unknown token type: {token.token_type}")

    @staticmethod
    def is_operation_compatible(op_node: PNode, left_node: PNode, right_node: PNode) -> bool:
        """
        Checks if the operation represented by op_node is compatible with the types of left_node and right_node.

        Args:
            op_node (PNode): The parse tree node representing the operation.
            left_node (PNode): The left operand node.
            right_node (PNode): The right operand node.

        Returns:
            bool: True if the operation is compatible, False otherwise.
        """
        if op_node.node_type != NodeType.BINARY_OPERATION:
            raise ValueError("Node is not of type BINARY_OPERATION.")

        left_type = left_node.token.token_type
        right_type = right_node.token.token_type

        if left_type == right_type:
            return True

        # Check for implicit type conversion
        if (left_type == TokenType.INT and right_type == TokenType.FLOAT) or \
           (left_type == TokenType.FLOAT and right_type == TokenType.INT):
            return True

        return False