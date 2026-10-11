class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None

class LL:
    def __init__(self):
        self.Head = None

    def append(self, x):
        new_node = Node(x)
        if self.Head is None:
            self.Head = new_node
            return
        current = self.Head
        while current.next:
            current = current.next
        current.next = new_node

    def print_list(self):
        current = self.Head
        while current:
            print(current.Element, end=" ")
            current = current.next
        print()


def merge_sorted(L1, L2):
    result = LL()
    dummy = Node(0)
    tail = dummy
    a = L1.Head
    b = L2.Head

    while a and b:
        if a.Element <= b.Element:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next

    if a:
        tail.next = a
    else:
        tail.next = b

    result.Head = dummy.next
    return result


L1 = LL()
for x in [1, 4, 7]:
    L1.append(x)

L2 = LL()
for x in [2, 3, 8]:
    L2.append(x)

M = merge_sorted(L1, L2)
M.print_list()
```
