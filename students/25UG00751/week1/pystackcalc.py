
import re
import sys
import math


# Operator configuration
PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3,
    "u+": 4,
    "u-": 4,
}

RIGHT_ASSOCIATIVE = {"^", "u+", "u-"}

TOKEN_PATTERN = re.compile(
    r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[+\-*/^%()=]"
)


# Step 1: Stack class
class Stack:
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


# Step 2: Tokenizer
def tokenize(expr: str) -> list[str]:
    if not isinstance(expr, str) or not expr.strip():
        raise ValueError("Empty expression")

    tokens = []
    position = 0

    for match in TOKEN_PATTERN.finditer(expr):
        # Reject unrecognized characters between tokens.
        gap = expr[position:match.start()]
        if gap.strip():
            raise ValueError(f"Invalid token: {gap.strip()}")

        tokens.append(match.group())
        position = match.end()

    if expr[position:].strip():
        raise ValueError(f"Invalid token: {expr[position:].strip()}")

    if not tokens:
        raise ValueError("Empty expression or invalid tokens")

    return tokens


# Step 3: Infix to postfix conversion
def infix_to_postfix(tokens: list[str]) -> list[str]:
    output = []
    operators = Stack()
    expect_operand = True

    for token in tokens:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            if not expect_operand:
                raise ValueError("Missing operator between operands")
            output.append(token)
            expect_operand = False

        elif re.fullmatch(r"[a-zA-Z_]\w*", token):
            if not expect_operand:
                raise ValueError("Missing operator between operands")
            output.append(token)
            expect_operand = False

        elif token == "(":
            if not expect_operand:
                raise ValueError("Missing operator before '('")
            operators.push(token)
            expect_operand = True

        elif token == ")":
            if expect_operand:
                raise ValueError("Unexpected ')' or missing operand")

            while not operators.is_empty() and operators.peek() != "(":
                output.append(operators.pop())

            if operators.is_empty():
                raise ValueError("Unmatched closing parenthesis")

            operators.pop()  # Remove '('
            expect_operand = False

        elif token in PRECEDENCE:
            # Support unary + and -.
            op = token
            if expect_operand:
                if token in ("+", "-"):
                    op = "u" + token
                else:
                    raise ValueError(
                        f"Unexpected operator: {token}"
                    )

            while not operators.is_empty():
                top = operators.peek()

                if top == "(":
                    break

                higher = PRECEDENCE[top] > PRECEDENCE[op]
                equal_and_left = (
                    PRECEDENCE[top] == PRECEDENCE[op]
                    and op not in RIGHT_ASSOCIATIVE
                )

                if higher or equal_and_left:
                    output.append(operators.pop())
                else:
                    break

            operators.push(op)
            expect_operand = True

        else:
            raise ValueError(f"Invalid token: {token}")

    if expect_operand:
        raise ValueError("Expression ends with an operator or is incomplete")

    while not operators.is_empty():
        op = operators.pop()

        if op == "(":
            raise ValueError("Unmatched opening parenthesis")

        output.append(op)

    return output


# Step 4: Postfix evaluator
def eval_postfix(postfix: list[str], variables: dict) -> float:
    operands = Stack()

    for token in postfix:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            value = float(token) if "." in token else int(token)
            operands.push(value)

        elif token in ("u+", "u-"):
            if operands.size() < 1:
                raise ValueError("Missing operand for unary operator")

            value = operands.pop()
            operands.push(value if token == "u+" else -value)

        elif token in PRECEDENCE:
            if operands.size() < 2:
                raise ValueError("Not enough operands")

            b = operands.pop()
            a = operands.pop()

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

            operands.push(result)

        else:
            if token not in variables:
                raise ValueError(f"Unknown variable: {token}")
            operands.push(variables[token])

    if operands.size() != 1:
        raise ValueError("Invalid expression")

    return operands.pop()


