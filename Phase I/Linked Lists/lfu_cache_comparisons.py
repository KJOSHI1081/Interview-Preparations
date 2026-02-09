"""
This file contains two implementations of LFU (Least Frequently Used) cache:
1. Hash Map + Frequency Map-based LFU
2. Doubly Linked List + Frequency Map-based LFU

Each implementation includes comments explaining its pros and cons, making it easier to understand and compare their trade-offs.
"""

# Implementation 1: Hash Map + Frequency Map-based LFU
class LFUCache_HashMap:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # Map key to (value, frequency)
        self.freq_map = {}  # Map frequency to {key_set}
        self.min_freq = 0  # Keep track of the minimum frequency usage

    def _update(self, key: int):
        value, freq = self.cache[key]
        # Remove key from current frequency list
        self.freq_map[freq].remove(key)
        if not self.freq_map[freq]:
            if self.min_freq == freq:
                self.min_freq += 1  # Update minimum frequency
            del self.freq_map[freq]

        # Add key to the next frequency
        new_freq = freq + 1
        self.cache[key] = (value, new_freq)
        if new_freq not in self.freq_map:
            self.freq_map[new_freq] = set()
        self.freq_map[new_freq].add(key)

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self._update(key)
        return self.cache[key][0]

    def put(self, key: int, value: int):
        if self.capacity == 0:  # Handle corner case where capacity is 0
            return
        
        if key in self.cache:
            # Update value and frequency
            self.cache[key] = (value, self.cache[key][1])
            self._update(key)
        else:
            if len(self.cache) >= self.capacity:
                # Evict the least frequently used item
                lfu_key = self.freq_map[self.min_freq].pop()
                if not self.freq_map[self.min_freq]:
                    del self.freq_map[self.min_freq]
                del self.cache[lfu_key]
            
            # Add the new key-value pair
            self.cache[key] = (value, 1)
            self.min_freq = 1
            if self.min_freq not in self.freq_map:
                self.freq_map[self.min_freq] = set()
            self.freq_map[self.min_freq].add(key)

# Pros of Hash Map + Frequency Map-based LFU:
# 1. Simplicity: Uses basic data structures like dictionaries and sets, which are easy to implement in Python.
# 2. Fast Lookups: Offers O(1) average time complexity for most operations.
# 3. Memory Efficiency: Avoids pointer overheads of doubly linked lists.

# Cons:
# 1. No Natural LRU within Frequency: Does not maintain LRU order directly within the same frequency bucket.
# 2. Requires additional logic to handle ties (e.g., maintaining insertion order).


# Implementation 2: Doubly Linked List + Frequency Map-based LFU
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 1
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = Node(None, None)  # Dummy head
        self.tail = Node(None, None)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_to_front(self, node):
        """Add a node to the front (right after the head)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def remove_node(self, node):
        """Remove a node from the linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def remove_last(self):
        """Remove the last node from the list (right before the tail)."""
        if self.head.next == self.tail:  # Empty list
            return None
        last_node = self.tail.prev
        self.remove_node(last_node)
        return last_node

    def is_empty(self):
        """Check if the doubly linked list is empty."""
        return self.head.next == self.tail

class LFUCache_DoublyLinkedList:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.size = 0
        self.node_map = {}  # key -> Node
        self.freq_map = {}  # freq -> DoublyLinkedList
        self.min_freq = 0

    def update_frequency(self, node):
        """Update the frequency of a node."""
        freq = node.freq
        self.freq_map[freq].remove_node(node)

        # If the current list is empty, delete it and update min_freq
        if self.freq_map[freq].is_empty():
            del self.freq_map[freq]
            if freq == self.min_freq:
                self.min_freq += 1

        # Increase the frequency and add the node to the new frequency list
        node.freq += 1
        new_freq = node.freq
        if new_freq not in self.freq_map:
            self.freq_map[new_freq] = DoublyLinkedList()
        self.freq_map[new_freq].add_to_front(node)

    def get(self, key: int) -> int:
        if key not in self.node_map:
            return -1

        node = self.node_map[key]
        # Update the access frequency of the node
        self.update_frequency(node)
        return node.value

    def put(self, key: int, value: int):
        if self.capacity == 0:
            return

        if key in self.node_map:
            # Update the node's value and frequency
            node = self.node_map[key]
            node.value = value
            self.update_frequency(node)
        else:
            # If the cache is full, evict the least frequently used (LFU) node
            if self.size >= self.capacity:
                # Remove the least frequently used node
                lfu_list = self.freq_map[self.min_freq]
                node_to_remove = lfu_list.remove_last()
                del self.node_map[node_to_remove.key]
                self.size -= 1

            # Add the new key-value pair
            new_node = Node(key, value)
            self.node_map[key] = new_node
            if 1 not in self.freq_map:
                self.freq_map[1] = DoublyLinkedList()
            self.freq_map[1].add_to_front(new_node)
            self.min_freq = 1
            self.size += 1

# Pros of Doubly Linked List + Frequency Map-based LFU:
# 1. Maintains LRU Order: Easily manages LRU within frequency buckets.
# 2. Efficient Operations: Supports O(1) operations for adding, removing, and updating nodes.
#
# Cons:
# 1. Memory Overhead: Each node requires additional pointers, increasing memory consumption.
# 2. Pointer Management Complexity: Requires careful handling of node connections to avoid bugs.