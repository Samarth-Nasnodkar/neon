from typing import Optional
from utils.models.token import Token
from utils.enums.node_type import NodeType


class PNode:
    id: str
    token: Token
    node_type: NodeType
    depth: int
    children: list['PNode']

    def __init__(self, token: Token = Token.empty(), node_type: NodeType = NodeType.ATOM, depth: int = 0, children: Optional[list['PNode']] = None):
        self.token = token
        self.node_type = node_type
        self.depth = depth
        self.id = f"{self.token.lexeme}_{id(self)}"
        if not children:
            children = []
        
        for child in children:
            child.depth = self.depth + 1

        self.children = children

    def add_child(self, child: 'PNode') -> None:
        child.depth = self.depth + 1
        self.children.append(child)
    
    def __repr__(self) -> str:
        prefix = ' ' * (self.depth * 2)
        return f'{prefix}PNode(token={self.token}, depth={self.depth}) children:\n{self.children}'