class DivideAndConquerMastery:
    """
    Top 7 Divide and Conquer problems for Arrays & Strings.
    Pattern: Split problem into sub-problems, solve recursively, and combine.
    """

    def countInversions(self, arr: list[int]) -> int:
        """
        1. COUNT INVERSIONS (Modified Merge Sort)
        Definition: Count pairs (i, j) where i < j and arr[i] > arr[j].
        Input: [8, 4, 2, 1]
        Output: 6 (Pairs: (8,4), (8,2), (8,1), (4,2), (4,1), (2,1))
        Complexity: Time O(N log N), Space O(N)
        """
        def merge_and_count(data):
            if len(data) <= 1: return data, 0
            
            mid = len(data) // 2
            left, count_l = merge_and_count(data[:mid])
            right, count_r = merge_and_count(data[mid:])
            
            merged = []
            i = j = count = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    # If right[j] is smaller, it's an inversion with ALL remaining left elements
                    merged.append(right[j])
                    count += (len(left) - i)
                    j += 1
            merged += left[i:]
            merged += right[j:]
            return merged, count_l + count_r + count

        _, total_inversions = merge_and_count(arr)
        return total_inversions

    def longestNiceSubstring(self, s: str) -> str:
        """
        2. LONGEST NICE SUBSTRING
        Definition: Substring where every letter exists in both upper and lower case.
        Input: "YazaAay"
        Output: "aAa"
        Complexity: Time O(N^2) worst case, but O(N log N) average.
        """
        if len(s) < 2: return ""
        chars = set(s)
        for i, c in enumerate(s):
            # If the counterpart is missing, s[i] cannot be in any nice substring
            if c.swapcase() not in chars:
                s1 = self.longestNiceSubstring(s[:i])
                s2 = self.longestNiceSubstring(s[i+1:])
                return s1 if len(s1) >= len(s2) else s2
        return s

    def longestSubstringAtLeastK(self, s: str, k: int) -> int:
        """
        3. LONGEST SUBSTRING WITH AT LEAST K REPEATING CHARACTERS
        Definition: Every character in the substring must appear >= k times.
        Input: s = "ababbc", k = 2
        Output: 5 ("ababb")
        Complexity: Time O(N^2) worst, usually O(N log N)
        """
        if len(s) < k: return 0
        for c in set(s):
            if s.count(c) < k:
                # Character 'c' breaks the rule, split around it
                return max(self.longestSubstringAtLeastK(sub, k) for sub in s.split(c))
        return len(s)

    def diffWaysToCompute(self, expression: str) -> list[int]:
        """
        4. DIFFERENT WAYS TO ADD PARENTHESES
        Definition: Return all possible results from grouping operators differently.
        Input: "2-1-1"
        Output: [0, 2] -> ((2-1)-1) = 0 and (2-(1-1)) = 2
        Complexity: Exponential (Catalan Number)
        """
        memo = {}
        def solve(expr):
            if expr in memo: return memo[expr]
            if expr.isdigit(): return [int(expr)]
            
            res = []
            for i, char in enumerate(expr):
                if char in "+-*":
                    # Divide at the operator
                    left = solve(expr[:i])
                    right = solve(expr[i+1:])
                    # Combine results
                    for l in left:
                        for r in right:
                            if char == '+': res.append(l + r)
                            elif char == '-': res.append(l - r)
                            elif char == '*': res.append(l * r)
            memo[expr] = res
            return res
        return solve(expression)

    def maxSubArray(self, nums: list[int]) -> int:
        """
        5. MAXIMUM SUBARRAY (Divide and Conquer Version)
        Definition: Find contiguous subarray with the largest sum.
        Input: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
        Output: 6 ([4, -1, 2, 1])
        Complexity: Time O(N log N)
        """
        def find_max_crossing(l, m, r):
            left_sum = float('-inf')
            curr = 0
            for i in range(m, l - 1, -1):
                curr += nums[i]
                left_sum = max(left_sum, curr)
                
            right_sum = float('-inf')
            curr = 0
            for i in range(m + 1, r + 1):
                curr += nums[i]
                right_sum = max(right_sum, curr)
            return left_sum + right_sum

        def solve(l, r):
            if l == r: return nums[l]
            mid = (l + r) // 2
            # Max is either in left half, right half, or crossing the middle
            return max(solve(l, mid), solve(mid + 1, r), find_max_crossing(l, mid, r))

        return solve(0, len(nums) - 1)

    def constructBeautifulArray(self, n: int) -> list[int]:
        """
        6. BEAUTIFUL ARRAY
        Definition: Array where for i < k < j, arr[i] + arr[j] != 2*arr[k].
        Input: n = 4
        Output: [1, 3, 2, 4]
        Complexity: Time O(N log N)
        """
        # Logic: (Odd + Even) != 2 * k. Transform range(n) into Odds and Evens recursively.
        memo = {1: [1]}
        def solve(count):
            if count in memo: return memo[count]
            # Map odd indices: 2*x - 1, Map even indices: 2*x
            odds = solve((count + 1) // 2)
            evens = solve(count // 2)
            memo[count] = [2 * x - 1 for x in odds] + [2 * x for x in evens]
            return memo[count]
        return solve(n)

    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        """
        7. MEDIAN OF TWO SORTED ARRAYS (Hard)
        Definition: Find median of two sorted arrays in log time.
        Complexity: Time O(log(min(M, N)))
        """
        A, B = nums1, nums2
        if len(B) < len(A): A, B = B, A
        total = len(A) + len(B)
        half = total // 2
        
        l, r = 0, len(A) - 1
        while True:
            i = (l + r) // 2  # Partition for A
            j = half - i - 2  # Partition for B
            
            Aleft = A[i] if i >= 0 else float("-inf")
            Aright = A[i + 1] if (i + 1) < len(A) else float("inf")
            Bleft = B[j] if j >= 0 else float("-inf")
            Bright = B[j + 1] if (j + 1) < len(B) else float("inf")
            
            # If partition is correct
            if Aleft <= Bright and Bleft <= Aright:
                # Odd total
                if total % 2: return min(Aright, Bright)
                # Even total
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2
            elif Aleft > Bright:
                r = i - 1
            else:
                l = i + 1