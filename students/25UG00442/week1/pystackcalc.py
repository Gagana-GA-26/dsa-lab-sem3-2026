
import re
import sys

class Stack:
    def __init__(self): self.items = []
    def push(self, x): self.items.append(x)
    def pop(self):
        if not self.items: raise IndexError("Empty stack")
        return self.items.pop()
    def peek(self): return self.items[-1] if self.items else None
    def is_empty(self): return not self.items
    def size(self): return len(self.items)
    def to_list(self): return self.items.copy()

P = {'+':1, '-':1, '*':2, '/':2, '%':2, '^':3}
R = {'^'}

def tokenize(s):
    p = r'\d+(?:\.\d+)?|[a-zA-Z_]\w*|[+\-*/^%()=]'
    t = re.findall(p, s)
    if not t or re.sub(p, '', s).strip(): raise ValueError("Invalid expression")
    return t

def infix_to_postfix(tokens):
    out, st = [], Stack()
    for t in tokens:
        if re.fullmatch(r'\d+(?:\.\d+)?|[a-zA-Z_]\w*', t):
            out.append(t)
        elif t == '(':
            st.push(t)
        elif t == ')':
            while st.peek() != '(':
                if st.is_empty(): raise ValueError("Mismatched parentheses")
                out.append(st.pop())
            st.pop()
        elif t in P:
            while st.peek() in P and (P[st.peek()] > P[t] or
                  (P[st.peek()] == P[t] and t not in R)):
                out.append(st.pop())
            st.push(t)
        else:
            raise ValueError("Invalid token")
    while not st.is_empty():
        t = st.pop()
        if t == '(': raise ValueError("Mismatched parentheses")
        out.append(t)
    return out

def eval_postfix(tokens, variables=None):
    variables = variables or {}
    st = Stack()
    for t in tokens:
        if re.fullmatch(r'\d+(?:\.\d+)?', t):
            st.push(float(t) if '.' in t else int(t))
        elif t not in P:
            if t not in variables: raise ValueError("Undefined variable: " + t)
            st.push(variables[t])
        else:
            b, a = st.pop(), st.pop()
            if t in ('/', '%') and b == 0: raise ZeroDivisionError("Division by zero")
            st.push({'+':lambda:a+b, '-':lambda:a-b,
                     '*':lambda:a*b, '/':lambda:a/b,
                     '%':lambda:a%b, '^':lambda:a**b}[t]())
    if st.size() != 1: raise ValueError("Invalid expression")
    return st.pop()

class PyStackCalc:
    def __init__(self):
        self.variables = {'pi':3.14159, 'e':2.71828}
        self.undo_stack, self.redo_stack = Stack(), Stack()

    def execute(self, s):
        s = s.strip()
        if s in ('undo', 'redo'):
            src, dst = (self.undo_stack, self.redo_stack) if s == 'undo' else (self.redo_stack, self.undo_stack)
            if src.is_empty(): raise ValueError("Nothing to " + s)
            dst.push(self.variables.copy())
            self.variables = src.pop()
            return None
        m = re.fullmatch(r'(?:let\s+)?([a-zA-Z_]\w*)\s*=\s*(.+)', s)
        if m:
            name, rhs = m.groups()
            if name in ('pi', 'e'): raise ValueError("Reserved name")
            v = self.calc(rhs)
            self.undo_stack.push(self.variables.copy())
            self.redo_stack = Stack()
            self.variables[name] = v
            return v
        return self.calc(s)

    def calc(self, s):
        return eval_postfix(infix_to_postfix(tokenize(s)), self.variables)

    def start_repl(self):
        while True:
            try:
                s = input('calc> ')
                if s.strip().lower() in ('exit', 'quit'): break
                r = self.execute(s)
                if r is not None: print(r)
            except (ValueError, IndexError, ZeroDivisionError) as e:
                print("Error:", e)

def run_tests():
    c = PyStackCalc()
    assert c.execute("3 + 4 * 2") == 11
    assert c.execute("(3 + 4) * 2") == 14
    assert c.execute("2 ^ 3 ^ 2") == 512
    assert c.execute("( 3 + 4 ) * 2 - 8 / 4") == 12
    c.execute("let x = 15")
    c.execute("let y = x * 2 - 10")
    assert c.variables['y'] == 20
    c.execute("undo")
    assert 'y' not in c.variables
    c.execute("redo")
    assert c.variables['y'] == 20
    try: c.execute("(3 + 4 * 2")
    except ValueError: pass
    else: assert False
    try: c.execute("100 / (4 - 4)")
    except ZeroDivisionError: pass
    else: assert False
    print("All 9 test cases passed successfully!")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test': run_tests()
    else: PyStackCalc().start_repl()
