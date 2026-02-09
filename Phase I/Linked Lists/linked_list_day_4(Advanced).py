'''
DAY 4: ADVANCED STRUCTURES & PERFORMANCE OPTIMIZATION
1. SORT LIST (O(n log n) Time, O(1) Space)

THE CHALLENGE: Merge Sort on a Linked List is standard, but doing it in O(1) space requires a Bottom-Up Iterative approach.

STAFF LEVEL GOAL: Avoid recursion to prevent Stack Overflow on massive lists. Master the "Split" and "Merge" helper functions to handle sub-lists of sizes 1, 2, 4, 8...

KEY LOGIC: Use a dummy head and a "tail" pointer to stitch merged segments together in each pass.

2. LFU CACHE (LEAST FREQUENTLY USED)

THE CHALLENGE: Evict the item used least often. If frequencies are tied, evict the least recently used (LRU) among them.

STAFF LEVEL GOAL: Achieve O(1) for both get() and put().

DATA STRUCTURE: Use a HashMap to store nodes, and another HashMap where the Key is "Frequency" and the Value is a Doubly Linked List of all nodes with that frequency.

3. INTERSECTION OF TWO LINKED LISTS

THE CHALLENGE: Find the node where two lists converge.

STAFF LEVEL GOAL: Beyond the "Two-Pointer" solution, discuss the "Difference in Length" strategy.

SYSTEM DESIGN TWIST: How would you find the intersection if the lists are stored across different distributed shards? (Answer: Use a hash-based sampling or Bloom Filters).

4. ROTATE LIST (K PLACES)

THE CHALLENGE: Shift the list to the right by K positions.

STAFF LEVEL GOAL: Handle cases where K is much larger than N (K % N).

REFINEMENT: Connect the tail to the head to form a temporary ring, find the (N - K % N)-th node, set its next to null, and return the new head. This minimizes pointer re-assignments.

5. DESIGN BROWSER HISTORY

THE CHALLENGE: Implement 'visit(url)', 'back(steps)', and 'forward(steps)'.

STAFF LEVEL GOAL: Use a Doubly Linked List to represent the timeline.

TRADE-OFFS: Compare this to a Dynamic Array (ArrayList/Vector). Discuss why a Doubly Linked List is superior for frequent "visit" operations (deleting forward history) versus the memory locality benefits of an array.

STAFF-LEVEL ARCHITECTURAL QUESTIONS FOR TODAY:
CONCURRENCY: How would you implement a "Lock-Free" Linked List using Compare-And-Swap (CAS) operations?

MEMORY: How do Linked Lists interact with the CPU Cache? (Answer: Poorly, due to non-contiguous memory, leading to cache misses).

PERSISTENCE: If this list were mapped to a file on disk, how would you manage "pointers" (offsets)?


Problem	        Key Pattern	            Staff-Level Discussion Point
Sort List	    Divide & Conquer	    Why is QuickSort generally avoided for Linked Lists? (Answer: Sequential access vs. Random access).
LFU Cache	    Multi-level Mapping	    How do you handle "Frequency Ties"? (Usually fallback to LRU logic).
Intersection	Two-Pointer / Offset	What if the lists are stored in different databases?

'''

# =============================================================================
# DAY 4: LINKED LIST ADVANCED STRUCTURES & PERFORMANCE
# =============================================================================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Node: # Used for LFU Cache
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 1
        self.prev = None
        self.next = None

