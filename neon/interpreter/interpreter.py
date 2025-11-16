from interpreter.moderator import Moderator
from utils.models.pnode import PNode
from utils.enums.node_type import NodeType


class Interpreter:
    def __init__(self, root: PNode) -> None:
        self.root = root

    def interpret(self):
        return self._evaluate(self.root)

    def _evaluate(self, node: PNode):
        if node is None:
            return None

        if node.node_type == NodeType.ATOM:
            return Moderator.get_atomic_value(node)

        if node.node_type == NodeType.BINARY_OPERATION:
            left = self._evaluate(node.children[0])
            right = self._evaluate(node.children[1])
            return self._apply_operator(left, right, node.token.lexeme)

        raise ValueError(f"Unknown node type: {node.node_type}")

    def _apply_operator(self, left, right, operator):
        # if not Moderator.is_operation_compatible(operator, left, right):
        #     raise TypeError(f"Incompatible types for operator {operator}: {type(left)} and {type(right)}")
        
        if operator == '+':
            return left + right
        if operator == '-':
            return left - right
        if operator == '*':
            return left * right
        if operator == '/':
            return left / right
        if operator == '%':
            return left % right
        
        raise ValueError(f"Unknown operator: {operator}")