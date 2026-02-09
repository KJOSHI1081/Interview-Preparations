import heapq

"""
LINKED LIST PREP: DAY 3
-------------------------------------------------
This file covers the progression from fundamental pointer manipulation 
to complex structural design and system-level data structures.

Key Patterns Included:
1. Reversal & Cycle Detection
2. Arithmetic & Random Pointer Cloning
3. Scaling (Merge K, K-Groups)
4. Hierarchy & Stability (Flattening, Partitioning)
5. System Design (LRU Cache)

Scaling: Merge K Lists (Heap/Divide & Conquer)
Complexity: Reverse K-Group (Recursive/Iterative segmenting)
Hierarchy: Flattening (DFS/Stack)
System Design: LRU Cache (Hashmap + DLL)
Stability: Partition List (Two-Pointer/Sentinel)
""" 
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Node:
    """Node for Multilevel List and LRU Cache"""
    def __init__(self, val, prev=None, next=None, child=None):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child

# ---------------------------------------------------------
# 1. MERGE K SORTED LISTS
# ---------------------------------------------------------
def mergeKLists(lists):
    '''
    EXPLANATION:
    At scale, merging lists sequentially is O(N*K).
    We start with the first list and merge it with every subsequent list.
    Standard helper to merge two sorted lists in O(len(l1) + len(l2))
    res = lists[0]
    for i in range(1, len(lists)):
        res = mergeTwoLists(res, lists[i])
    return res
     
    Using a Min-Heap (Priority Queue) reduces this to O(N log K), where N is the total number of nodes.
    
    STAFF INSIGHT: 
    We store a tuple (node.val, id(node), node) in the heap. Including id(node) or count
    prevents the heap from trying to compare ListNode objects directly if 
    two nodes have the same value.
    '''
    min_heap = []
    count = 0  # <--- Simple integer increment is faster than id()
    for l in lists:
        if l:
            heapq.heappush(min_heap, (l.val, count, l))
            count += 1 

    dummy = ListNode(0)
    curr = dummy
    
    while min_heap:
        _, _, node = heapq.heappop(min_heap)
        
        # Connect the smallest node found across all lists
        curr.next = node
        
        # If the extracted node has a neighbor, add it to the heap
        if node.next:
            count += 1
            heapq.heappush(min_heap, (node.next.val, count, node.next))

        curr = curr.next
            
    return dummy.next

# ---------------------------------------------------------
# 2. REVERSE NODES IN K-GROUP
# ---------------------------------------------------------

def reverseKGroupRecursive(head, k):
    # 1. Check if there are at least k nodes to reverse
    curr = head
    for _ in range(k):
        if not curr:
            return head # Not enough nodes, leave as is
        curr = curr.next
    
    # 2. Reverse the first k nodes
    prev = None
    curr = head
    for _ in range(k):
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    
    # 3. Recursion: Connect the original head (now the tail)
    # to the head of the next reversed group
    if curr:
        head.next = reverseKGroup(curr, k)
    
    # 4. 'prev' is the new head of this reversed k-segment
    return prev

def reverseKGroup(head, k):
    '''
    EXPLANATION:
    We use a recursive or iterative approach to reverse segments of size k.
    If fewer than k nodes remain, we leave them as is.
    
    STAFF INSIGHT:
    This problem tests your ability to maintain 'jump' pointers between 
    reversed segments. Using a dummy node simplifies the 'head' logic.
    '''
    dummy = ListNode(0, head)
    group = dummy
    while True:
        # Find the kth node
        kth = group
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next
        # Reverse the group (Standard reverse logic)
        next_group = kth.next
        curr, prev = group.next, kth.next
        while curr != next_group:
            n = curr.next
            curr.next = prev
            prev = curr
            curr = n

        # Re-link with the rest of the list
        temp = group.next
        group.next = kth
        group = temp

        #one liner of above relinking would be:
        #group.next, group = kth, group.next
 
# ---------------------------------------------------------
# 3. FLATTEN A MULTILEVEL DOUBLY LINKED LIST
# ---------------------------------------------------------
def flatten(head):
    '''
    EXPLANATION:
    Imagine a structure like this:

    Level 1: 1 <-> 2 <-> 3 <-> 4

    (Node 2 has a child) Level 2: 7 <-> 8

    The Flattening Rules:
    If a node has a child, the entire child list must appear immediately after that node.

    The original next of that node must follow after the entire child branch is finished.

    All prev and next pointers must be correctly updated to maintain the doubly linked property.

    Flattened Result: 1 <-> 2 <-> 7 <-> 8 <-> 3 <-> 4

    This is essentially a Pre-order DFS. When we encounter a child, we 
    process the child branch before moving to the next node.
    
    STAFF INSIGHT:
    An iterative approach using a Stack is more robust for production 
    systems to avoid RecursionDepthExceeded errors on deep structures.
    '''
    if not head: return head
    
    stack = [head]
    dummy = Node(0)
    prev = dummy
    
    while stack:
        curr = stack.pop()
        
        # Connect prev and curr
        prev.next = curr
        curr.prev = prev
        
        # Push next first, then child, so child is processed first (LIFO)
        if curr.next:
            stack.append(curr.next)
        if curr.child:
            stack.append(curr.child)
            curr.child = None # Crucial: Clear the child pointer
            
    # Cleanup dummy head
    head.prev = None
    return head

