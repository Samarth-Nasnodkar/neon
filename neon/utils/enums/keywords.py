from enum import Enum
from typing import Optional
from utils.cache.method import cached

class Keyword(Enum):
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    FOR = "for"
    RETURN = "return"
    FUNCTION = "fn"
    CONST = "const"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    INT = "int"
    FLOAT = "float"
    STRING = "str"
    BOOL = "bool"

    @classmethod
    @cached
    def get_keyword(cls, value: str) -> Optional[Enum]:
        return cls._value2member_map_.get(value, None)

    @classmethod
    @cached
    def is_keyword(cls, value: str) -> bool:
        return cls.get_keyword(value) is not None