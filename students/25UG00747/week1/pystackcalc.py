import math

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

def tokenize(text):
    tokens = []
    current = ""

    for char in text:

        if char.isalnum() or char == "." or char == "_":
            current += char
        else:
            if current:
                tokens.append(current)
                current = ""
            if char in "+-*/%^()":
                tokens.append(char)

    if current:
        tokens.append(current)

    return tokens

def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

def is_variable(token):
    if len(token) == 0:
        return False
    first = token[0]
    return first.isalpha() or first == "_"

FUNCTIONS = ["sqrt", "abs", "sin"]

def is_function(token):
    return token in FUNCTIONS

def is_unary_minus(token, prev_token):
    # A '-' means "negative" (not "subtract") when there's nothing
    # meaningful directly to its left: start of expression, right after
    # another operator, right after '(', or right after a function name.
    if token != "-":
        return False
    if prev_token is None:
        return True
    if prev_token == "(":
        return True
    if is_function(prev_token):
        return True
    if prev_token in "+-*/%^":
        return True
    return False

def priority(op):
    if op == "u-":
        return 4  # unary minus binds tightest: "-2+3" must be (-2)+3, not -(2+3)
    if op == "^":
        return 3
    if op == "*" or op == "/" or op == "%":
        return 2
    if op == "+" or op == "-":
        return 1
    return 0

def infix_to_postfix(tokens):
    output = []
    stack = Stack()
    prev_token = None

    for token in tokens:

        if is_number(token):
            output.append(token)

        elif is_function(token):
            stack.push(token)

        elif is_unary_minus(token, prev_token):
            stack.push("u-")

        elif is_variable(token):
            output.append(token)

        elif token == "(":
            stack.push(token)

        elif token == ")":
            while not stack.is_empty() and stack.peek() != "(":
                output.append(stack.pop())
            if stack.is_empty():
                raise ValueError("missing '('")
            stack.pop()  # discard the '('
            if not stack.is_empty() and is_function(stack.peek()):
                output.append(stack.pop())  # the function applies now

        else:  # it's an operator: + - * / % ^
            while True:
                if stack.is_empty():
                    break
                top = stack.peek()
                if top == "(":
                    break
                if priority(top) > priority(token):
                    output.append(stack.pop())
                elif priority(top) == priority(token) and token != "^":
                    output.append(stack.pop())
                else:
                    break
            stack.push(token)

        prev_token = token

    while not stack.is_empty():
        top = stack.pop()
        if top == "(":
            raise ValueError("missing ')'")
        output.append(top)

    return output

def evaluate(postfix, variables):
    stack = Stack()

    for token in postfix:

        if is_number(token):
            stack.push(float(token))

        elif token == "u-":
            value = stack.pop()
            stack.push(-value)

        elif is_function(token):
            value = stack.pop()
            if token == "sqrt":
                if value < 0:
                    raise ValueError("sqrt of negative number")
                result = math.sqrt(value)
            elif token == "abs":
                result = abs(value)
            elif token == "sin":
                result = math.sin(value)
            stack.push(result)

        elif is_variable(token):
            if token not in variables:
                raise NameError("unknown variable: " + token)
            stack.push(variables[token])

        else:  # operator
            a = stack.pop()  # right-hand side (popped first)
            b = stack.pop()  # left-hand side

            if token == "+":
                result = b + a
            elif token == "-":
                result = b - a
            elif token == "*":
                result = b * a
            elif token == "/":
                if a == 0:
                    raise ZeroDivisionError("division by zero")
                result = b / a
            elif token == "%":
                if a == 0:
                    raise ZeroDivisionError("division by zero")
                result = b % a
            elif token == "^":
                result = b ** a

            stack.push(result)

    if stack.size() != 1:
        raise ValueError("invalid expression")

    return stack.pop()

def copy_vars(variables):
    new_vars = {}
    for name in variables:
        new_vars[name] = variables[name]
    return new_vars

def run():
    variables = {}
    history = []
    undo_stack = Stack()
    redo_stack = Stack()
    trace = False

    print("Commands: let <name> = <expr>, vars, history, trace, undo, redo, exit")

    while True:
        text = input("> ").strip()

        if text == "":
            continue

        if text == "exit":
            break

        if text == "vars":
            for name in variables:
                print(name, "=", variables[name])
            continue

        if text == "history":
            for item in history:
                print(item)
            continue

        if text == "trace":
            trace = not trace
            print("trace on" if trace else "trace off")
            continue

        if text == "undo":
            if undo_stack.is_empty():
                print("Nothing to undo")
            else:
                redo_stack.push(copy_vars(variables))
                variables = undo_stack.pop()
                print("Undo complete")
            continue

        if text == "redo":
            if redo_stack.is_empty():
                print("Nothing to redo")
            else:
                undo_stack.push(copy_vars(variables))
                variables = redo_stack.pop()
                print("Redo complete")
            continue

        try:
            if text.startswith("let "):
                rest = text[4:]
                if "=" not in rest:
                    raise ValueError("use: let <name> = <expr>")

                name, expr_text = rest.split("=", 1)
                name = name.strip()
                expr_text = expr_text.strip()

                tokens = tokenize(expr_text)
                postfix = infix_to_postfix(tokens)
                if trace:
                    print("tokens :", tokens)
                    print("postfix:", postfix)
                value = evaluate(postfix, variables)

                undo_stack.push(copy_vars(variables))
                redo_stack = Stack()
                variables[name] = value
                history.append(text)
                print(name, "=", value)

            else:
                tokens = tokenize(text)
                postfix = infix_to_postfix(tokens)
                if trace:
                    print("tokens :", tokens)
                    print("postfix:", postfix)
                result = evaluate(postfix, variables)
                history.append(text)
                print(result)

        except (ValueError, ZeroDivisionError, NameError, IndexError) as e:
            print("Error:", e)

if __name__ == "__main__":
    run()