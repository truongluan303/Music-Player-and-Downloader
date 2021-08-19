from typing import Generic, TypeVar
T = TypeVar('T')

class CircularDoublyLinkedList(Generic[T]):
    def __init__(self) -> None:
        self.size: int = 0
        self.head: Node = None


    def get_size(self) -> int:
        return self.size


    def is_empty(self) -> bool:
        return self.size == 0


    def append(self, new_value: T) -> None:
        '''
        insert a new node to the end of the linked list
        '''
        if self.is_empty():
            new_node = Node[T](new_value)
            new_node.next = new_node.prev = new_node
            self.head = new_node
        else:
            tail = self.head.prev
            new_node = Node[T](new_value, tail, self.head)
            self.head.prev = new_node
            tail.next = new_node
        self.size += 1


    def remove_at(self, position=None) -> T:
        '''
        remove the node at the input position(index) from the linked list
        @return: the value of the node removed
        '''
        # if position is not specified, we remove the first Node
        if position is None:
            position = 1
        self.__check_position_validity(position, "Attempted to remove from an empty list!!!")
        to_be_removed = self.__get_node_at(position)
        to_be_removed.next.prev = to_be_removed.prev
        if position != 1:
            to_be_removed.prev.next = to_be_removed.next
        else:
            self.head = to_be_removed.next
        self.size -= 1
        return to_be_removed.value


    def remove(self, value: T) -> int:
        '''
        remove the first node with the input value found
        @return: the position of the node removed,
                if the value was not found and no node was removed, return -1
        '''
        current = self.head
        for i in range(self.size):
            if current.value == value:
                current.next.prev = current.prev
                current.prev.next = current.next
                return (i + 1)
            current = current.next
        return -1
            

    def clear(self) -> None:
        '''
        clear every node from the linked list
        '''
        self.head = None
        self.size = 0


    def __get_node_at(self, position: int):
        '''
        @return: the node at the input position(index)
        '''
        self.__check_position_validity(position, "Attempted to search an empty list!!!")
        current = self.head
        for i in range(1, position):
            current = current.next
        return current

    
    def __check_position_validity(self, position: int, empty_message: str) -> None:
        '''
        check if the input position is in valid range. If not, throw an exception
        '''
        if self.is_empty():
            raise Exception(empty_message)
        if position > self.size or position <= 0:
            raise Exception("Illegal Position!!!")


# The Node class
class Node(Generic[T]):
    def __init__(self, value: T, prev=None, next=None) -> None:
        self.value: T = value
        self.prev: self = prev
        self.next: self = next
