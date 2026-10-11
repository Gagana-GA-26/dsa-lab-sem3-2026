import math
import re

class Stack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1] if self.items else None


def precedence(op):
    return {'+': 1, '-': 1, '*': 2, '/': 2}.get(op, 0)


def infix_to_postfix(expr):
    stack = Stack()
    output = []

    tokens = re.findall(r"sqrt|\d+|[()+\-*/]", expr.replace(" ", ""))

    print("\nSTEP 1: Infix to Postfix")

    for ch in tokens:
        if ch.isdigit():
            output.append(ch)

        elif ch == 'sqrt' or ch == '(':
            stack.push(ch)

        elif ch == ')':
            while stack.peek() != '(':
                output.append(stack.pop())
            stack.pop()

            if stack.peek() == 'sqrt':
                output.append(stack.pop())

        else:
            while (stack.peek() and stack.peek() not in ('(', 'sqrt')
                   and precedence(stack.peek()) >= precedence(ch)):
                output.append(stack.pop())
            stack.push(ch)

        print("Read:", ch, "| Stack:", stack.items,
              "| Postfix:", ' '.join(output))

    while stack.peek():
        output.append(stack.pop())

    print("\nSTEP 2: Final Postfix:", ' '.join(output))
    return output


def calculate(postfix):
    stack = Stack()
    print("\nSTEP 3: Calculate Postfix")

    for ch in postfix:
        if ch.isdigit():
            stack.push(int(ch))
            print("Push", ch, "->", stack.items)

        elif ch == 'sqrt':
            a = stack.pop()

            if a < 0:
                raise ValueError("Square root of a negative number is not supported")

            result = math.sqrt(a)
            print("sqrt(", a, ") =", result)
            stack.push(result)
            print("Stack:", stack.items)

        else:
            b = stack.pop()
            a = stack.pop()

            if ch == '+':
                result = a + b
            elif ch == '-':
                result = a - b
            elif ch == '*':
                result = a * b
            elif ch == '/':
                if b == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                result = a / b

            print(a, ch, b, "=", result)
            stack.push(result)
            print("Stack:", stack.items)

    return stack.pop()


expr = input("Enter infix: ")
postfix = infix_to_postfix(expr)
answer = calculate(postfix)

if isinstance(answer, float) and answer.is_integer():
    answer = int(answer)

print("\nFINAL ANSWER:", answer)