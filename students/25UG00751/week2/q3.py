
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
        elements = []

        while current is not None:
            elements.append(str(current.Element))
            current = current.next

        print(" ".join(elements))


def merge_sorted(L1, L2):
    result = LL()

    # Dummy node simplifies linking
    dummy = Node(0)
    tail = dummy

    p = L1.Head
    q = L2.Head

    while p is not None and q is not None:
        if p.Element <= q.Element:
            next_node = p.next
            tail.next = p
            p = next_node
        else:
            next_node = q.next
            tail.next = q
            q = next_node

        tail = tail.next

    # Attach any remaining nodes
    if p is not None:
        tail.next = p
    elif q is not None:
        tail.next = q

    result.Head = dummy.next
    return result


if __name__ == "__main__":
    L1 = LL()
    for value in [1, 4, 7]:
        L1.append(value)

    L2 = LL()
    for value in [2, 3, 8]:
        L2.append(value)

    M = merge_sorted(L1, L2)
    M.print_list()

    # Edge case: merging an empty list
    empty = LL()
    L3 = LL()
    L3.append(5)
    L3.append(6)

    merged = merge_sorted(empty, L3)
    merged.print_list()
