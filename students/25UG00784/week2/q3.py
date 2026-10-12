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

        while current.next is not None:
            current = current.next

        current.next = new_node

    def print_list(self):
        current = self.Head
        values = []

        while current is not None:
            values.append(str(current.Element))
            current = current.next

        print(" ".join(values))


def merge_sorted(L1, L2):
    result = LL()

    first = L1.Head
    second = L2.Head

    dummy = Node(0)
    tail = dummy

    while first is not None and second is not None:
        if first.Element <= second.Element:
            tail.next = Node(first.Element)
            first = first.next
        else:
            tail.next = Node(second.Element)
            second = second.next

        tail = tail.next

    while first is not None:
        tail.next = Node(first.Element)
        tail = tail.next
        first = first.next

    while second is not None:
        tail.next = Node(second.Element)
        tail = tail.next
        second = second.next

    result.Head = dummy.next

    return result


L1 = LL()
L1.append(1)
L1.append(4)
L1.append(7)

L2 = LL()
L2.append(2)
L2.append(3)
L2.append(8)

M = merge_sorted(L1, L2)

M.print_list()