# Step 5: Calculator engine
class PyStackCalc:
    def __init__(self):
        self.variables = {
            "pi": 3.14159,
            "e": 2.71828,
        }
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def execute(self, command: str):
        if not isinstance(command, str) or not command.strip():
            raise ValueError("Empty command")

        command = command.strip()
        lower_command = command.lower()

        # Undo
        if lower_command == "undo":
            if self.undo_stack.is_empty():
                return None

            self.redo_stack.push(dict(self.variables))
            self.variables = self.undo_stack.pop()
            return None

        # Redo
        if lower_command == "redo":
            if self.redo_stack.is_empty():
                return None

            self.undo_stack.push(dict(self.variables))
            self.variables = self.redo_stack.pop()
            return None

        # Variable assignment: let x = 15 or x = 15
        assignment = re.fullmatch(
            r"(?:let\s+)?([a-zA-Z_]\w*)\s*=\s*(.+)",
            command,
            flags=re.IGNORECASE,
        )

        if assignment:
            name = assignment.group(1)
            expression = assignment.group(2)

            # Variable names are case-sensitive, as in Python.
            if name.lower() == "let":
                raise ValueError("Invalid variable name")

            # Calculate before modifying the variables.
            value = self.calculate(expression)

            self.undo_stack.push(dict(self.variables))
            self.redo_stack = Stack()
            self.variables[name] = value

            return value

        if "=" in command:
            raise ValueError("Invalid assignment")

        return self.calculate(command)

    def calculate(self, expression: str):
        tokens = tokenize(expression)
        postfix = infix_to_postfix(tokens)
        return eval_postfix(postfix, self.variables)

    def start_repl(self):
        print("PyStackCalc — Terminal Calculator")
        print("Type 'help' for commands or 'exit' to quit.")

        while True:
            try:
                command = input("calc> ").strip()

                if command.lower() in ("exit", "quit"):
                    print("Goodbye!")
                    break

                if command.lower() == "help":
                    print("Examples:")
                    print("  3 + 4 * 2")
                    print("  (3 + 4) * 2")
                    print("  2 ^ 3 ^ 2")
                    print("  let x = 15")
                    print("  x = x + 5")
                    print("  undo")
                    print("  redo")
                    print("  variables")
                    print("  exit")
                    continue

                if command.lower() == "variables":
                    print(self.variables)
                    continue

                result = self.execute(command)

                if result is not None:
                    print(result)

            except (ValueError, ZeroDivisionError, OverflowError) as error:
                print(f"Error: {error}")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break


# Automated tests
def run_tests():
    print("Running PyStackCalc Test Suite...")
    engine = PyStackCalc()

    # 1. Basic precedence and grouping
    assert engine.execute("3 + 4 * 2") == 11
    assert engine.execute("(3 + 4) * 2") == 14
    assert engine.execute("2 ^ 3 ^ 2") == 512
    assert engine.execute("( 3 + 4 ) * 2 - 8 / 4") == 12

    # 2. Variables
    engine.execute("let x = 15")
    engine.execute("let y = x * 2 - 10")
    assert engine.variables["y"] == 20

    # 3. Undo and redo
    engine.execute("undo")
    assert "y" not in engine.variables

    engine.execute("redo")
    assert engine.variables["y"] == 20

    # 4. Error handling
    try:
        engine.execute("(3 + 4 * 2")
        assert False, "Should raise ValueError for unclosed '('"
    except ValueError:
        pass

    try:
        engine.execute("100 / (4 - 4)")
        assert False, "Should raise ZeroDivisionError"
    except ZeroDivisionError:
        pass

    # Additional tests
    assert engine.execute("10 % 3") == 1
    assert engine.execute("2 ^ 3 ^ 2") == 512
    assert engine.execute("-5 + 8") == 3
    assert engine.execute("pi") == 3.14159

    try:
        engine.execute("unknown_variable + 1")
        assert False, "Should reject unknown variables"
    except ValueError:
        pass

    try:
        engine.execute("3 + * 4")
        assert False, "Should reject malformed expressions"
    except ValueError:
        pass

    print("All tests passed successfully!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        calc = PyStackCalc()
        calc.start_repl()
