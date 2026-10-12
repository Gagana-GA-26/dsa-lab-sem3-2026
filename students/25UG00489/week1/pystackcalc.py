import re
import sys

# STEP 1: STACK CLASS


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

# STEP 2: TOKENIZER


def tokenize(expr: str) -> list[str]:
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"

    tokens = re.findall(pattern, expr)

    # Ensure that no invalid characters or text were skipped.
    remaining = re.sub(pattern, "", expr)
    if remaining.strip():
        raise ValueError("Invalid characters in expression")

    if not tokens:
        raise ValueError("Empty expression or invalid tokens")

    return tokens


# STEP 3: INFIX TO POSTFIX CONVERSION
PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3
}

RIGHT_ASSOCIATIVE = {"^"}


def infix_to_postfix(tokens: list[str]) -> list[str]:
    output = []
    operators = Stack()

    for token in tokens:

        # Numbers and variable names go directly to output.
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            output.append(token)

        elif re.fullmatch(r"[a-zA-Z_]\w*", token):
            output.append(token)

        # Opening parenthesis.
        elif token == "(":
            operators.push(token)

        # Closing parenthesis.
        elif token == ")":
            found_opening = False

            while not operators.is_empty():
                top = operators.pop()

                if top == "(":
                    found_opening = True
                    break

                output.append(top)

            if not found_opening:
                raise ValueError("Mismatched parentheses")

        # Operators.
        elif token in PRECEDENCE:

            while not operators.is_empty():
                top = operators.peek()

                if top == "(":
                    break

                higher_precedence = (
                    PRECEDENCE[top] > PRECEDENCE[token]
                )

                equal_left_associative = (
                    PRECEDENCE[top] == PRECEDENCE[token]
                    and token not in RIGHT_ASSOCIATIVE
                )

                if higher_precedence or equal_left_associative:
                    output.append(operators.pop())
                else:
                    break

            operators.push(token)

        else:
            raise ValueError(f"Invalid token: {token}")

    # Move remaining operators to output.
    while not operators.is_empty():
        top = operators.pop()

        if top == "(":
            raise ValueError("Mismatched parentheses")

        output.append(top)

    return output

# STEP 4: POSTFIX EVALUATOR


def eval_postfix(tokens: list[str], variables: dict) -> int | float:
    operands = Stack()

    for token in tokens:

        # Number.
        if re.fullmatch(r"\d+(?:\.\d+)?", token):

            if "." in token:
                operands.push(float(token))
            else:
                operands.push(int(token))

        # Variable.
        elif re.fullmatch(r"[a-zA-Z_]\w*", token):

            if token not in variables:
                raise NameError(f"Undefined variable: {token}")

            operands.push(variables[token])

        # Operator.
        elif token in PRECEDENCE:

            if operands.size() < 2:
                raise ValueError("Invalid mathematical expression")

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
            raise ValueError(f"Invalid postfix token: {token}")

    # A valid expression must leave exactly one result.
    if operands.size() != 1:
        raise ValueError("Invalid mathematical expression")

    return operands.pop()

# STEP 5: CALCULATOR ENGINE


class PyStackCalc:

    def __init__(self):
        self.variables = {
            "pi": 3.14159,
            "e": 2.71828
        }

        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def execute(self, command: str):

        command = command.strip()

        if not command:
            return None

        # Undo the previous variable change.
        if command.lower() == "undo":

            if self.undo_stack.is_empty():
                return None

            self.redo_stack.push(dict(self.variables))
            self.variables = self.undo_stack.pop()

            return None

        # Redo the previous undone change.
        if command.lower() == "redo":

            if self.redo_stack.is_empty():
                return None

            self.undo_stack.push(dict(self.variables))
            self.variables = self.redo_stack.pop()

            return None

        # Handle variable assignment.
        assignment = re.fullmatch(
            r"(?:let\s+)?([a-zA-Z_]\w*)\s*=\s*(.+)",
            command
        )

        if assignment:

            name = assignment.group(1)
            expression = assignment.group(2)

            # Constants pi and e are predefined.
            if name in ("pi", "e"):
                raise ValueError("Cannot overwrite built-in constants")

            # Calculate the new value before changing the variables.
            tokens = tokenize(expression)
            postfix = infix_to_postfix(tokens)
            value = eval_postfix(postfix, self.variables)

            # Save the previous state for undo.
            self.undo_stack.push(dict(self.variables))

            # A new variable change invalidates the redo history.
            self.redo_stack = Stack()

            self.variables[name] = value

            return value

        # Evaluate a normal mathematical expression.
        tokens = tokenize(command)
        postfix = infix_to_postfix(tokens)

        return eval_postfix(postfix, self.variables)

    def start_repl(self):

        print("        PyStackCalc :) ")
        print("Enter a mathematical expression.")
        print("Use 'let x = expression' to assign variables.")
        print("Commands: undo, redo, exit")
        print()

        while True:

            try:
                command = input("calc> ").strip()

                if command.lower() in ("exit", "quit"):
                    print("Goodbye!")
                    break

                result = self.execute(command)

                if result is not None:
                    print(result)

            except (ValueError, NameError, ZeroDivisionError, IndexError) as error:
                print(f"Error: {error}")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

# FOR TESTING :)


def run_tests():
    """Automated test cases to verify the implementation."""

    print("Running PyStackCalc Test Suite...")

    engine = PyStackCalc()

    # 1. Basic precedence and grouping.
    assert engine.execute("3 + 4 * 2") == 11
    assert engine.execute("(3 + 4) * 2") == 14
    assert engine.execute("2 ^ 3 ^ 2") == 512
    assert engine.execute("( 3 + 4 ) * 2 - 8 / 4") == 12

    # 2. Variables.
    engine.execute("let x = 15")
    engine.execute("let y = x * 2 - 10")

    assert engine.variables["y"] == 20

    # 3. Undo and redo.
    engine.execute("undo")
    assert "y" not in engine.variables

    engine.execute("redo")
    assert engine.variables["y"] == 20

    # 4. Error handling: missing closing parenthesis.
    try:
        engine.execute("(3 + 4 * 2")
        assert False, "Should raise ValueError for unclosed '('"
    except ValueError:
        pass

    # 5. Error handling: division by zero.
    try:
        engine.execute("100 / (4 - 4)")
        assert False, "Should raise ZeroDivisionError"
    except ZeroDivisionError:
        pass

    print("All 9 test cases passed successfully!")


# PROGRAM ENTRY POINT
if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()

    else:
        calc = PyStackCalc()
        calc.start_repl()
