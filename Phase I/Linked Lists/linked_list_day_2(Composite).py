'''
Day 2 Linked List Problems:

1. Linked List Cycle II (Find the Start of the Cycle)
2. Reorder List
3. Add Two Numbers
4. Copy List with Random Pointer
5. Palindrome Linked List
''' 

class ListNode:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random # Only used for Problem 4

def create_linked_list(arr):
    if not arr: return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

class LinkedListSolutions:
    """
    DAY 2: STAFF ENGINEER PREP - LINKED LIST PATTERNS
    Focus: O(1) Space Complexity and Composite Logic.
    """

    # 1. LINKED LIST CYCLE II (Floyd's Tortoise and Hare)
    # Why Staff Level: Requires understanding the mathematical offset 
    # between the meeting point and the cycle entry.
    '''                 a
    1 -> 2 -> 3 -> 4 -> 5 -> 6 ->  7
                     c /|\         |
                        |         \|/
                       12          8
                       /|\         |
                        |         \|/
                       11 <- 10 <- 9 b
    Why does the math work?

    Imagine the path is split into three segments:
    $a$: The distance from the Start to the Cycle Entrance. (1 -> 5) 
    $b$: The distance from the Cycle Entrance to the Meeting Point. ( 5-> 9)
    $c$: The distance from the Meeting Point back to the Cycle Entrance. ( 9-> 5)
    The total length of the actual circle is $b + c$.
                        
    The Hare traveled exactly twice as far as the Tortoise.
    Distance of Tortoise ($D_{t}$): $a + b$
    Distance of Hare ($D_{h}$): $a + b + c + b$ 
    (The hare went through $a$, through $b$, around the circle $c$, and back to $b$).
    a + 2b + c = 2(a + b)
    which leads to a = c

    '''
    def detectCycle(self, head: ListNode) -> ListNode:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                # Cycle detected. Reset one pointer to head.
                # Moving both at 1x speed will lead them to meet at the entry.
                ptr = head
                while ptr != slow:
                    ptr = ptr.next
                    slow = slow.next
                return ptr
        return None

    # 2. REORDER LIST (The "Triple Pattern" Problem)
    # Pattern: Find Middle -> Reverse Second Half -> Interleave
    '''
    Real-World Example
    Imagine a Undo/Redo Stack or a Task Scheduler where you want to 
    balance the oldest tasks with the newest tasks to ensure both "freshness" and "completion."

    You are given the head of a singly linked-list. The list can be represented as:

    L0 → L1 → … → Ln - 1 → Ln
    Reorder the list to be on the following form:

    L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …
    You may not modify the values in the list's nodes. Only nodes themselves may be changed.
    Example 1:
    Input: head = [1,2,3,4]
    Output: [1,4,2,3]

    Example2:
    Input: head = [1,2,3,4,5]
    Output: [1,5,2,4,3]
    After creating two lists from one
    first=[1, 2, 3], second=[5, 4]
    ===========iteration=0========
    t1, t2 = first.next, second.next; makes t1=[2, 3], t2=[4]
    first.next = second; makes first=[1, 5, 4], first.next=[5, 4]
    second.next = t1; makes second=[5, 2, 3], second.next=[2, 3]
    first, second = t1, t2; makes first=[2, 3], second=[4]
    Now new head=[1, 5, 2, 3]
    ===========iteration=1========
    t1, t2 = first.next, second.next; makes t1=[3], t2=[]
    first.next = second; makes first=[2, 4], first.next=[4]
    second.next = t1; makes second=[4, 3], second.next=[3]
    first, second = t1, t2; makes first=[3], second=[]
    Now new head=[1, 5, 2, 4, 3]
    '''
    def reorderList(self, head: ListNode) -> None:
        if not head or not head.next:
            return

        # PHASE 1: Find the middle (Standard Pattern)
        # For 1->2->3->4, slow will end at 2.
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # PHASE 2: Reverse the second half (Standard Pattern)
        # second starts at 3->4
        second = slow.next
        slow.next = None # Sever the connection! (Critical for Staff level)
        
        prev = None
        while second:
            tmp = second.next
            second.next = prev
            prev = second
            second = tmp
        # 'prev' is now the head of the reversed second half: 4->3

        # PHASE 3: Interleave (The "Zip" Pattern)
        # first: 1->2, second: 4->3
        first, second = head, prev
        while second:
            tmp1, tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first, second = tmp1, tmp2

    # 3. ADD TWO NUMBERS (Carry Logic)
    # Why Staff Level: Handling data streams of unequal length and carry-over.
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode(0)
        curr = dummy
        carry = 0
        while l1 or l2 or carry:
            val = (l1.val if l1 else 0) + (l2.val if l2 else 0) + carry
            carry = val // 10
            curr.next = ListNode(val % 10)
            curr = curr.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return dummy.next

    # 4. COPY LIST WITH RANDOM POINTER (Interweaving Pattern)
    # Why Staff Level: Solving in O(1) space instead of using a Hash Map.
    def copyRandomList(self, head: 'ListNode') -> 'ListNode':
        if not head: return None
        
        # A. Create interleaved nodes (A -> A' -> B -> B')
        curr = head
        while curr:
            new_node = ListNode(curr.val, curr.next)
            curr.next = new_node
            curr = new_node.next
            
        # B. Copy random pointers
        curr = head
        while curr:
            if curr.random:
                curr.next.random = curr.random.next
            curr = curr.next.next
            
        # C. Separate the two lists
        curr = head
        new_head = head.next
        while curr:
            copy = curr.next
            curr.next = copy.next
            if copy.next:
                copy.next = copy.next.next
            curr = curr.next
        return new_head

    # 5. PALINDROME LINKED LIST
    # Pattern: Reverse half and compare. 
    # Staff Tip: Mention restoring the list in interviews.
    def isPalindrome(self, head: ListNode) -> bool:
        # Step 1: Find middle
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # Step 2: Reverse second half
        prev, curr = None, slow
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
            
        # Step 3: Compare
        left, right = head, prev
        while right:
            if left.val != right.val: return False
            left = left.next
            right = right.next
        return True
    
    # --- TEST RUNNER ---
