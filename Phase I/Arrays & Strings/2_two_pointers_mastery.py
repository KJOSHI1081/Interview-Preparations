"""
Filename: two_pointers_mastery.py
Focus: Mastering the Two Pointers pattern (Converging, Fast/Slow, and Slow Runner).
"""

# =============================================================================
# CATEGORY A: Converging Pointers (Outside-In)
# Logic: Start at both ends and move toward the center based on conditions.
# =============================================================================

def two_sum_ii(numbers, target):
    """
    Problem: Find two numbers in a sorted array that add up to a specific target.
    Logic: Use two pointers at ends. If sum > target, move right inward (smaller). 
    If sum < target, move left inward (larger).
    """
    l, r = 0, len(numbers) - 1
    while l < r:
        cur = numbers[l] + numbers[r]
        if cur == target:
            return [l + 1, r + 1]
        if cur < target:
            l += 1
        else:
            r -= 1
    return []

def is_palindrome(s):
    """
    Problem: Determine if string is a palindrome (alphanumeric only, ignore case).
    Logic: Move pointers inward, skipping non-alphanumeric chars, and compare.
    """
    l, r = 0, len(s) - 1
    while l < r:
        while l < r and not s[l].isalnum(): l += 1
        while l < r and not s[r].isalnum(): r -= 1
        if s[l].lower() != s[r].lower():
            return False
        l, r = l + 1, r - 1
    return True

def longest_palindrome(s: str) -> str:
    if not s: return ""
    
    def get_palindrome(left, right):
        # Expand as long as characters match and we are within bounds
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Return the valid palindrome found (adjusting for the final decrement/increment)
        return s[left + 1:right]

    ans = ""
    for i in range(len(s)):
        # Case 1: Odd length (center is a character like 'aba')
        p1 = get_palindrome(i, i)
        # Case 2: Even length (center is between characters like 'abba')
        p2 = get_palindrome(i, i + 1)
        
        # Keep the longest one found so far
        ans = max(ans, p1, p2, key=len)
        
    return ans

def max_area(height):
    """
    Problem: Container With Most Water.
    Logic: Area = width * min(height[l], height[r]). To find more area, 
    always move the pointer pointing to the shorter bar.
    """
    l, r, area = 0, len(height) - 1, 0
    while l < r:
        width = r - l
        current_area = min(height[l], height[r]) * width
        area = max(area, current_area)
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return area

def three_sum(nums):
    """
    Problem: Find all unique triplets that sum to zero.
    Logic: Sort array, iterate through and fix 'a', then use Two Sum (Converging) 
    for the remaining two values. Skip duplicate values to ensure uniqueness.
    """
    nums.sort()
    res = []
    for i, a in enumerate(nums):
        if i > 0 and a == nums[i-1]: continue # Skip duplicate 'a'
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = a + nums[l] + nums[r]
            if s > 0:
                r -= 1
            elif s < 0:
                l += 1
            else:
                res.append([a, nums[l], nums[r]])
                l += 1
                while l < r and nums[l] == nums[l-1]: l += 1 # Skip duplicate 'b'
    return res

def trap(height):
    """
    Problem: Trapping Rain Water.
    Logic: Water trapped at index i is min(max_left, max_right) - height[i].
    Use two pointers to maintain running maxes from both sides.
    """
    if not height: return 0
    l, r = 0, len(height) - 1
    l_max, r_max = height[l], height[r]
    res = 0
    while l < r:
        if l_max < r_max:
            l += 1
            l_max = max(l_max, height[l])
            res += l_max - height[l]
        else:
            r -= 1
            r_max = max(r_max, height[r])
            res += r_max - height[r]
    return res


# =============================================================================
# CATEGORY B: Fast & Slow Pointers (Cycle Detection)
# Logic: Pointers move at different speeds to find loops or midpoints.
# =============================================================================

def has_cycle(head):
    """
    Problem: Check if a linked list has a cycle.
    Logic: Fast moves 2 steps, slow moves 1. If they meet, there is a cycle.
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

def find_duplicate(nums):
    """
    Problem: Find the duplicate number in array of n+1 integers.
    Logic: Treat array values as pointers (index -> value). Use Floyd's 
    Cycle-Finding to find meeting point, then find entry of cycle.
    """
    slow = fast = 0
    # Phase 1: Find intersection point
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast: break
    
    # Phase 2: Find entrance to cycle (the duplicate)
    slow2 = 0
    while True:
        slow = nums[slow]
        slow2 = nums[slow2]
        if slow == slow2:
            return slow

def middle_node(head):
    """
    Problem: Return middle node of Linked List.
    Logic: When fast reaches end, slow is at the halfway mark.
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


# =============================================================================
# CATEGORY C: Same Direction (Slow Runner)
# Logic: Use a slow pointer to track the "valid" boundary for in-place updates.
# =============================================================================

def remove_duplicates(nums):
    """
    Problem: Remove duplicates from sorted array in-place.
    Logic: 'l' tracks where the next unique element should be placed.
    """
    if not nums: return 0
    l = 1
    for r in range(1, len(nums)):
        if nums[r] != nums[r-1]:
            nums[l] = nums[r]
            l += 1
    return l

def move_zeroes(nums):
    """
    Problem: Move all 0s to end, maintaining relative order.
    Logic: 'l' tracks the position of the next non-zero element. 
    Swap when r finds a non-zero.
    """
    l = 0
    for r in range(len(nums)):
        if nums[r] != 0:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
    return nums