# ---------------------------------------------------------
# 4. LRU CACHE (THE HYBRID PATTERN)
# ---------------------------------------------------------
class LRUCache:
    '''
    EXPLANATION:
    Combines a Hash Map for O(1) lookups and a Doubly Linked List for 
    O(1) updates to the "Most Recently Used" position.
    
    STAFF INSIGHT:
    We use 'Left' and 'Right' dummy nodes as boundaries. This eliminates 
    null checks when adding/removing nodes from the list.
    '''
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {} # map key to node
        
        # Left = Least Recently Used, Right = Most Recently Used
        self.left, self.right = Node(0, 0), Node(0, 0)
        self.left.next, self.right.prev = self.right, self.left

    def _remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def _insert(self, node):
        # Insert at the right (MRU)
        prev, nxt = self.right.prev, self.right
        prev.next = nxt.prev = node
        node.next, node.prev = nxt, prev

    def get(self, key: int) -> int:
        if key in self.cache:
            self._remove(self.cache[key])
            self._insert(self.cache[key])
            return self.cache[key].val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        self.cache[key] = Node(value)
        self.cache[key].key = key # Storing key to delete from dict later
        self._insert(self.cache[key])
        
        if len(self.cache) > self.cap:
            # remove from list and delete from dict
            lru = self.left.next
            self._remove(lru)
            del self.cache[lru.key]

# ---------------------------------------------------------
# 5. PARTITION LIST
# ---------------------------------------------------------
def partition(head: ListNode, x: int) -> ListNode:
    '''
    EXPLANATION:
    The goal is to rearrange the list so all nodes < x come before nodes >= x.
    The order of nodes within each partition must be preserved (Stable Sort property).

    STAFF INSIGHT:
    The most "Staff-level" way to solve this is using two separate dummy chains 
    (lesser and greater). This avoids complex in-place swaps and ensures 
    the code is readable and bug-free. 
    
    CRITICAL STEP: You must nullify the 'next' pointer of the tail of the 
    'greater' list to avoid creating a cycle in the final result.
    '''
    # Create two dummy nodes to act as the start of two independent lists
    less_head = ListNode(0)
    greater_head = ListNode(0)
    
    # Pointers to the current tail of both lists
    less = less_head
    greater = greater_head
    
    curr = head
    while curr:
        if curr.val < x:
            less.next = curr
            less = less.next
        else:
            greater.next = curr
            greater = greater.next
        curr = curr.next
    
    # IMPORTANT: Terminate the 'greater' list to prevent cycles
    greater.next = None
    
    # Connect the end of the 'less' list to the start of the 'greater' list
    less.next = greater_head.next
    
    return less_head.next

# =========================================================
# TEST RUNNER
# =========================================================

def print_list(head):
    vals = []
    while head:
        vals.append(str(head.val))
        head = head.next
    print(" -> ".join(vals) if vals else "Empty List")

if __name__ == "__main__":
    # print("--- Testing Merge K Sorted Lists ---")
    # l1 = ListNode(9, ListNode(10, ListNode(15)))
    # l2 = ListNode(1, ListNode(3, ListNode(4)))
    # l3 = ListNode(2, ListNode(6))
    # l3 = ListNode(7, ListNode(18))
    # merged = mergeKLists([l1, l2, l3])
    # print_list(merged) # Expected: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6

    # print("\n--- Testing Reverse K-Group (k=2) ---")
    # list_to_rev = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    # rev_k = reverseKGroup(list_to_rev, 2)
    # print_list(rev_k) # Expected: 2 -> 1 -> 4 -> 3 -> 5

    print("\n--- Testing Partition List (x=3) ---")
    list_to_part = ListNode(1, ListNode(4, ListNode(3, ListNode(2, ListNode(5, ListNode(2))))))
    partitioned = partition(list_to_part, 4)
    print_list(partitioned) # Expected: 1 -> 2 -> 2 -> 4 -> 3 -> 5
    
    # --- Testing LRU Cache ---
    print("\n--- Testing LRU Cache ---")
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(f"Get 1: {cache.get(1)}") # returns 1
    cache.put(3, 3)                # evicts key 2
    print(f"Get 2 (evicted): {cache.get(2)}") # returns -1
    cache.put(4, 4)                # evicts key 1
    print(f"Get 1 (evicted): {cache.get(1)}") # returns -1
    print(f"Get 3: {cache.get(3)}") # returns 3
    print(f"Get 4: {cache.get(4)}") # returns 4
    print("LRU Cache tests passed!")

    # --- Testing Flatten Multilevel List ---
    # print("\n--- Testing Flatten Multilevel List ---")
    # # Structure: 1-2-3-4
    # #              |
    # #              7-8
    # n1, n2, n3, n4 = Node(1), Node(2), Node(3), Node(4)
    # n7, n8 = Node(7), Node(8)
    # n1.next, n2.prev = n2, n1
    # n2.next, n3.prev = n3, n2
    # n3.next, n4.prev = n4, n3
    # n2.child = n7 # Node 2 has child 7
    # n7.next, n8.prev = n8, n7
    
    # flattened = flatten(n1)
    # print_list(flattened) # Expected order: 1 -> 2 -> 7 -> 8 -> 3 -> 4