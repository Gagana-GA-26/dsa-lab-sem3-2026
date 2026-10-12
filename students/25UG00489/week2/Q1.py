class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None


class LL:  # LL is Linkedlist
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
        current = self.Head
        while current is not None:
            print(current.Element, end=" ")
            current = current.next
        print()

    # Return the number of nodes
    def length(self):
        count = 0
        current = self.Head

        while current is not None:
            count += 1
            current = current.next

        return count

    # Count occurrences of an element
    def count(self, x):
        total = 0
        current = self.Head

        while current is not None:
            if current.Element == x:
                total += 1
            current = current.next

        return total

    # Find the largest element
    def find_max(self):
        if self.Head is None:
            return None

        maximum = self.Head.Element
        current = self.Head.next

        while current is not None:
            if current.Element > maximum:
                maximum = current.Element
            current = current.next

        return maximum

    # Return the element at a given index
    def get_nth(self, n):
        if n < 0:
            print("Index out of range")
            return None

        current = self.Head
        index = 0

        while current is not None:
            if index == n:
                return current.Element

            current = current.next
            index += 1

        print("Index out of range")
        return None


# Testing :)
L = LL()
L.append(4)
L.append(9)
L.append(4)
L.append(1)

L.print_list()
print(L.length(), L.count(4), L.find_max(), L.get_nth(2))
L.get_nth(10)
