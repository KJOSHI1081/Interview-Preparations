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

def find_missing_number(nums, using_cyclic_sort=True):
    """
    268. Missing Number
    Problem: Array contains n distinct numbers in range [0, n]. Find the missing one.

    Given an array nums containing n distinct numbers in the range [0, n], return the 
    only number in the range that is missing from the array.

    Logic: Value 'i' belongs at index 'i'. After sorting, the first index 
    where nums[i] != i is the missing number.
    
    Example 1:
    Input: nums = [3,0,1]
    Output: 2
    Explanation:
    n = 3 since there are 3 numbers, so all numbers are in the range [0,3]. 
    2 is the missing number in the range since it does not appear in nums.

    Example 2:
    Input: nums = [0,1]
    Output: 2
    Explanation:
    n = 2 since there are 2 numbers, so all numbers are in the range [0,2]. 
    2 is the missing number in the range since it does not appear in nums.

    Example 3:
    Input: nums = [9,6,4,2,3,5,7,0,1]
    Output: 8
    Explanation:
    n = 9 since there are 9 numbers, so all numbers are in the range [0,9]. 
    8 is the missing number in the range since it does not appear in nums.

    """

    if not using_cyclic_sort:
        n = len(nums) + 1
        total = sum(nums)
        expected_toal = (n * n - 1) // 2
        return expected_toal - total

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
    442. Find All Duplicates in an Array
    Given an integer array nums of length n where all the integers of nums are in the range [1, n] and each integer appears at most twice, return an array of all the integers that appears twice.

    You must write an algorithm that runs in O(n) time and uses only constant auxiliary space, excluding the space needed to store the output
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
    41. First Missing Positive
    
    Given an unsorted integer array nums. Return the smallest positive integer that is not present in nums.

    You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space. 
        
    Example 1:

    Input: nums = [1,2,0]
    Output: 3
    Explanation: The numbers in the range [1,2] are all in the array.
    Example 2:

    Input: nums = [3,4,-1,1]
    Output: 2
    Explanation: 1 is in the array but 2 is missing.
    Example 3:

    Input: nums = [7,8,9,11,12]
    Output: 1
    Explanation: The smallest positive integer 1 is missing.

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