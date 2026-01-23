"""
Filename: prefix_sum_mastery.py
Focus: Mastering the Prefix Sum / Pre-computation pattern.
Key Idea: Pre-calculate cumulative data to answer range queries in O(1) time.
"""

# =============================================================================
# PATTERN: Prefix Sum & Pre-computation
# Logic: Build an auxiliary array or variable that stores cumulative results 
# (sum, product, or counts) up to index i.
# =============================================================================

def running_sum_1d(nums):
    """
    Problem: Range Sum Query (Immutable).
    Logic: sum(i, j) = prefix[j] - prefix[i-1]. 
    By pre-calculating the sum from index 0 to i, we answer any range sum in O(1).
    """
    prefix = [0] * (len(nums) + 1)
    for i in range(len(nums)):
        prefix[i+1] = prefix[i] + nums[i]
    
    # Example Query: sum of elements between index 1 and 3
    # return prefix[4] - prefix[1]
    return prefix

def product_except_self(nums):
    """
    Problem: Product of Array Except Self (without using division).
    Logic: For any index i, the result is (product of all elements to the left) 
    MULTIPLIED by (product of all elements to the right).
    We do two passes: one for prefix products, one for suffix products.
    """
    res = [1] * len(nums)
    
    # Pass 1: Prefix products (Left side)
    prefix = 1
    for i in range(len(nums)):
        res[i] = prefix
        prefix *= nums[i]
        
    # Pass 2: Suffix products (Right side)
    suffix = 1
    for i in range(len(nums) - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
        
    return res

def subarray_sum_equals_k(nums, k):
    """
    Problem: Count the total number of continuous subarrays whose sum equals k.
    Logic: Use a Hash Map to store (prefix_sum: frequency).
    If (current_sum - k) exists in the map, it means a subarray ending here sums to k.
    This is the 'Prefix Sum + Hash Map' optimization.
    """
    count = 0
    current_sum = 0
    # Base case: a prefix sum of 0 has been seen once (before the array starts)
    prefix_map = {0: 1}
    
    for n in nums:
        current_sum += n
        diff = current_sum - k
        
        # If (current_sum - target) was seen before, we found a valid subarray
        count += prefix_map.get(diff, 0)
        
        # Update map with the current prefix sum
        prefix_map[current_sum] = prefix_map.get(current_sum, 0) + 1
        
    return count

def find_pivot_index(nums):
    """
    Problem: Find the index where the sum of elements to the left == sum to the right.
    Logic: Total_Sum = Left_Sum + Pivot_Value + Right_Sum.
    Therefore: Right_Sum = Total_Sum - Left_Sum - nums[i].
    We just need to check if Left_Sum == Total_Sum - Left_Sum - nums[i].
    """
    total = sum(nums)
    left_sum = 0
    for i, x in enumerate(nums):
        if left_sum == (total - left_sum - x):
            return i
        left_sum += x
    return -1

def subarray_sums_divisible_by_k(nums, k):
    """
    Problem: Count subarrays with a sum divisible by k.
    Logic: If prefix_sum[i] % k == prefix_sum[j] % k, then the subarray 
    between i and j is divisible by k.
    """
    count = 0
    prefix_rem = 0
    # Map to store frequency of remainders
    rem_map = {0: 1}
    
    for n in nums:
        prefix_rem = (prefix_rem + n) % k
        # Handle negative remainders in Python to keep them in range [0, k-1]
        if prefix_rem < 0: prefix_rem += k
        
        count += rem_map.get(prefix_rem, 0)
        rem_map[prefix_rem] = rem_map.get(prefix_rem, 0) + 1
        
    return count

def range_addition(length, updates):
    """
    Problem: Apply multiple range increments [start, end, val] to an array.
    Logic: Difference Array. Instead of O(N) per update, mark start with +val 
    and end+1 with -val. The final array is the prefix sum of these marks.
    Complexity: O(Updates + N) instead of O(Updates * N).
    """
    res = [0] * length
    for start, end, val in updates:
        res[start] += val
        if end + 1 < length:
            res[end+1] -= val
            
    # Final pass to convert differences to actual values
    for i in range(1, length):
        res[i] += res[i-1]
    return res

# =============================================================================
# STAFF SIGNAL: 2D Prefix Sum (Bonus for Distributed Data)
# =============================================================================

def matrix_sum_query(matrix):
    """
    Problem: Range Sum Query 2D (Immutable).
    Logic: Sum of rectangle (r1, c1) to (r2, c2) is:
    Prefix[r2][c2] - Prefix[r1-1][c2] - Prefix[r2][c1-1] + Prefix[r1-1][c1-1]
    The overlapping area is added back.
    """
    if not matrix: return []
    rows, cols = len(matrix), len(matrix[0])
    p = [[0] * (cols + 1) for _ in range(rows + 1)]
    
    for r in range(rows):
        for c in range(cols):
            p[r+1][c+1] = matrix[r][c] + p[r][c+1] + p[r+1][c] - p[r][c]
            
    return p