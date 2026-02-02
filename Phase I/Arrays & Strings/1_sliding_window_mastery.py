


from collections import Counter, deque, defaultdict

"""
FILE: sliding_window_mastery.py
TOPIC: Phase I - Arrays & Strings (Sliding Window Pattern)
TARGET: Staff Engineer Interview Preparation
-------------------------------------------------------------------------------
STAFF-LEVEL KEY TAKEAWAYS:
1. FLOW CONTROL: Think of Sliding Window as a "Flow Control" mechanism. 
   It mimics how TCP windows manage congestion or how stream processors 
   (like Flink) handle windowing over infinite data.

2. STATE SEPARATION: Keep your 'window state' (HashMap/Counters) distinct from 
   your 'pointers'. This makes the code modular and easier to explain.

3. COMPLEXITY: All these solutions are O(N) Time and O(K) Space (where K is 
   the size of the window/alphabet). Mentioning the O(1) space optimization 
   (using a fixed-size array instead of a Hash Map for ASCII) is a great signal.

4. THE "AT MOST" TRICK: For "Exactly K" problems, always remember the 
   mathematical decomposition: Exactly(K) = AtMost(K) - AtMost(K-1).


To master the Sliding Window pattern, you need to recognize that it comes in two flavors: Fixed Size (easier) and Variable Size (harder).

If you master these 7 problems, you will cover roughly 90% of the variations used in interviews at companies like Google, Meta, and Amazon.

1. The "Basics" (Fixed Window)
Maximum Sum Subarray of Size K: The introductory problem. It teaches you how to "roll" the window by adding the new element and subtracting the old one.

Find All Anagrams in a String: Teaches you how to use a frequency map (hash map) inside a sliding window.

Pattern: Maintain a window of size len(target). If the character counts match, you've found an anagram.

2. The "Shrinkable" (Variable Window)
Longest Substring Without Repeating Characters: The absolute classic. It teaches you how to dynamically move the start pointer based on a condition (duplicate discovery).

Longest Repeating Character Replacement: A common "Hard-Medium." It forces you to track the frequency of the most common character in the current window to decide if the window is still "valid."

3. The "Constraint" Pattern (The "Nice Substring" style)
Subarrays with K Different Integers: This is a "Hard" problem. It uses the "At Most K" trick. To find "Exactly K," you calculate atMost(K) - atMost(K-1).

Fruit Into Baskets: A friendly way to practice windows with a constraint of "exactly 2 types."

4. The "Final Boss"
Minimum Window Substring: If you can solve this from scratch without help, you have mastered the pattern. It involves a "matching" counter and complex pointer movements.
-------------------------------------------------------------------------------
"""

