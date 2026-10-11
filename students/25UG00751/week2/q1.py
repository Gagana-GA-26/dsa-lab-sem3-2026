
class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None


class LL:
    def __init__(self):
        self.Head = None

    # Insert at the head
    def add_element(self, x):
        new_node = Node(x)
        new_node.next = self.Head
        self.Head = new_node

    # Insert at the tail
    def append(self, x):
        new_node = Node(x)

        if self.Head is None:
            self.Head = new_node
            return

        current = self.Head
        while current.next is not None:
            current = current.next

        current.next = new_node

    # Print elements in order
    def print_list(self):
        current = self.Head
        elements = []

        while current is not None:
            elements.append(str(current.Element))
            current = current.next

        print(" ".join(elements))

    # Count nodes
    def length(self):
        count = 0
        current = self.Head

        while current is not None:
            count += 1
            current = current.next

        return count

    # Count occurrences of x
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

    # Get element at zero-based index n
    def get_nth(self, n):
        if not isinstance(n, int) or n < 0:
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


if __name__ == "__main__":
    L = LL()
    L.append(4)
    L.append(9)
    L.append(4)
    L.append(1)

    L.print_list()
    print(L.length(), L.count(4), L.find_max(), L.get_nth(2))
    L.get_nth(10)
