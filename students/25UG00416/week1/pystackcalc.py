import re
import sys


class Stack:
    """A stack follows Last In, First Out (LIFO)."""

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return self.items.copy()


def tokenize(expr: str) -> list[str]:
    """Split an expression into numbers, names and operators."""
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    tokens = re.findall(pattern, expr)

    # Reject characters that the tokenizer does not recognize.
    if not tokens or "".join(tokens) != re.sub(r"\s+", "", expr):
        raise ValueError("Empty expression or invalid tokens")

    return tokens