if __name__ == "__main__":
    solver = LinkedListSolutions()

    print("--- Test 1: Add Two Numbers (2-4-3 + 5-6-4) ---")
    l1 = create_linked_list([2, 4, 3])
    l2 = create_linked_list([5, 6, 4])
    result = solver.addTwoNumbers(l1, l2)
    print(f"Result: {to_list(result)} (Expected: [7, 0, 8])\n")

    print("--- Test 2: Reorder List [1, 2, 3, 4, 5] ---")
    l3 = create_linked_list([1, 2, 3, 4, 5, 6])
    solver.reorderList(l3)
    print(f"Result: {to_list(l3)} (Expected: [1, 5, 2, 4, 3])\n")

    print("--- Test 3: Detect Cycle ---")
    l4 = create_linked_list([3, 2, 0, -4])
    # Create manual cycle: -4 points back to 2
    l4.next.next.next.next = l4.next 
    cycle_node = solver.detectCycle(l4)
    print(f"Cycle Start Node Value: {cycle_node.val if cycle_node else 'None'} (Expected: 2)\n")

    print("--- Test 4: Copy List with Random Pointer ---")
    # Create a simple list: 1 -> 2 -> 3
    # with random pointers: 1->3, 2->1, 3->2
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node1.next = node2
    node2.next = node3
    node1.random = node3
    node2.random = node1
    node3.random = node2
    
    copied = solver.copyRandomList(node1)
    
    # Verify structure
    print(f"Original list values: {to_list(node1)} (Expected: [1, 2, 3])")
    print(f"Copied list values: {to_list(copied)} (Expected: [1, 2, 3])")
    
    # Verify random pointers are correctly copied
    print(f"Original node1.random.val: {node1.random.val} (Expected: 3)")
    print(f"Copied node1.random.val: {copied.random.val} (Expected: 3)")
    print(f"Original node2.random.val: {node1.next.random.val} (Expected: 1)")
    print(f"Copied node2.random.val: {copied.next.random.val} (Expected: 1)")
    print(f"Original node3.random.val: {node1.next.next.random.val} (Expected: 2)")
    print(f"Copied node3.random.val: {copied.next.next.random.val} (Expected: 2)")
    
    # Verify deep copy (different objects)
    print(f"Are they different objects? {node1 is not copied} (Expected: True)")
    print(f"Are their next nodes different? {node1.next is not copied.next} (Expected: True)\n")

    print("--- Test 5: Copy List with Random Pointer (Edge Case: None) ---")
    empty_copy = solver.copyRandomList(None)
    print(f"Copied None: {empty_copy} (Expected: None)\n")

    print("--- Test 6: Copy List with Random Pointer (Single Node) ---")
    single = ListNode(5)
    single.random = single
    single_copy = solver.copyRandomList(single)
    print(f"Copied single node value: {single_copy.val} (Expected: 5)")
    print(f"Single node random points to itself: {single_copy.random is single_copy} (Expected: True)\n")

    print("--- Test 7: Palindrome Check [1, 2, 2, 1] ---")
    l5 = create_linked_list([1, 2, 2, 1])
    print(f"Is Palindrome? {solver.isPalindrome(l5)} (Expected: True)\n")

    print("--- Test 8: Palindrome Check [1, 2, 3] ---")
    l6 = create_linked_list([1, 2, 3])
    print(f"Is Palindrome? {solver.isPalindrome(l6)} (Expected: False)")