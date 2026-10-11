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

    def search(self, x):
        current = self.Head
        index = 0
        while current:
            if current.Element == x:
                return index
            current = current.next
            index += 1
        return -1

    def delete_element(self, x):
        while self.Head and self.Head.Element == x:
            self.Head = self.Head.next

        current = self.Head
        while current and current.next:
            if current.next.Element == x:
                current.next = current.next.next
            else:
                current = current.next


L = LL()
for x in [1, 1, 2, 1, 3]:
    L.append(x)

print(L.search(2))
print(L.search(5))
L.delete_element(1)
L.print_list()
```
