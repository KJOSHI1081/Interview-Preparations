"""
BINARY SEARCH INTERVIEW CHEAT SHEET
Contains all 7 major interview patterns with explanations.
"""

import math
from typing import List


# ---------------------------------------------------------
# 1. STANDARD SEARCH (Exact Match)
# LeetCode #704: Binary Search
# Goal: Find the index of a target in a unique, sorted array.
# ---------------------------------------------------------
def standard_binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

'''
744. Find Smallest Letter Greater Than Target

You are given an array of characters letters that is sorted in non-decreasing order, 
and a character target. There are at least two different characters in letters.

Return the smallest character in letters that is lexicographically greater than target.
 If such a character does not exist, return the first character in letters.
 
Example 1:

Input: letters = ["c","f","j"], target = "a"
Output: "c"
Explanation: The smallest character that is lexicographically greater than 'a' in letters is 'c'.
Example 2:

Input: letters = ["c","f","j"], target = "c"
Output: "f"
Explanation: The smallest character that is lexicographically greater than 'c' in letters is 'f'.
Example 3:

Input: letters = ["x","x","y","y"], target = "z"
Output: "x"
Explanation: There are no characters in letters that is lexicographically greater than 'z' so we return letters[0].
  
Constraints:

2 <= letters.length <= 104
letters[i] is a lowercase English letter.
letters is sorted in non-decreasing order.
letters contains at least two different characters.
target is a lowercase English letter.

'''
def nextGreatestLetter(letters: List[str], target: str) -> str:
    l, r = 0, len(letters) - 1

    while l <=  r:
        mid = l + (r - l) // 2 
        if letters[mid] <= target:
            l = mid + 1
        else:
            r = mid - 1
            
    return letters[l % len(letters)]
        


'''
Problem 702: Search in a Sorted Array of Unknown Size.
While this is a Premium problem on LeetCode, 
it is widely known in interview preparation as the "Infinite Array" problem

Since you don't know the array's length, 
you cannot set an initial right boundary. 
You must find it yourself using Exponential Search: 
Find Bounds: Start with a range of size 2 (e.g., low = 0, high = 1).
 While the target is greater than the value at high, double the range (e.g., high = high * 2).
Binary Search: Once the target is within the [low, high] 
range, perform a standard binary search.
'''

def search_element_in_infinite_array(nums, target):
    l, r = 0, 1
    while nums[r] < target:
        l = r
        r *= 2
    
    while l <= r:
        mid = l + (r - l)//2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            l = mid + 1
        else:
            r = mid - 1
    
    return -1

'''
852. Peak Index in a Mountain Array aka bitonic

You are given an integer mountain array arr of 
length n where the values increase to a peak element and then decrease.

Return the index of the peak element.

Your task is to solve it in O(log(n)) time complexity.
 
'''
def peakIndexInMountainArray(self, arr: List[int]) -> int:
    l , r = 0, len(arr) - 1
    while l < r:
        m = l + (r - l) // 2
        if arr[m] < arr[m + 1]:
            l = m + 1
        else:
            r = m
    return l


