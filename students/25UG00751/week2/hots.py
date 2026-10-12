
class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None


class BigInt:
    def __init__(self):
        self.Head = None

    @classmethod
    def from_string(cls, s):
        if not s or not s.isdigit():
            raise ValueError("Enter a non-negative integer string")

        number = cls()

        for ch in reversed(s):
            number.append(int(ch))

        number.remove_leading_zeros()
        return number

    def append(self, digit):
        node = Node(digit)

        if self.Head is None:
            self.Head = node
            return

        current = self.Head
        while current.next is not None:
            current = current.next

        current.next = node

    def remove_leading_zeros(self):
        if self.Head is None:
            self.Head = Node(0)
            return

        # Digits are stored in reverse order.
        # Remove zeros at the most significant end.
        previous = None
        current = self.Head

        while current.next is not None:
            previous = current
            current = current.next

        while previous is not None and current.Element == 0:
            previous.next = None
            current = self.Head
            previous = None

            while current.next is not None:
                previous = current
                current = current.next

        if self.Head is None:
            self.Head = Node(0)

    def to_string(self):
        digits = []
        current = self.Head

        while current is not None:
            digits.append(str(current.Element))
            current = current.next

        return "".join(reversed(digits)).lstrip("0") or "0"


def add(A, B):
    result = BigInt()
    p = A.Head
    q = B.Head
    carry = 0

    while p is not None or q is not None or carry:
        total = carry

        if p is not None:
            total += p.Element
            p = p.next

        if q is not None:
            total += q.Element
            q = q.next

        result.append(total % 10)
        carry = total // 10

    result.remove_leading_zeros()
    return result


def subtract(A, B):
    # Assumes A >= B
    result = BigInt()
    p = A.Head
    q = B.Head
    borrow = 0

    while p is not None:
        digit = p.Element - borrow
        if q is not None:
            digit -= q.Element
            q = q.next

        if digit < 0:
            digit += 10
            borrow = 1
        else:
            borrow = 0

        result.append(digit)
        p = p.next

    result.remove_leading_zeros()
    return result


if __name__ == "__main__":
    A = BigInt.from_string("999999999999")
    B = BigInt.from_string("1")
    print(add(A, B).to_string())

    A = BigInt.from_string("12345")
    B = BigInt.from_string("678")
    print(add(A, B).to_string())

    A = BigInt.from_string("1000")
    B = BigInt.from_string("999")
    print(subtract(A, B).to_string())

    A = BigInt.from_string("500")
    B = BigInt.from_string("500")
    print(subtract(A, B).to_string())
