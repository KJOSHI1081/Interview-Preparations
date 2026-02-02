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
    560. Subarray Sum Equals K 
    Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.

    A subarray is a contiguous non-empty sequence of elements within an array. 

    Problem: Count the total number of continuous subarrays whose sum equals k.
    Logic: Use a Hash Map to store (prefix_sum: frequency).
    If (current_sum - k) exists in the map, it means a subarray ending here sums to k.
    This is the 'Prefix Sum + Hash Map' optimization.

    NOTE: THIS is very tempting problem to use sliding window, however the window will remain broken
          forever if we find -ve or 0s. That is why prefix sum map is the ideal way to solve it.
    Example 1:

    Input: nums = [1,1,1], k = 2
    Output: 2
    Example 2:

    Input: nums = [1,2,3], k = 3
    Output: 2 
        ix num curr_sum diff prefix_map(before) prefix_map(after)           count
        0  1   1        -2   {0: 1}             {0: 1, 1: 1}                 0 
        1  2   3        1    {0: 1, 1: 1}       {0: 1, 1: 1, 3: 1}           1
        2  3   6        3    {0: 1, 1: 1, 3: 1} {0: 1, 1: 1, 3: 1, 6: 1}     2
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


def find_max_length(nums, k): 
    '''
    525. Contiguous Array
    Given a binary array nums, return the maximum length of a contiguous subarray with an equal number of 0 and 1.
    Example 1:

    Input: nums = [0,1]
    Output: 2
    Explanation: [0, 1] is the longest contiguous subarray with an equal number of 0 and 1.
    Flipping 0 to -1 is the "Aha!" moment for this problem.
    By making that change, the problem transforms from "finding equal counts" to 
    "finding the longest subarray that sums to 0."
    '''
    max_length = 0
    curr_sum = 0
    # Key: Prefix Sum, Value: First index where this sum occurred
    # We initialize with {0: -1} to handle subarrays starting at index 0
    prefix_map = {0: -1}

    for i, n in enumerate(nums):
        curr_sum += 1 if n == 1 else -1
        if curr_sum in prefix_map:
            max_length = max(max_length, i - prefix_map[curr_sum])
        else:
            prefix_map[curr_sum] = i
    
    return max_length


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

def subarray_sums_divisible_by_k(nums, k, sub_arr=True):
    """
    974. Subarray Sums Divisible by K
    Problem: Count subarrays with a sum divisible by k.
        Given an integer array nums and an integer k, return the number of 
        non-empty subarrays that have a sum divisible by k. 
        A subarray is a contiguous part of an array. 

    Example 1: 
    Input: nums = [4,5,0,-2,-3,1], k = 5
    Output: 7
    Explanation: There are 7 subarrays with a sum divisible by k = 5:
    [4, 5, 0, -2, -3, 1], [5], [5, 0], [5, 0, -2, -3], [0], [0, -2, -3], [-2, -3]

    Example 2: 
    Input: nums = [5], k = 9
    Output: 0

    Logic: If prefix_sum[i] % k == prefix_sum[j] % k, then the subarray  between i and j is divisible by k.
    """
    # There are only k possible remainders (0 to k-1)
    # count_map[rem] stores how many times we've seen remainder 'rem'

    if sub_arr:
        from collections import defaultdict
        rem_map = defaultdict(list)
        rem_map[0] = [-1]
        results = []
        curr_sum = 0
        for i, num in enumerate(nums):
            curr_sum += num
            rem = curr_sum % k
            if rem in rem_map:
                for ix in rem_map[rem]:
                    results.append(nums[ix + 1: i + 1]) 
            rem_map[rem].append(i)
        return len(results)


    count_map = [0] * k
    count_map[0] = 1  # Base case: a sum of 0 is divisible by k
    
    curr_sum = 0
    total_subarrays = 0
    
    for n in nums:
        curr_sum += n
        remainder = curr_sum % k
        
        # In Python % k is always 0 to k-1, even for negatives.
        # In Java/C++, use: remainder = (curr_sum % k + k) % k
        
        # Every time we see the same remainder, it pairs with 
        # ALL previous instances to form valid subarrays.
        total_subarrays += count_map[remainder]
        
        # Update the map for future indices
        count_map[remainder] += 1
            
    return total_subarrays



