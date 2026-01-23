"""
Filename: dutch_national_flag_mastery.py
Focus: Mastering 3-Way Partitioning (Dutch National Flag).
Key Idea: Use three pointers to maintain three sections: 
[0...low-1], [low...mid-1], and [high+1...n-1].
"""

# =============================================================================
# PATTERN: Dutch National Flag
# Logic: 
# 1. low: points to where the next '0' should go.
# 2. mid: the current element under examination.
# 3. high: points to where the next '2' should go.
# =============================================================================

def sort_colors(nums):
    """
    Problem: Sort an array with 0s, 1s, and 2s in-place (LeetCode 75).
    Logic: 
    - If nums[mid] == 0: swap with low, increment both low and mid.
    - If nums[mid] == 1: just increment mid (it's in the right place).
    - If nums[mid] == 2: swap with high, decrement high. Do NOT increment mid 
      yet because the new value swapped from high needs to be checked.
    """
    low, mid = 0, 0
    high = len(nums) - 1
    
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else: # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
    return nums



def partition_labels(s):
    """
    Problem: Partition string into as many parts as possible so that each 
    letter appears in at most one part.
    Logic: This is a variation of partitioning. Track the last occurrence 
    of every character. Use a pointer to track the end of the current partition.
    """
    last_occ = {char: i for i, char in enumerate(s)}
    
    res = []
    start, end = 0, 0
    for i, char in enumerate(s):
        end = max(end, last_occ[char])
        if i == end:
            res.append(i - start + 1)
            start = i + 1
    return res

def move_target_elements(nums, target):
    """
    Problem: Move all instances of 'target' to the middle, elements 
    smaller to the left, and larger to the right.
    Logic: Standard DNF partitioning with a dynamic pivot value.
    """
    low, mid = 0, 0
    high = len(nums) - 1
    
    while mid <= high:
        if nums[mid] < target:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == target:
            mid += 1
        else: # nums[mid] > target
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
    return nums

# =============================================================================
# STAFF SIGNAL: QuickSort Stability
# =============================================================================
# This pattern is the foundation for "3-Way QuickSort," which is 
# significantly more efficient than standard QuickSort when there 
# are many duplicate elements (O(N) instead of O(N log N)).