# ---------------------------------------------------------
# 2. BINARY SEARCH ON PEAKS (Unsorted-ish)
# LeetCode #162: Find Peak Element
# Goal: Find an element that is strictly greater than its neighbors.
# ---------------------------------------------------------
def find_peak_element(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1 # Climbing up, peak is to the right
        else:
            right = mid # Going down, mid could be the peak
    return left


'''
1095. Find in Mountain Array

You may recall that an array arr is a mountain array if and only if:

arr.length >= 3
There exists some i with 0 < i < arr.length - 1 such that:
arr[0] < arr[1] < ... < arr[i - 1] < arr[i]
arr[i] > arr[i + 1] > ... > arr[arr.length - 1]
Given a mountain array mountainArr, return the minimum index such that mountainArr.get(index) == target. If such an index does not exist, return -1.

You cannot access the mountain array directly. You may only access the array using a MountainArray interface:

MountainArray.get(k) returns the element of the array at index k (0-indexed).
MountainArray.length() returns the length of the array.
Submissions making more than 100 calls to MountainArray.get will be judged Wrong Answer. Also, any solutions that attempt to circumvent the judge will result in disqualification.


Example 1:

Input: mountainArr = [1,2,3,4,5,3,1], target = 3
Output: 2
Explanation: 3 exists in the array, at index=2 and index=5. Return the minimum index, which is 2.
Example 2:

Input: mountainArr = [0,1,2,4,2,1], target = 3
Output: -1
Explanation: 3 does not exist in the array, so we return -1.
 

Constraints:

3 <= mountainArr.length() <= 104
0 <= target <= 109
0 <= mountainArr.get(index) <= 109

'''
def findInMountainArray(target: int, mountainArr: 'MountainArray') -> int:
    def findPeak(nums):
        l, r = 0, nums.length() - 1
        while l < r:
            m = l + (r - l) // 2
            if nums.get(m) < nums.get(m + 1):
                l = m + 1
            else:
                r = m
        return l

    def orderAgnosticBinarySearch(nums, target, start, end, is_ascending):
        l, r = start, end
        while l <= r:
            m = l + (r -l) // 2
            val = nums.get(m)
            if val == target:
                return m
            if is_ascending:
                if val < target: l = m + 1
                else: r = m - 1
            else:
                # On descending side: if value is LESS than target,
                # we need to go LEFT (towards larger numbers)
                if val < target: r = m - 1
                else: l = m + 1
        return -1

    p = findPeak(mountainArr)

    if mountainArr.get(p) == target:
        return p
    
    # 1. Search the ascending part (0 to p)
    res = orderAgnosticBinarySearch(mountainArr, target, 0, p, True)
    if res != -1:
        return res
    
    # 2. Search the descending part (p+1 to end)
    # Note: p+1 because we already checked p in the first search
    return orderAgnosticBinarySearch(mountainArr, target, p + 1, mountainArr.length() - 1, False)

# ---------------------------------------------------------
# 3. BOUNDARY SEARCH (Leftmost/First Occurrence)
# LeetCode #34: Find First and Last Position of Element
# Goal: Find the first index of a target in an array with duplicates.
# ---------------------------------------------------------
'''
34. Find First and Last Position of Element in Sorted Array

Given an array of integers nums sorted in non-decreasing order, 
find the starting and ending position of a given target value.

If target is not found in the array, return [-1, -1].

You must write an algorithm with O(log n) runtime complexity. 

Example 1:

Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]
Example 2:

Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]
Example 3:

Input: nums = [], target = 0
Output: [-1,-1]
 

Constraints:

0 <= nums.length <= 105
-109 <= nums[i] <= 109
nums is a non-decreasing array.
-109 <= target <= 109

'''
def searchRange(nums: List[int], target: int) -> List[int]:

    def binarySearch(nums, target, first_occurence):
        ans = -1
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = l + (r - l) // 2
            if nums[mid] < target:
                l = mid + 1
            elif nums[mid] > target:
                r = mid - 1
            else:
                ans = mid
                if first_occurence:
                    r = mid - 1
                else:
                    l = mid + 1
        return ans
    
    start = binarySearch(nums, target, True)
    end = binarySearch(nums, target, False)

    return [start, end]

def find_first_occurrence(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            result = mid
            right = mid - 1 # Keep shrinking right to find the "first"
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

                
# ---------------------------------------------------------
# 4. MODIFIED SEARCH (Rotated Array)
# LeetCode #33: Search in Rotated Sorted Array
# Goal: Find target in a shifted sorted array like [4,5,6,7,0,1,2].
# ---------------------------------------------------------

def search_in_rotated_array(nums: List[int], target: int) -> int:   
    def findPivot(n):
        l, r = 0, len(n) - 1
        while l <= r:
            m = l + (r - l) // 2
            # Case 1: mid is the pivot (e.g., [..., 5, 1, ...])
            if m < r and n[m] > n[m + 1]:
                return m
            # Case 2: mid-1 is the pivot
            if m > l and n[m] < n[m - 1]:
                return m - 1
            
            # Decide which way to go
            if n[m] <= n[l]:
                r = m - 1 # Pivot is to the left
            else:
                l = m + 1 # Pivot is to the right
        return -1

    def binarySearch(n, target, start, end):
        l, r = start, end
        while l <= r:
            m = l + (r - l) // 2
            if n[m] == target: return m
            if n[m] < target: l = m + 1
            else: r = m - 1
        return -1

    p = findPivot(nums)

    # If no pivot found, the array isn't rotated
    if p == -1:
        return binarySearch(nums, target, 0, len(nums) - 1)

    # Check the pivot itself
    if nums[p] == target:
        return p
    
    # Search Left side (ascending)
    res = binarySearch(nums, target, 0, p - 1)
    if res != -1:
        return res
    
    # Search Right side (also ascending in a rotated array!)
    return binarySearch(nums, target, p + 1, len(nums) - 1)

def search_in_rotated_array_alternate(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target: return mid
        
        # Check which side is sorted
        if nums[left] <= nums[mid]: # Left side is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else: # Right side is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1

def search_in_rotated_array_with_duplicates(nums: List[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    
    while l <= r:
        mid = l + (r - l) // 2
        
        if nums[mid] == target:
            return mid
        
        # --- DUPLICATE HANDLING ---
        # If the elements at l, mid, and r are the same, we can't tell 
        # which half is sorted. We just skip the duplicates.
        if nums[l] == nums[mid] == nums[r]:
            l += 1
            r -= 1
            continue
            
        # --- STANDARD ROTATED SEARCH LOGIC ---
        # 1. Check if the Left side is sorted
        if nums[l] <= nums[mid]:
            # Target is within the sorted left range
            if nums[l] <= target < nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
        
        # 2. Otherwise, the Right side must be sorted
        else:
            # Target is within the sorted right range
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
                
    return -1

'''
153. Find Minimum in Rotated Sorted Array (rotation count)
Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array nums = [0,1,2,4,5,6,7] might become:

[4,5,6,7,0,1,2] if it was rotated 4 times.
[0,1,2,4,5,6,7] if it was rotated 7 times.
Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].

Given the sorted rotated array nums of unique elements, 
return the minimum element of this array.

You must write an algorithm that runs in O(log n) time. 

Example 1:

Input: nums = [3,4,5,1,2]
Output: 1
Explanation: The original array was [1,2,3,4,5] rotated 3 times.
Example 2:

Input: nums = [4,5,6,7,0,1,2]
Output: 0
Explanation: The original array was [0,1,2,4,5,6,7] and it was rotated 4 times.
Example 3:

Input: nums = [11,13,15,17]
Output: 11
Explanation: The original array was [11,13,15,17] and it was rotated 4 times. 
 

Constraints:

n == nums.length
1 <= n <= 5000
-5000 <= nums[i] <= 5000
All the integers of nums are unique.
nums is sorted and rotated between 1 and n times.
'''

def find_min_in_rotated_array(nums: List[int]) -> int:
    # In rotated array min would be next to Pivot and otherwise the first element
    l, r = 0, len(nums) - 1
    # If the array is already sorted, rotation count is 0
    if nums[l] <= nums[r]:
        return 0
        
    while l <= r:
        mid = l + (r - l) // 2
        
        # Check if mid + 1 is the minimum
        if mid < r and nums[mid] > nums[mid + 1]:
            return mid + 1
        
        # Check if mid is the minimum
        if mid > l and nums[mid] < nums[mid - 1]:
            return mid
            
        # Decide which side to go to
        if nums[mid] >= nums[l]:
            l = mid + 1 # Pivot is on the right
        else:
            r = mid - 1 # Pivot is on the left
            
    return 0
    

'''
154. Find Minimum in Rotated Sorted Array II 
Suppose an array of length n sorted in ascending order is rotated between 1 and n times. 
For example, the array nums = [0,1,4,4,5,6,7] might become:

[4,5,6,7,0,1,4] if it was rotated 4 times.
[0,1,4,4,5,6,7] if it was rotated 7 times.
Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 
1 time results in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].

Given the sorted rotated array nums that may contain duplicates, 
return the minimum element of this array.

You must decrease the overall operation steps as much as possible.
 
Example 1:

Input: nums = [1,3,5]
Output: 1
Example 2:

Input: nums = [2,2,2,0,1]
Output: 0 

Constraints: 
n == nums.length
1 <= n <= 5000
-5000 <= nums[i] <= 5000
nums is sorted and rotated between 1 and n times.

'''

def find_min_in_rotated_array_with_duplicates(nums):
    l, r = 0, len(nums) - 1
    
    while l < r:
        mid = l + (r - l) // 2
        
        if nums[mid] > nums[r]:
            # Minimum is definitely in the right half
            l = mid + 1
        elif nums[mid] < nums[r]:
            # Minimum is at mid or in the left half
            r = mid
        else:
            # nums[mid] == nums[r]: Duplicates! 
            # We can't tell where the pivot is, so we just shrink the range.
            r -= 1
            
    return l # The index of the minimum element is the rotation count

'''
1752. Check if Array Is Sorted and Rotated 

Given an array nums, return true if the array was originally sorted in non-decreasing order, then rotated some number of positions (including zero). Otherwise, return false.

There may be duplicates in the original array.

Note: An array A rotated by x positions results in an array B of the same length such that B[i] == A[(i+x) % A.length] for every valid index i.

  
Example 1:

Input: nums = [3,4,5,1,2]
Output: true
Explanation: [1,2,3,4,5] is the original sorted array.
You can rotate the array by x = 2 positions to begin on the element of value 3: [3,4,5,1,2].
Example 2:

Input: nums = [2,1,3,4]
Output: false
Explanation: There is no sorted array once rotated that can make nums.
Example 3:

Input: nums = [1,2,3]
Output: true
Explanation: [1,2,3] is the original sorted array.
You can rotate the array by x = 0 positions (i.e. no rotation) to make nums.
 

Constraints:

1 <= nums.length <= 100
1 <= nums[i] <= 100

'''
def check_if_sorted_and_rotated(nums: List[int]) -> bool:
    #In a sorted array that has been rotated, 
    # there can be at most one point where an element is greater
    #  than the next one (a "drop"). If we find more than one drop, 
    # it means the original array was not sorted 
    count = 0
    n = len(nums)
    
    for i in range(n):
        # Use modulo to check the wrap-around case (last element vs first element)
        if nums[i] > nums[(i + 1) % n]:
            count += 1
            
        # If we find more than one 'drop', it's not sorted and rotated
        if count > 1:
            return False
            
    return True


''' 
410. Split Array Largest Sum

Given an integer array nums and an integer k, split nums into k non-empty subarrays 
such that the largest sum of any subarray is minimized.

Return the minimized largest sum of the split.

A subarray is a contiguous part of the array. 

Example 1:

Input: nums = [7,2,5,10,8], k = 2
Output: 18
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [7,2,5] and [10,8], where the largest sum 
among the two subarrays is only 18.

Example 2:

Input: nums = [1,2,3,4,5], k = 2
Output: 9
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [1,2,3] and [4,5], where the largest 
sum among the two subarrays is only 9.
 

Constraints:

1 <= nums.length <= 1000
0 <= nums[i] <= 106
1 <= k <= min(50, nums.length)
'''

def splitArray(nums: List[int], k: int) -> int:
    # 1. Define the search range for the 'Largest Sum'
    # The smallest possible max-sum is max(nums) (each number its own piece)
    # The largest possible max-sum is sum(nums) (the whole array is one piece)
    r = sum(nums)
    l = max(nums)
    while l < r:
        # 2. Pick a "guess" for the largest sum limit
        m = l + (r - l)// 2
        total = 0
        pieces = 1
        # 3. GREEDY CHECK: Can we stay under the limit 'm'?
        for n in nums:
            if total + n > m:
                total = n
                pieces += 1
            else:
                total += n
        # 4. EVALUATE THE GUESS
        if pieces > k:
            # If we needed more than k pieces, our limit 'm' was too small.
            # We must increase the limit.   
            l = m + 1
        else:
            # If we stayed within k pieces, 'm' might be the answer,
            # but let's try an even smaller limit to find the minimum.
            r = m 
    # When l == r, we've found the smallest valid maximum sum
    return r

# ---------------------------------------------------------
# 5. 2D MATRIX SEARCH 
# LeetCode 240. Search a 2D Matrix II
# Rows and columns are sorted independently; 
# no connection between the end of one row and the start of the next. 
# ---------------------------------------------------------
def staircase_search_in_2d_matrix(matrix: list[list[int]], target: int) -> bool:
    m , n = len(matrix), len(matrix[0]) 
    # we start from upper-right corner or alternatively we can start from bottom-left
    #  to eliminate a row or column from search range at every comparison
    #  time complexity of O(m + n)
    # You cannot use a single binary search because the matrix isn't "fully" sorted
    #  (e.g., the last element of row 1 might be 20, but the first element of row 2 could be 2).
    r, c = 0, n - 1
    while 0 <= r < m and 0 <= c < n:
        val = matrix[r][c]
        if val > target:
            c -= 1
        elif val < target:
            r += 1
        else:
            return True
    return False

# ---------------------------------------------------------
# 5.a. 2D MATRIX SEARCH
# LeetCode #74: Search a 2D Matrix
# The first element of each row is greater than the last element of the previous row.
# Goal: Search target in a matrix where rows/columns are sorted.
# 
def search_2d_matrix(matrix: list[list[int]], target: int) -> bool:
    if not matrix: return False
    ROWS, COLS = len(matrix), len(matrix[0])
    left, right = 0, (ROWS * COLS) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        # Map 1D index back to 2D coordinates
        mid_val = matrix[mid // COLS][mid % COLS]
        if mid_val == target: return True
        elif mid_val < target: left = mid + 1
        else: right = mid - 1
    return False

def search_2d_matrix_simplified(self, matrix: List[List[int]], target: int) -> bool:
    if not matrix or not matrix[0]: return False
    
    ROWS, COLS = len(matrix), len(matrix[0])

    # STEP 1: Binary search on the ROWS (the 'index')
    # Goal: Find the ONLY row that could possibly contain the target.
    top, bot = 0, ROWS - 1
    target_row = -1

    while top <= bot:
        mid_row = (top + bot) // 2
        # If target > last element of this row, it must be in a row below.
        if target > matrix[mid_row][-1]:
            top = mid_row + 1
        # If target < first element of this row, it must be in a row above.
        elif target < matrix[mid_row][0]:
            bot = mid_row - 1
        else:
            # target_row is now identified
            target_row = mid_row
            break

    # If no such row was found during binary search
    if target_row == -1: return False

    # STEP 2: Standard binary search within the identified row
    row = matrix[target_row]
    l, r = 0, COLS - 1
    while l <= r:
        m = (l + r) // 2
        if row[m] == target: return True
        elif row[m] < target: l = m + 1
        else: r = m - 1
        
    return False

# ---------------------------------------------------------
# 6. MEDIAN OF TWO SORTED ARRAYS (The Hard One)
# LeetCode #4: Median of Two Sorted Arrays
# Goal: Find the median in log(min(m, n)) time.
# ---------------------------------------------------------
def find_median_sorted_arrays(nums1, nums2):
    A, B = nums1, nums2
    if len(B) < len(A): A, B = B, A # Search on the smaller array
    
    total = len(A) + len(B)
    half = total // 2
    l, r = 0, len(A) - 1
    
    while True:
        i = (l + r) // 2  # Partition index for A
        j = half - i - 2  # Partition index for B
        
        A_left = A[i] if i >= 0 else float("-inf")
        A_right = A[i + 1] if (i + 1) < len(A) else float("inf")
        B_left = B[j] if j >= 0 else float("-inf")
        B_right = B[j + 1] if (j + 1) < len(B) else float("inf")
        
        if A_left <= B_right and B_left <= A_right:
            if total % 2:
                return min(A_right, B_right)
            return (max(A_left, B_left) + min(A_right, B_right)) / 2
        elif A_left > B_right:
            r = i - 1
        else:
            l = i + 1


# ---------------------------------------------------------
# 7. BINARY SEARCH ON THE ANSWER (Optimization)
# LeetCode #875: Koko Eating Bananas
# Goal: Find minimum speed 'k' to eat all bananas within 'h' hours.
# ---------------------------------------------------------
def min_eating_speed(piles: list[int], h: int) -> int:
    #NOTE: While this problem may sound intutively closer to DP, it's optimal solution lies in Binary Search
    # Whenever you see a "Minimize the Maximum" problem with a monotonic property, Binary Search is the industry-standard choice over DP. 
    left, right = 1, max(piles)
    
    def can_finish(k):
        # Calculate hours needed at speed k
        return sum(math.ceil(p/k) for p in piles) <= h

    while left < right:
        mid = left + (right - left) // 2
        if can_finish(mid):
            right = mid # Try a smaller speed
        else:
            left = mid + 1 # Need to go faster
    return left

if __name__ == "__main__":
    # Example Test
    print(f"Standard Search Index: {standard_binary_search([1, 2, 3, 4, 5], 4)}")
    print(f"Rotated Search Index: {search_in_rotated_array([4, 5, 6, 7, 0, 1, 2], 0)}")
