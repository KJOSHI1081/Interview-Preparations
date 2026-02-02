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
    Problem: 75. Sort Colors
    
    Given an array nums with n objects colored red, white, or blue, sort them in-place 
    so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

    We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

    You must solve this problem without using the library's sort function.
    Sort an array with 0s, 1s, and 2s in-place (LeetCode 75).
    
    Example 1:

    Input: nums = [2,0,2,1,1,0]
    Output: [0,0,1,1,2,2]
    Example 2:

    Input: nums = [2,0,1]
    Output: [0,1,2]
    
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
    LeetCode #763: Partition Labels.
    Problem: 
    You are given a string s. We want to partition the string into as many parts as possible
      so that each letter appears in at most one part. For example, the string "ababcc" 
      can be partitioned into ["abab", "cc"], but partitions such as ["aba", "bcc"] or ["ab", "ab", "cc"] are invalid.

    Note that the partition is done so that after concatenating all the parts in order, the resultant string should be s.
    Return a list of integers representing the size of these parts.
    
    Example 1:
    Input: s = "ababcbacadefegdehijhklij"
    Output: [9,7,8]
    Explanation:
    The partition is "ababcbaca", "defegde", "hijhklij".
    This is a partition so that each letter appears in at most one part.
    A partition like "ababcbacadefegde", "hijhklij" is incorrect, because it splits s into less parts.
    
    Example 2:
    Input: s = "eccbbbbdec"
    Output: [10]
    
    Partition string into as many parts as possible so that each 
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

def move_zeros(nums: list[int]) -> None:
    '''
    283. Move Zeroes
    Given an integer array nums, move all 0's to the end of it while 
    maintaining the relative order of the non-zero elements.

    Note that you must do this in-place without making a copy of the array.
    Debug Trace: nums = [0, 1, 0, 3, 12]
    Step fastindex nums[fast] Action                            slowindex   Array State (after step)
    0     0        0          Target found! Do nothing.         0           [0, 1, 0, 3, 12]
    1     1        1          Non-zero! Swap nums[0], nums[1]   1           [1, 0, 0, 3, 12]
    2     2        0          Target found! Do nothing.         1           [1, 0, 0, 3, 12]
    3     3        3          Non-zero! Swap nums[1], nums[3]   2           [1, 3, 0, 0, 12]
    4     4        12         Non-zero! Swap nums[2], nums[4]   3           [1, 3, 12, 0, 0]
    '''
    # 'slow' is our "Write Pointer" - it marks where the next non-zero goes
    slow = 0
    
    # 'fast' is our "Read Pointer" - it explores the array
    for fast in range(len(nums)):
        # If we find a non-zero element...
        if nums[fast] != 0:
            # Swap it with the 'slow' pointer's position
            nums[slow], nums[fast] = nums[fast], nums[slow]
            
            # Move 'slow' forward to the next available slot
            slow += 1


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