# -----------------------------------------------------------------------------
# 1. SORT LIST (O(n log n) Time, O(1) Space)
# Uses Bottom-Up (Iterative) Merge Sort to avoid recursion stack.
# -----------------------------------------------------------------------------
class Solution1:
# -----------------------------------------------------------------------------
    # BOTTOM-UP MERGE SORT (ITERATIVE)
    # Time: O(n log n) | Space: O(1)
    # Why Staff Level? It eliminates the O(log n) recursion stack, making it 
    # safe for extremely large lists that would otherwise cause a Stack Overflow.
    # -----------------------------------------------------------------------------
    def sortList(self, head: ListNode) -> ListNode:
        # Base case: empty or single-node lists are already sorted
        if not head or not head.next:
            return head
        
        # 1. Measure total length to determine how many 'step' passes we need
        length, curr = 0, head
        while curr:
            length += 1
            curr = curr.next
            
        # Sentinel node to handle head changes and simplify stitching
        dummy = ListNode(0, head)
        
        # 2. Outer Loop: Increase merge size exponentially (1, 2, 4, 8...)
        step = 1
        while step < length:
            # 'prev' tracks the end of the sorted portion
            # 'curr' tracks the start of the remaining unsorted portion
            prev, curr = dummy, dummy.next
            
            # 3. Inner Loop: Process the entire list in chunks of size 'step'
            while curr:
                # h1 is the head of the first sub-list
                h1 = curr
                # h2 is the head of the second sub-list, h1 is cut off at 'step'
                h2 = self.split(h1, step)
                # 'curr' becomes the head of the REST of the list, h2 is cut off
                curr = self.split(h2, step)
                
                # Merge the two isolated sub-lists and attach to the sorted end
                prev.next = self.merge(h1, h2)
                
                # Move 'prev' to the new end of the merged sub-list
                while prev.next:
                    prev = prev.next
            
            # Double the step size for the next pass
            step *= 2
            
        return dummy.next

    # Helper: Breaks the list after 'step' nodes and returns the next node
    # This 'isolates' sub-lists so the merge function doesn't bleed into the whole list
    def split(self, head, step):
        for i in range(step - 1):
            if not head: break
            head = head.next
        
        if not head: return None
        
        next_start = head.next
        head.next = None # Crucial: Sever the link to isolate the segment
        return next_start

    # Standard Two-Pointer Merge
    def merge(self, l1, l2):
        temp_dummy = ListNode(0)
        curr = temp_dummy
        while l1 and l2:
            if l1.val < l2.val:
                curr.next, l1 = l1, l1.next
            else:
                curr.next, l2 = l2, l2.next
            curr = curr.next
        curr.next = l1 or l2
        return temp_dummy.next

# -----------------------------------------------------------------------------
# 2. LFU CACHE (Least Frequently Used)
# O(1) Get and Put using Frequency Map + Doubly Linked Lists.
# -----------------------------------------------------------------------------
import collections

class DLinkedList:
    def __init__(self):
        self.sentinel = Node(None, None) # Dual Sentinel approach
        self.sentinel.next = self.sentinel.prev = self.sentinel
        self.size = 0

    def append(self, node):
        node.next = self.sentinel
        node.prev = self.sentinel.prev
        node.prev.next = node
        self.sentinel.prev = node
        self.size += 1

    def pop(self, node=None):
        if self.size == 0: return None
        if not node: node = self.sentinel.next
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        return node

