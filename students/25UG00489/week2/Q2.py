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

    # Return the number of nodes
    def length(self):
        count = 0
        ptr = self.Head

        while ptr is not None:
            count += 1
            ptr = ptr.next

        return count

    # Count occurrences of an element
    def count(self, x):
        total = 0
        ptr = self.Head

        while ptr is not None:
            if ptr.Element == x:
                total += 1
            ptr = ptr.next

        return total

    # Find the largest element
    def find_max(self):
        if self.Head is None:
            return None

        maximum = self.Head.Element
        ptr = self.Head.next

        while ptr is not None:
            if ptr.Element > maximum:
                maximum = ptr.Element
            ptr = ptr.next

        return maximum

    # Return the element at a given index
    def get_nth(self, n):
        if n < 0:
            print("Index out of range")
            return None

        ptr = self.Head
        index = 0

        while ptr is not None:
            if index == n:
                return ptr.Element

            ptr = ptr.next
            index += 1

        print("Index out of range")
        return None

    # Search for the first occurrence of x
    def search(self, x):
        ptr = self.Head
        index = 0

        while ptr is not None:
            if ptr.Element == x:
                return index

            ptr = ptr.next
            index += 1

        return -1

    # Delete all occurrences of x
    def delete_element(self, x):
        while self.Head is not None and self.Head.Element == x:
            self.Head = self.Head.next

        ptr = self.Head

        while ptr is not None and ptr.next is not None:
            if ptr.next.Element == x:
                ptr.next = ptr.next.next
            else:
                ptr = ptr.next


# Testing :)
L = LL()
L.append(1)
L.append(1)
L.append(2)
L.append(1)
L.append(3)

print(L.search(2))
print(L.search(5))

L.delete_element(1)
L.print_list()