class SlidingWindowMastery:
    
    def max_sub_array_of_size_k(self, k: int, arr: list[int]) -> int:
        """
        1. MAXIMUM SUM SUBARRAY OF SIZE K (Fixed Window)
        Definition: Find the contiguous subarray of size k with the largest sum.
        Input: arr = [2, 1, 5, 1, 3, 2], k = 3
        Output: 9 (from [5, 1, 3])
        Complexity: Time O(N), Space O(1)
        """
        max_sum, window_sum = 0, 0
        start = 0

        for end in range(len(arr)):
            window_sum += arr[end]
            
            # Slide the window once we reach size k
            if end >= k - 1:
                max_sum = max(max_sum, window_sum)
                window_sum -= arr[start]
                start += 1
        return max_sum
    

    def findAnagrams(self, s: str, p: str) -> list[int]:
            """
            2. FIND ALL ANAGRAMS IN A STRING (Fixed Window + Hash Map)
            Definition: Find all start indices of p's anagrams in s.
            Input: s = "cbaebabacd", p = "abc"
            If the input is:
                s = "cbaebabacd"

                p = "abc"

                Index 0: Substring "cba" is an anagram of "abc". → [0]

                Index 1: Substring "bae" is NOT an anagram.

                Index 2: Substring "aeb" is NOT an anagram.

                Index 6: Substring "bac" is an anagram of "abc". → [0, 6]
            Output: [0, 6]
            Complexity: Time O(N), Space O(1) (max 26 chars in map)
            """
            p_count = Counter(p)
            s_count = Counter()
            res = []
            
            for i in range(len(s)):
                s_count[s[i]] += 1
                if i >= len(p):
                    left_char = s[i - len(p)]
                    if s_count[left_char] == 1:
                        del s_count[left_char]
                    else:
                        s_count[left_char] -= 1
                
                if s_count == p_count:
                    res.append(i - len(p) + 1)
            return res

    # 1. Longest Substring Without Repeating Characters (Variable (Shrinkable) Window)
    # Signal: Ability to handle deduplication in streaming data.
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_map = {} 
        max_len = start = 0
        for end, char in enumerate(s):
            if char in char_map and char_map[char] >= start:
                start = char_map[char] + 1
            char_map[char] = end
            max_len = max(max_len, end - start + 1)
        return max_len
    '''
    The Technical Reality: $O(1)$ vs $O(k)$ 
    In above code, the char_map size is bounded by the number of unique characters in the 
    input string's character set (e.g., 26 for lowercase English, 128 for ASCII,
      or 1,114,112 for Unicode).If the character set is fixed (e.g., ASCII): 
      The space complexity is already $O(1)$ because the map will never exceed 128 (or 256) 
      entries, regardless of how long the input string $N$ is.If the character 
      set is infinite (theoretical): The space is $O(k)$.

      The Optimized "Fixed Array" Approach
      To strictly avoid the overhead of a Python dictionary (hash map) and 
      demonstrate a low-level $O(1)$ mindset, you can use a fixed-size array.
        This is often faster in practice because it avoids hashing collisions and dynamic 
        resizing.
    '''
    
    def lengthOfLongestSubstringOptimized(self, s: str) -> int:
        '''
        3. Longest Substring Without Repeating Characters
        
        Given a string s, find the length of the longest substring without duplicate characters.

        

        Example 1:

        Input: s = "abcabcbb"
        Output: 3
        Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.
        Example 2:

        Input: s = "bbbbb"
        Output: 1
        Explanation: The answer is "b", with the length of 1.
        Example 3:

        Input: s = "pwwkew"
        Output: 3
        Explanation: The answer is "wke", with the length of 3.
        Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
        '''
        # Assuming ASCII (128) or Extended ASCII (256)
        # Using an array initialized to -1 (last seen index)
        last_seen = [-1] * 256
        max_len = start = 0
        
        for end, char in enumerate(s):
            char_code = ord(char)
            
            # If the char was seen within the current window, move start
            if last_seen[char_code] >= start:
                start = last_seen[char_code] + 1
                
            last_seen[char_code] = end
            max_len = max(max_len, end - start + 1)
            
        return max_len
    
    def characterReplacement(self, s: str, k: int) -> int:
            """
            4. LONGEST REPEATING CHARACTER REPLACEMENT (Dynamic (Non-Shrinkable) Window + Constraint)
            Definition: Maximize same-letter substring length by replacing k chars.
            Input: s = "AABABBA", k = 1
            Output: 4
            Complexity: Time O(N), Space O(1)
            """
            count = {}
            max_len = start = max_freq = 0
            
            for end in range(len(s)):
                count[s[end]] = count.get(s[end], 0) + 1
                # Track the most frequent character in the current window
                max_freq = max(max_freq, count[s[end]])
                
                # If (window size - max_freq) > k, we need more than k replacements
                if (end - start + 1) - max_freq > k:
                    count[s[start]] -= 1
                    start += 1
                    
                max_len = max(max_len, end - start + 1)
            return max_len
    
    def totalFruit(self, fruits: list[int]) -> int:
        """
        5. FRUIT INTO BASKETS (Variable + 2-Unique Constraint)
        Definition: Find longest subarray with at most 2 unique integers.
        Input: fruits = [1, 2, 3, 2, 2]
        Output: 4 ([2, 3, 2, 2])
        Complexity: Time O(N), Space O(1)
        """
        count = {}
        start = max_fruits = 0
        
        for end in range(len(fruits)):
            count[fruits[end]] = count.get(fruits[end], 0) + 1
            
            while len(count) > 2:
                count[fruits[start]] -= 1
                if count[fruits[start]] == 0:
                    del count[fruits[start]]
                start += 1
            max_fruits = max(max_fruits, end - start + 1)
        return max_fruits 
    
    # 3. Sliding Window Maximum (Fixed Window - Monotonic Deque)
    # Signal: Efficiently managing peak values in time-series data.
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        ''' 
        239. Sliding Window Maximum
        You are given an array of integers nums, there is a sliding window of size k which is moving from the 
        very left of the array to the very right. You can only see the k numbers in the window. 
        Each time the sliding window moves right by one position.
        Return the max sliding window.

        Example 1:

        Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
        Output: [3,3,5,5,6,7]
        Explanation: 
        Window position                Max
        ---------------               -----
        [1  3  -1] -3  5  3  6  7       3
        1 [3  -1  -3] 5  3  6  7       3
        1  3 [-1  -3  5] 3  6  7       5
        1  3  -1 [-3  5  3] 6  7       5
        1  3  -1  -3 [5  3  6] 7       6
        1  3  -1  -3  5 [3  6  7]      7
        Example 2:

        Input: nums = [1], k = 1
        Output: [1]
        '''
        res = []
        # Stores indices of elements in decreasing order of their values
        q = deque() 
        for i, n in enumerate(nums):
            while q and nums[q[-1]] < n:
                q.pop()
            q.append(i)
            # Remove indices that have slid out of the window
            if q[0] == i - k:
                q.popleft()
            # Once window is full, front of deque is the max
            if i >= k - 1:
                res.append(nums[q[0]])
        return res

    # 2. Minimum Window Substring (Dynamic Window - Two State Counters)
    # Signal: Mastering complex contraction logic and optimization. 
    def minWindow(self, s: str, t: str) -> str:

        '''
        76. Minimum Window Substring 
            Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t
            (including duplicates) is included in the window. If there is no such substring, return the empty string "".

            The testcases will be generated such that the answer is unique. 
        '''
        ans = ""
        # Base Case: If source is smaller than target, a valid window is impossible
        if not s or not t or len(s) < len(t): 
            return ans
        
        # window: current character frequencies in the sliding window
        # target: required character frequencies from string 't'
        window, target = defaultdict(int), defaultdict(int)
        for c in t:
            target[c] += 1

        # have: how many unique characters in 'window' meet the frequency in 'target'
        # need: the total unique characters in 't' that must be satisfied
        have, need = 0, len(target)
        min_window_size = float('inf')

        start = end = 0

        # EXPANSION PHASE: Move the 'end' pointer to find a valid window
        while end < len(s):
            c = s[end]
            window[c] += 1
            
            # If the current character's count matches exactly what we need, increment 'have'
            if c in target and target[c] == window[c]:
                have += 1
            
            # CONTRACTION PHASE: Once the window is valid ('have == need'), 
            # shrink from the 'start' to find the smallest possible substring
            while have == need and start <= end:
                window_size = (end - start + 1)
                
                # Update the global minimum if the current window is smaller
                if min_window_size > window_size:
                    ans = s[start: end + 1]
                    min_window_size = window_size
                
                # Remove the character at 'start' and move the pointer forward
                c = s[start]
                window[c] -= 1
                
                # If removing this char breaks our 'target' requirement, decrement 'have'
                if c in target and window[c] < target[c]:
                    have -= 1
                
                start += 1 # Shrink the window
                
            end += 1 # Expand the window
            
        return ans


    # 5. Subarrays with K Different Integers (The Decomposition Pattern)
    # Signal: Complex problem decomposition—the mark of a Staff Engineer.
    def subarraysWithKDistinct(self, nums: list[int], k: int) -> int:
        """
            6. SUBARRAYS WITH K DIFFERENT INTEGERS (Hard / Exactly K)
            Definition: Count subarrays with exactly k different integers.
            Pattern: Exactly(K) = AtMost(K) - AtMost(K-1)
            Input: nums = [1, 2, 1, 2, 3], k = 2
            Output: 7
            Complexity: Time O(N), Space O(K)

            Given an integer array nums and an integer k, return the number of good subarrays of nums.

            A good array is an array where the number of different integers in that array is exactly k.

            For example, [1,2,3,1,2] has 3 different integers: 1, 2, and 3.
            A subarray is a contiguous part of an array.

            

            Example 1:

            Input: nums = [1,2,1,2,3], k = 2
            Output: 7
            Explanation: Subarrays formed with exactly 2 different integers: [1,2], [2,1], [1,2], [2,3], [1,2,1], [2,1,2], [1,2,1,2]
            Example 2:

            Input: nums = [1,2,1,3,4], k = 3
            Output: 3
            Explanation: Subarrays formed with exactly 3 different integers: [1,2,1,3], [2,1,3], [1,3,4].
 
        """
        def atMost(n):
            count = {}
            l = res = 0
            for r in range(len(nums)):
                count[nums[r]] = count.get(nums[r], 0) + 1
                while len(count) > n:
                    count[nums[l]] -= 1
                    if count[nums[l]] == 0:
                        del count[nums[l]]
                    l += 1
                res += (r - l + 1)
            return res
        return atMost(k) - atMost(k - 1)
    

    def solve_k_distinct(nums: list[int], k: int, return_list: bool = False):
        ''' 
        992. Subarrays with K Different Integers
        To return the actual subarrays (the lists of elements) rather than just the count, we use the Three-Pointer technique. 
        This allows us to find the range of valid starting positions for every ending position
        This solution uses two "left" pointers to maintain the boundaries of the "Exactly K" range.
        o build a solution that is efficient for both counting and returning the subarrays, we use the Three-Pointer strategy.The beauty of this approach is that for every right position, the number of valid subarrays is simply the "width" of the start-pointer range: (left_near - left_far). 
        You can sum these widths to get the count in O(N) time, or iterate through them to collect the subarrays in 
        O(total subarrays) time.

        Why this is the "Staff" choiceSingle Pass Logic: We only traverse the right pointer once.
        We don't need to run two separate "AtMost" functions, which saves on overhead.
        Decoupled Complexity: * The count logic remains O(N).
        The collection logic is O(total subarrays).
        By using a boolean flag or a generator, you avoid the O(N^2) space penalty when you only need the count.
        The "Gap" Logic: The distance between left_far (the earliest valid start) and left_near (the first invalid start after shrinking) 
        represents the number of duplicates we can skip while still having exactly K distinct numbers.
        Think of it this way:

        Min Window Substring: You want the smallest window that satisfies a condition.

        Subarrays with K Distinct: You want all possible windows that satisfy a condition. 
        '''
        left, right, prefix = 0, 0, 0
        sub_arrays = []
        window = defaultdict(int)
        res = 0

        while right < len(nums):
            num = nums[right]
            window[num] += 1
            
            # Phase 1: Keep window valid (distinct count <= k)
            while len(window) > k:
                num = nums[left]
                window[num] -= 1
                if not window[num]:
                    del window[num]
                left += 1
                prefix = 0
            
            # Phase 2: Count leading duplicates (prefixes)/Standardize the window (shrink left as long as it's a duplicate)
            while window[nums[left]] > 1:
                prefix += 1
                window[nums[left]] -= 1
                left += 1

            # Phase 3: Collect results
            if len(window) == k:
                # 1. Add the current unique window
                res += (1 + prefix)
                if return_list:
                    # 2. Extract subarrays: from (left - prefix) up to left
                    # All these starting points are valid for the current 'right'
                    for i in range(left - prefix, left + 1): 
                        sub_arrays.append(nums[i:right + 1])#  Yield results one by one yield nums[i : right + 1] to reduce the memory footprint
            right += 1
        print(f'{sub_arrays=}')
        return res

    # Example
    # count, arrays = solve_k_distinct([1, 2, 1, 2, 3], 2, return_list=True)
    def longestNiceSubarray(self, nums: list[int]) -> int:
        '''
        2401. Longest Nice Subarray
        You are given an array nums consisting of positive integers.

        We call a subarray of nums nice if the bitwise AND of every pair of elements that are in different positions in the subarray is equal to 0.

        Return the length of the longest nice subarray.

        A subarray is a contiguous part of an array.

        Note that subarrays of length 1 are always considered nice.

        '''
        start, max_len, mask = 0, 1, 0

        for end in range(len(nums)):
            num = nums[end]
            # In standard binary addition, (1 + 1) causes a carry to the next bit position. 
            # However, since a "nice" subarray guarantees that no two numbers share a set bit, 
            # you will never have a (1 + 1) situation at any bit position while the window is valid.
            while (mask & num) != 0:
                mask -=  nums[start] # mask ^= nums[start]
                start += 1
            mask += num  # mask |= num
            max_len = max(max_len, end - start + 1)
        return max_len
    
# Example Usage & Testing
if __name__ == "__main__":
    sol = SlidingWindowMastery()
    print(f"Max Sliding Window: {sol.maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3)}")
    # Expected: [3, 3, 5, 5, 6, 7]

