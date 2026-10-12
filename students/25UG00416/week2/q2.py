
    # Search for the first occurrence of x
    def search(self, x):
        current = self.Head
        position = 0

        while current is not None:
            if current.Element == x:
                return position

            current = current.next
            position += 1

        return -1

    # Delete all occurrences of x
    def delete_element(self, x):
        # Remove matching nodes from the head
        while self.Head is not None and self.Head.Element == x:
            self.Head = self.Head.next

        # Remove matching nodes from the rest of the list
        current = self.Head

        while current is not None and current.next is not None:
            if current.next.Element == x:
                current.next = current.next.next
            else:
                current = current.next
