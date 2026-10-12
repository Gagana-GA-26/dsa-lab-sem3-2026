class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None


class LL:
    def __init__(self):
        self.Head = None

    # Insert an element at the beginning
    def add_element(self, x):
        ptr = Node(x)
        ptr.next = self.Head
        self.Head = ptr

    # Insert an element at the end
    def append(self, x):
        ptr = Node(x)

        if self.Head is None:
            self.Head = ptr
            return

        current = self.Head
        while current.next is not None:
            current = current.next

        current.next = ptr

    # Print all elements
    def print_list(self):
        ptr = self.Head

        while ptr is not None:
            print(ptr.Element, end=" ")
            ptr = ptr.next

        print()


def merge_sorted(L1, L2):
    M = LL()

    ptr1 = L1.Head
    ptr2 = L2.Head

    # Create a dummy node to simplify merging
    dummy = Node(0)
    tail = dummy

    # Compare and link nodes from both lists
    while ptr1 is not None and ptr2 is not None:
        if ptr1.Element <= ptr2.Element:
            tail.next = ptr1
            ptr1 = ptr1.next
        else:
            tail.next = ptr2
            ptr2 = ptr2.next

        tail = tail.next

    # Attach the remaining nodes
    if ptr1 is not None:
        tail.next = ptr1
    else:
        tail.next = ptr2

    M.Head = dummy.next

    return M


# Test case 1
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

# Test case 2: Merge an empty list with 5 -> 6
L3 = LL()

L4 = LL()
L4.append(5)
L4.append(6)

M2 = merge_sorted(L3, L4)
M2.print_list()
