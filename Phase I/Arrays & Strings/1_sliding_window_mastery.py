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

from collections import Counter, deque

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

    # 1. Longest Substring Without Repeating Characters (Dynamic Window)
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
            4. LONGEST REPEATING CHARACTER REPLACEMENT (Variable + Constraint)
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

    # 2. Minimum Window Substring (Dynamic Window - Two State Counters)
    # Signal: Mastering complex contraction logic and optimization.
    def minWindow(self, s: str, t: str) -> str:
        '''
                (Hard / The Final Boss)
                Definition: Smallest substring in s containing all chars of t.
                Input: s = "ADOBECODEBANC", t = "ABC"
                Output: "BANC"
                Complexity: Time O(N + M), Space O(N + M)
        '''

        if not t or not s: return ""
        target_count = Counter(t)
        required = len(target_count)
        l = r = formed = 0
        window_counts = {}
        # (length, left, right)
        ans = float("inf"), None, None

        while r < len(s):
            char = s[r]
            window_counts[char] = window_counts.get(char, 0) + 1
            if char in target_count and window_counts[char] == target_count[char]:
                formed += 1
            
            # Contract window
            while l <= r and formed == required:
                char = s[l]
                if r - l + 1 < ans[0]:
                    ans = (r - l + 1, l, r)
                window_counts[char] -= 1
                if char in target_count and window_counts[char] < target_count[char]:
                    formed -= 1
                l += 1    
            r += 1
        return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]

    # 3. Sliding Window Maximum (Fixed Window - Monotonic Deque)
    # Signal: Efficiently managing peak values in time-series data.
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
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

# Example Usage & Testing
if __name__ == "__main__":
    sol = SlidingWindowMastery()
    print(f"Max Sliding Window: {sol.maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3)}")
    # Expected: [3, 3, 5, 5, 6, 7]