class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.nodes = {} # key to Node
        self.freqs = collections.defaultdict(DLinkedList) # freq to DLinkedList
        self.min_freq = 0

    def _update(self, node):
        f = node.freq
        self.freqs[f].pop(node)
        if self.min_freq == f and self.freqs[f].size == 0:
            self.min_freq += 1
        node.freq += 1
        self.freqs[node.freq].append(node)

    def get(self, key: int) -> int:
        if key not in self.nodes: return -1
        node = self.nodes[key]
        self._update(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.cap == 0: return
        if key in self.nodes:
            node = self.nodes[key]
            node.value = value
            self._update(node)
        else:
            if len(self.nodes) == self.cap:
                node = self.freqs[self.min_freq].pop()
                del self.nodes[node.key]
            new_node = Node(key, value)
            self.nodes[key] = new_node
            self.freqs[1].append(new_node)
            self.min_freq = 1

# -----------------------------------------------------------------------------
# 3. INTERSECTION OF TWO LINKED LISTS
# Two-pointer approach (A+B = B+A)
# -----------------------------------------------------------------------------
class Solution3:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        if not headA or not headB: return None
        pA, pB = headA, headB
        while pA != pB:
            pA = pA.next if pA else headB
            pB = pB.next if pB else headA
        return pA

# -----------------------------------------------------------------------------
# 4. ROTATE LIST (K Places)
# Optimized for K > length
# -----------------------------------------------------------------------------
class Solution4:
    def rotateRight(self, head: ListNode, k: int) -> ListNode:
        if not head or not head.next or k == 0: return head
        
        # 1. Close the list into a ring and find length
        old_tail = head
        length = 1
        while old_tail.next:
            old_tail = old_tail.next
            length += 1
        old_tail.next = head
        
        # 2. Find new tail: (length - k % length - 1)th node
        # 3. New head is (length - k % length)th node
        new_tail = head
        for _ in range(length - (k % length) - 1):
            new_tail = new_tail.next
        
        new_head = new_tail.next
        new_tail.next = None # Break the ring
        
        return new_head
    
# -----------------------------------------------------------------------------
# ROTATE LEFT (K Places)
# Time: O(n) | Space: O(1)
# -----------------------------------------------------------------------------
class SolutionRotateLeft:
    def rotateLeft(self, head: ListNode, k: int) -> ListNode:
        if not head or not head.next or k == 0:
            return head
        
        # 1. Compute length and find the current tail
        old_tail = head
        length = 1
        while old_tail.next:
            old_tail = old_tail.next
            length += 1
            
        # 2. Normalize k (if k > length)
        k = k % length
        if k == 0:
            return head
            
        # 3. Connect tail to head to form a circular ring
        old_tail.next = head
        
        # 4. For Rotate Left, the new tail is k-1 steps from the original head
        # Example: 1->2->3->4->5, k=2. New head is 3. New tail is 2.
        new_tail = head
        for _ in range(k - 1):
            new_tail = new_tail.next
            
        # 5. The new head is the node after the new tail
        new_head = new_tail.next
        
        # 6. Break the ring
        new_tail.next = None
        
        return new_head
# -----------------------------------------------------------------------------
# 5. DESIGN BROWSER HISTORY
# Doubly Linked List for O(1) visit and O(Steps) traversal
# -----------------------------------------------------------------------------
class BrowserNode:
    def __init__(self, url: str):
        self.url = url
        self.prev = None
        self.next = None

class BrowserHistory:
    def __init__(self, homepage: str):
        self.curr = BrowserNode(homepage)

    def visit(self, url: str) -> None:
        new_page = BrowserNode(url)
        self.curr.next = new_page
        new_page.prev = self.curr
        self.curr = new_page # Forward history is deleted by moving curr

    def back(self, steps: int) -> str:
        while steps > 0 and self.curr.prev:
            self.curr = self.curr.prev
            steps -= 1
        return self.curr.url

    def forward(self, steps: int) -> str:
        while steps > 0 and self.curr.next:
            self.curr = self.curr.next
            steps -= 1
        return self.curr.url

# =============================================================================
# TEST RUNNER
# =============================================================================

def list_to_ll(arr):
    if not arr: return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def ll_to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def run_tests():
    print("--- Running Day 4 Tests ---")

    # Test 1: Sort List
    s1 = Solution1()
    l1 = list_to_ll([4, 2, 1, 3])
    sorted_l1 = s1.sortList(l1)
    print(f"1. Sort List: {ll_to_list(sorted_l1)} (Expected: [1, 2, 3, 4])")

    # Test 2: LFU Cache
    print("2. LFU Cache:", end=" ")
    lfu = LFUCache(2)
    lfu.put(1, 1)
    lfu.put(2, 2)
    res1 = lfu.get(1)       # returns 1, freq of 1 becomes 2
    lfu.put(3, 3)           # evicts key 2 (min_freq was 1)
    res2 = lfu.get(2)       # returns -1
    print(f"Get(1): {res1}, Get(2): {res2} (Expected: 1, -1)")

    # Test 3: Intersection
    s3 = Solution3()
    intersect = ListNode(8, ListNode(4, ListNode(5)))
    headA = ListNode(4, ListNode(1, intersect))
    headB = ListNode(5, ListNode(6, ListNode(1, intersect)))
    res3 = s3.getIntersectionNode(headA, headB)
    print(f"3. Intersection Node Val: {res3.val if res3 else 'None'} (Expected: 8)")

    # Test 4: Rotate List
    s4 = Solution4()
    l4 = list_to_ll([1, 2, 3, 4, 5])
    rotated = s4.rotateRight(l4, 2)
    print(f"4. Rotate List (k=2): {ll_to_list(rotated)} (Expected: [4, 5, 1, 2, 3])")

    # Test 5: Browser History
    print("5. Browser History:", end=" ")
    bh = BrowserHistory("leetcode.com")
    bh.visit("google.com")
    bh.visit("facebook.com")
    back1 = bh.back(1)    # google.com
    fwd1 = bh.forward(1)  # facebook.com
    print(f"Back: {back1}, Forward: {fwd1} (Expected: google.com, facebook.com)")

if __name__ == "__main__":
    run_tests()