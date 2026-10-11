import re


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
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
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    tokens = re.findall(pattern, expr)

    if not tokens:
        raise ValueError("Empty expression or invalid tokens")

    return tokens


PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3
}

RIGHT_ASSOCIATIVE = {"^"}


def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


def is_variable(token):
    return re.fullmatch(r"[a-zA-Z_]\w*", token) is not None


def infix_to_postfix(tokens):
    output = []
    stack = []

    for token in tokens:
        if is_number(token) or is_variable(token):
            output.append(token)

        elif token in PRECEDENCE:
            while stack and stack[-1] in PRECEDENCE and (
                PRECEDENCE[stack[-1]] > PRECEDENCE[token]
                or (
                    PRECEDENCE[stack[-1]] == PRECEDENCE[token]
                    and token not in RIGHT_ASSOCIATIVE
                )
            ):
                output.append(stack.pop())

            stack.append(token)

        elif token == "(":
            stack.append(token)

        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())

            if not stack:
                raise ValueError("Mismatched parentheses")

            stack.pop()

        else:
            raise ValueError("Invalid token")

    while stack:
        if stack[-1] == "(":
            raise ValueError("Mismatched parentheses")

        output.append(stack.pop())

    return output


def eval_postfix(postfix, variables=None):
    if variables is None:
        variables = {}

    stack = Stack()

    for token in postfix:
        if is_number(token):
            if "." in token:
                stack.push(float(token))
            else:
                stack.push(int(token))

        elif is_variable(token):
            if token not in variables:
                raise ValueError(f"Unknown variable: {token}")

            stack.push(variables[token])

        elif token in PRECEDENCE:
            if stack.size() < 2:
                raise ValueError("Invalid expression")

            b = stack.pop()
            a = stack.pop()

            if token == "+":
                result = a + b

            elif token == "-":
                result = a - b

            elif token == "*":
                result = a * b

            elif token == "/":
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                result = a / b

            elif token == "%":
                if b == 0:
                    raise ZeroDivisionError("Modulo by zero")
                result = a % b

            elif token == "^":
                result = a ** b

            stack.push(result)

    if stack.size() != 1:
        raise ValueError("Invalid expression")

    return stack.pop()


class PyStackCalc:
    def __init__(self):
        self.variables = {
            "pi": 3.14159,
            "e": 2.71828
        }

        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def evaluate(self, expression):
        tokens = tokenize(expression)
        postfix = infix_to_postfix(tokens)
        return eval_postfix(postfix, self.variables)

    def execute(self, command):
        command = command.strip()

        if not command:
            raise ValueError("Empty command")

        if command.lower() == "undo":
            if self.undo_stack.is_empty():
                return None

            self.redo_stack.push(dict(self.variables))
            self.variables = self.undo_stack.pop()
            return None

        if command.lower() == "redo":
            if self.redo_stack.is_empty():
                return None

            self.undo_stack.push(dict(self.variables))
            self.variables = self.redo_stack.pop()
            return None

        if command.startswith("let "):
            command = command[4:].strip()

        if "=" in command:
            name, expression = command.split("=", 1)

            name = name.strip()
            expression = expression.strip()

            if not is_variable(name):
                raise ValueError("Invalid variable name")

            value = self.evaluate(expression)

            self.undo_stack.push(dict(self.variables))
            self.redo_stack = Stack()

            self.variables[name] = value

            return value

        return self.evaluate(command)

    def start_repl(self):
        while True:
            try:
                command = input("calc> ").strip()

                if command.lower() in ("exit", "quit"):
                    break

                result = self.execute(command)

                if result is not None:
                    print(result)

            except Exception as error:
                print("Error:", error)


def run_tests():
    print("Running PyStackCalc Test Suite...")

    engine = PyStackCalc()

    assert engine.execute("3 + 4 * 2") == 11
    assert engine.execute("(3 + 4) * 2") == 14
    assert engine.execute("2 ^ 3 ^ 2") == 512
    assert engine.execute("( 3 + 4 ) * 2 - 8 / 4") == 12

    engine.execute("let x = 15")
    engine.execute("let y = x * 2 - 10")

    assert engine.variables["y"] == 20

    engine.execute("undo")
    assert "y" not in engine.variables

    engine.execute("redo")
    assert engine.variables["y"] == 20

    try:
        engine.execute("(3 + 4 * 2")
        assert False
    except ValueError:
        pass

    try:
        engine.execute("100 / (4 - 4)")
        assert False
    except ZeroDivisionError:
        pass

    print("All 9 test cases passed successfully!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        calc = PyStackCalc()
        calc.start_repl()