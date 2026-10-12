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

        while current is not None:
            print(current.Element, end="")
            if current.next is not None:
                print(" ", end="")
            current = current.next

        print()


def merge_sorted(L1, L2):
    result = LL()

    # Tail points to the last node in the merged list.
    tail = None
    a = L1.Head
    b = L2.Head

    while a is not None and b is not None:
        # Select the smaller node.
        if a.Element <= b.Element:
            chosen = a
            a = a.next
        else:
            chosen = b
            b = b.next

        # Link the chosen node into the result.
        if result.Head is None:
            result.Head = chosen
        else:
            tail.next = chosen

        tail = chosen

    # Attach any remaining nodes.
    if a is not None:
        if result.Head is None:
            result.Head = a
        else:
            tail.next = a

    elif b is not None:
        if result.Head is None:
            result.Head = b
        else:
            tail.next = b

    return result


# Test Q3
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

# Test with an empty list
L3 = LL()
L4 = LL()
L4.append(5)
L4.append(6)

M2 = merge_sorted(L3, L4)
M2.print_list()
