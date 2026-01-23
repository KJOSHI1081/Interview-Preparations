"""
Filename: cyclic_sort_mastery.py
Focus: Mastering the Cyclic Sort pattern.
Key Idea: If an array contains numbers from 1 to n (or 0 to n), we can 
place each number at its correct index (i.e., value 'i' at index 'i-1').
"""

# =============================================================================
# PATTERN: Cyclic Sort
# Logic: Iterate through the array. While the current number is not at its 
# correct index, swap it with the number at its target index.
# =============================================================================

def cyclic_sort(nums):
    """
    Problem: Sort an array containing numbers from 1 to n in O(n) time.
    Logic: Value 'n' belongs at index 'n-1'.
    """
    i = 0
    while i < len(nums):
        # The correct index for nums[i] should be nums[i] - 1
        correct_idx = nums[i] - 1
        if nums[i] != nums[correct_idx]:
            # Swap to put the number in its rightful place
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
        else:
            i += 1
    return nums

def find_missing_number(nums):
    """
    Problem: Array contains n distinct numbers in range [0, n]. Find the missing one.
    Logic: Value 'i' belongs at index 'i'. After sorting, the first index 
    where nums[i] != i is the missing number.
    """
    i, n = 0, len(nums)
    while i < n:
        correct_idx = nums[i]
        # Range check: value 'n' has no index in an array of size n
        if nums[i] < n and nums[i] != nums[correct_idx]:
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
        else:
            i += 1
            
    # Find the missing number
    for i in range(n):
        if nums[i] != i:
            return i
    return n

def find_all_duplicates(nums):
    """
    Problem: Array of n integers where 1 <= nums[i] <= n. Some appear twice.
    Logic: Perform cyclic sort. Any number not at its correct index 
    after sorting is a duplicate.
    """
    i = 0
    while i < len(nums):
        correct_idx = nums[i] - 1
        if nums[i] != nums[correct_idx]:
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
        else:
            i += 1
            
    duplicates = []
    for i in range(len(nums)):
        if nums[i] != i + 1:
            duplicates.append(nums[i])
    return duplicates

def find_first_missing_positive(nums):
    """
    Problem: Find the smallest missing positive integer (Hard).
    Logic: Similar to cyclic sort, but ignore non-positive numbers 
    and numbers greater than the array length.
    """
    i, n = 0, len(nums)
    while i < n:
        correct_idx = nums[i] - 1
        # Only swap if the number is in range [1, n]
        if 0 < nums[i] <= n and nums[i] != nums[correct_idx]:
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
        else:
            i += 1
            
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1

def find_corrupt_pair(nums):
    """
    Problem: One number from [1, n] was replaced by another (Duplicate + Missing).
    Logic: After cyclic sort, index 'i' will contain the duplicate, 
    and the number that SHOULD have been there (i+1) is the missing one.
    """
    i = 0
    while i < len(nums):
        correct_idx = nums[i] - 1
        if nums[i] != nums[correct_idx]:
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
        else:
            i += 1
            
    for i in range(len(nums)):
        if nums[i] != i + 1:
            return {"duplicate": nums[i], "missing": i + 1}
    return None

# =============================================================================
# STAFF SIGNAL: O(1) Space Constraint
# =============================================================================
# Interviewers love this pattern because it proves you can manipulate 
# pointers and indices to save memory, which is critical in systems
# where you cannot afford an extra O(N) Hash Set.