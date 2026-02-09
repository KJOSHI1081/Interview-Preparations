"""
TOPIC: LINKED LISTS - DAY 1
    1. REVERSE A LINKED LIST
    2. DETECT A CYCLE
    3. MERGE TWO SORTED LISTS
    4. REMOVE N-th NODE FROM END
    5. MIDDLE OF THE LINKED LIST
5 Frequent Interview Questions & Solutions with Test Cases
"""

class ListNode:
    """Standard definition for a singly-linked list node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedListSolutions:
    
    # 1. REVERSE A LINKED LIST
    def reverseList(self, head: ListNode) -> ListNode:
        # In-place implementation
        prev = None
        curr = head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        return prev 

        #recursion with single pointer
            # if not head or not head.next: return head

            # new_head = self.reverseList(head.next)
            # head.next.next = head
            # head.next = None
            # return new_head

        #recursion with two pointer head & tail
        # Helper function that carries the pointers through the recursion
        def reverse(curr, prev):
            # Base Case: We reached the end of the original list
            if not curr:
                return prev
            
            # Save the next node before we overwrite curr.next
            next_node = curr.next
            
            # The actual reversal: Point backwards
            curr.next = prev
            
            # Move forward: 
            # The old 'next_node' becomes the new 'curr'
            # The 'curr' we just processed becomes the new 'prev'
            return reverse(next_node, curr)

        # Initially, 'head' is curr, and its 'prev' should be None
        return reverse(head, None)

    # 2. DETECT A CYCLE
    def hasCycle(self, head: ListNode) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

    # 3. MERGE TWO SORTED LISTS
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode()
        tail = dummy
        while l1 and l2:
            if l1.val < l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        tail.next = l1 if l1 else l2
        return dummy.next

    # 4. REMOVE N-th NODE FROM END
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        dummy = ListNode(0, head)
        slow = fast = dummy
        for _ in range(n + 1):
            fast = fast.next
        while fast:
            slow = slow.next
            fast = fast.next
        slow.next = slow.next.next
        return dummy.next

    # 5. MIDDLE OF THE LINKED LIST
    def middleNode(self, head: ListNode) -> ListNode:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

# --- HELPER FUNCTIONS FOR TESTING ---

def list_to_linkedlist(arr):
    if not arr: return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def linkedlist_to_list(head):
    result = []
    curr = head
    while curr:
        result.append(curr.val)
        curr = curr.next
    return result

# --- MAIN EXECUTION BLOCK ---

if __name__ == "__main__":
    sol = LinkedListSolutions()
    
    print("--- 1. Reverse Linked List ---")
    ll1 = list_to_linkedlist([1, 2, 3, 4, 5])
    reversed_ll = sol.reverseList(ll1)
    print(f"Input: [1,2,3,4,5] -> Output: {linkedlist_to_list(reversed_ll)}")

    print("\n--- 2. Detect Cycle ---")
    ll2 = list_to_linkedlist([3, 2, 0, -4])
    # Manually creating a cycle: -4 points back to 2
    ll2.next.next.next.next = ll2.next 
    print(f"Cycle detected: {sol.hasCycle(ll2)}")

    print("\n--- 3. Merge Two Sorted Lists ---")
    l_a = list_to_linkedlist([1, 2, 4])
    l_b = list_to_linkedlist([1, 3, 4])
    merged = sol.mergeTwoLists(l_a, l_b)
    print(f"Merged [1,2,4] & [1,3,4] -> {linkedlist_to_list(merged)}")

    print("\n--- 4. Remove 2nd Node From End ---")
    ll4 = list_to_linkedlist([1, 2, 3, 4, 5])
    removed = sol.removeNthFromEnd(ll4, 2)
    print(f"Removing 2nd from end of [1,2,3,4,5] -> {linkedlist_to_list(removed)}")

    print("\n--- 5. Find Middle Node ---")
    ll5 = list_to_linkedlist([1, 2, 3, 4, 5, 6])
    mid = sol.middleNode(ll5)
    print(f"Middle of [1,2,3,4,5,6] is node with value: {mid.val}")