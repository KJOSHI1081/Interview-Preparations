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
-------------------------------------------------------------------------------
"""

from collections import Counter, deque

class SlidingWindowMastery:

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

    # 2. Minimum Window Substring (Dynamic Window - Two State Counters)
    # Signal: Mastering complex contraction logic and optimization.
    def minWindow(self, s: str, t: str) -> str:
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

    # 4. Longest Repeating Character Replacement (Dynamic Window - Max Frequency)
    # Signal: Understanding error-tolerance and "best-fit" windowing.
    def characterReplacement(self, s: str, k: int) -> int:
        count = {}
        max_f = l = res = 0
        for r in range(len(s)):
            count[s[r]] = 1 + count.get(s[r], 0)
            # max_f tracks the most frequent char we've ever seen in a window
            max_f = max(max_f, count[s[r]])
            
            # Window is invalid if replacements needed > k
            if (r - l + 1) - max_f > k:
                count[s[l]] -= 1
                l += 1
            res = max(res, r - l + 1)
        return res

    # 5. Subarrays with K Different Integers (The Decomposition Pattern)
    # Signal: Complex problem decomposition—the mark of a Staff Engineer.
    def subarraysWithKDistinct(self, nums: list[int], k: int) -> int:
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