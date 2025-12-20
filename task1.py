class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int):
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        prev.next = cur.next
        cur = None

    def search_element(self, data: int) -> Node | None:
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def print_list(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next


def reverse_linked_list(linked_list: LinkedList) -> LinkedList:
    prev = None
    current = linked_list.head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    linked_list.head = prev
    return linked_list

def merge_sort_linked_list(linked_list: LinkedList) -> LinkedList:
    if linked_list.head is None or linked_list.head.next is None:
        return linked_list

    base = linked_list.head
    next_to_base = base.next
    base.next = None

    def from_head(head: Node) -> LinkedList:
        linked_list = LinkedList()
        linked_list.head = head
        return linked_list

    left_half = merge_sort_linked_list(from_head(linked_list.head))
    right_half = merge_sort_linked_list(from_head(next_to_base))
    return merge_sorted_linked_lists(left_half, right_half)

def merge_sorted_linked_lists(llist1: LinkedList, llist2: LinkedList) -> LinkedList:
    merged_list = LinkedList()
    ptr1 = llist1.head
    ptr2 = llist2.head

    while ptr1 and ptr2:
        if ptr1.data < ptr2.data:
            merged_list.insert_at_end(ptr1.data)
            ptr1 = ptr1.next
        else:
            merged_list.insert_at_end(ptr2.data)
            ptr2 = ptr2.next

    while ptr1:
        merged_list.insert_at_end(ptr1.data)
        ptr1 = ptr1.next

    while ptr2:
        merged_list.insert_at_end(ptr2.data)
        ptr2 = ptr2.next

    return merged_list

def main():
    llist = LinkedList()
    llist.insert_at_beginning(5)
    llist.insert_at_beginning(10)
    llist.insert_at_beginning(15)

    print("Оригінальний список:")
    llist.print_list()

    llist = reverse_linked_list(llist)

    print("Реверсований список:")
    llist.print_list()

    llist1 = LinkedList()
    llist1.insert_at_end(1)
    llist1.insert_at_end(3)
    llist1.insert_at_end(5)

    llist2 = LinkedList()
    llist2.insert_at_end(2)
    llist2.insert_at_end(4)
    llist2.insert_at_end(6)
    merged_llist = merge_sorted_linked_lists(llist1, llist2)
    print("Об'єднаний відсортований список:")
    merged_llist.print_list()

    llist3 = LinkedList()
    llist3.insert_at_end(4)
    llist3.insert_at_end(2)
    llist3.insert_at_end(1)
    llist3.insert_at_end(3)
    llist3.insert_at_end(5)
    llist3.insert_at_end(0)
    sorted_llist = merge_sort_linked_list(llist3)
    print("Відсортований список за допомогою сортування злиттям:")
    sorted_llist.print_list()

if __name__ == "__main__":
    main()