def range_addition(length, updates):
    """
    LeetCode 370 (Range Addition)
    Problem: 
        You are given an array of length n, initialized with all zeros. 
        You are also given a list of updates, where each update is [start_index, end_index, increment]. 
        You need to return the final state of the array after all updates are applied.
        Apply multiple range increments [start, end, val] to an array.

    Input: n = 5, updates = [[1, 3, 2]]
    Result: [0, 2, 2, 2, 0]
    Explanation:
    Step	    Index 0	Index 1	Index 2	Index 3	Index 4	Index 5 (out)
    Initial	    0	    0	    0	    0	    0	    -
    Marking	    0	    +2	    0	    0	    -2	    -
    Prefix Sum	0	    2	    2	    2	    0	    -

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

def range_additon_ii(m, n, ops, using_prefix_sum=True):
    '''
    598. Range Addition II

    Problem: You are given an m x n matrix M initialized with all 0's and an array of operations ops, 
    where ops[i] = [ai, bi] means M[x][y] should be incremented by one for all 0 <= x < ai and 0 <= y < bi.

    Count and return the number of maximum integers in the matrix after performing all the operations.

    Input: m = 3, n = 3, ops = [[2,2],[3,3]]
    Output: 4
    Explanation: The maximum integer in M is 2, and there are four of it in M. So return 4.

    '''

    #approach 1 (Prefix Sum):
    '''
    Imagine an operation [2, 2] on a 4x4 grid
    Phase 1: 
    Marking the 4 Corners The markers act as "instructions" for the prefix sum:
    [ +1,  0, -1,  0 ]
    [  0,  0,  0,  0 ]
    [ -1,  0, +1,  0 ]
    [  0,  0,  0,  0 ]

    Phase 2: 
    The 2D Prefix Sum Pass As the algorithm moves row by row and column by column,
    the +1 from (0,0) is added to every cell. When it hits the -1 at (0,2),
    it cancels out the "flow" for the rest of that row.
    When it hits the -1 at (2,0), it cancels the "flow" for the rest of the column.
    [ 1, 1, 0, 0 ]
    [ 1, 1, 0, 0 ]
    [ 0, 0, 0, 0 ]
    [ 0, 0, 0, 0 ]
    The prefix sum in this probelm is overkill but it's good for 2D matrix prefix sum understanding.
    '''

    
    if not ops: return m*n

    
    if not using_prefix_sum: 
        min_a, min_b = m, n
        for a, b in ops:
            min_a = min(min_a, a)
            min_b = min(min_b, b)
        
        return min_a * min_b
    
    grid = [[0]*n for _ in range(m)]
    diff = [[0]*(n+1) for _ in range(m + 1)]
    count = 0
    max_val = 0
    for a, b in ops:
        r1, c1 = 0, 0
        r2, c2 = a - 1, b - 1
        diff[r1][c1] += 1
        if c2 + 1 < n:
            diff[r1][c2+1] -= 1
        if r2 + 1 < m:
            diff[r2 + 1][c1] -= 1
        if c2 + 1 < n and r2 + 1 < m:
            diff[r2 + 1][c2 + 1] += 1
    for r in range(m):
        for c in range(n):
            val = diff[r][c]
            if r > 0: val += grid[r-1][c]
            if c > 0: val += grid[r][c - 1]
            if r > 0 and c > 0: val += grid[r-1][c - 1]
            grid[r][c] = val
            if grid[r][c] > max_val:
                max_val = grid[r][c]
                count = 1
            elif grid[r][c] == max_val:
                count += 1
    return count
 
# =============================================================================
# STAFF SIGNAL: 2D Prefix Sum (Bonus for Distributed Data)
# =============================================================================

def matrix_sum_query(matrix, row1: int, col1: int, row2: int, col2: int):
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
            #current value + top + left - topleft (remove the overlap)
            p[r+1][c+1] = matrix[r][c] + p[r][c+1] + p[r+1][c] - p[r][c]
    #Range Sum: TopLeft + BottomRight - Top - Left (compensation)
    return (p[row1][col1] + p[row2 + 1][col2 + 1] - p[row1][col2 + 1] - p[row2 + 1][col1])