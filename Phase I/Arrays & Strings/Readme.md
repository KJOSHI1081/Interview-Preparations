# 🧩 Array & String Foundations: The 6 Core Patterns

Most array-based interview questions fall into these 6 foundational patterns. Master these, and you can solve 90% of the questions in the "Arrays and Strings" category.

---

### 1. The Sliding Window (Dynamic vs. Fixed)
* **The Concept:** Maintaining a subset of data as you iterate.
* **When to use:** Problems involving subarrays, substrings, or "contiguous" elements.
* **Staff Signal:** Discussing how this pattern handles **streaming data** where you can't load the entire array into memory.
* **Key Problems:** * Maximum sum subarray of size $K$ (Fixed).
    * Smallest subarray with a sum greater than $X$ (Dynamic).



### 2. Two Pointers (Converging vs. Diverging)
* **The Concept:** Using two indices to scan the array, usually moving toward each other or at different speeds.
* **When to use:** Sorted arrays, searching for pairs, or reversing data.
* **Staff Signal:** Mentioning **In-place algorithms** to achieve $O(1)$ space complexity, which is vital for high-performance systems.
* **Key Problems:**
    * 3Sum (Converging).
    * Container With Most Water (Converging).
    * Trapping Rain Water (Two pointers + Pre-computation).

### 3. Prefix Sum / Pre-computation
* **The Concept:** Calculating a cumulative sum (or product) to allow $O(1)$ range queries.
* **When to use:** "Sum of subarray between $i$ and $j$" or problems where you need to know the state of the "left side" of an index.
* **Staff Signal:** Comparing this to **Materialized Views** in databases—calculating once to serve many reads quickly.
* **Key Problems:**
    * Product of Array Except Self.
    * Subarray Sum Equals K.

    # 🎓 Master Class: Subarray & Prefix Sum Techniques

    ## 🌍 Real-World Applications
    In **Data Engineering** and **Signal Processing**, these techniques are high-performance shortcuts for pattern matching in continuous data streams.

    ### 1. Financial Systems (Auditing and Fraud)
    * **Application:** Detecting "Cyclical Transactions."
    * **The Logic:** A bank ledger treats deposits as positive and withdrawals as negative. If a group of transactions sums to zero (or a specific $k$), it may indicate "wash sales" or money-laundering loops.
    * **Efficiency:** Prefix Sum + Map scans billions of transactions in $O(n)$ time to find these loops without re-scanning history for every new entry.

    ### 2. Network Traffic & Load Balancing
    * **Application:** Finding "Balanced Windows."
    * **The Logic:** Engineers group data packets into batches exactly divisible by a fixed "Buffer Size" ($k$). This ensures hardware runs at 100% capacity without "trailing bits" wasting CPU cycles.

    ### 3. Genomics and DNA Sequencing
    * **Application:** Finding Isochores (regions with specific GC-content).
    * **The Logic:** By assigning $+1$ to one base and $-1$ to another (the LeetCode 525 "flip" strategy), scientists find the longest regions where the sum is $0$ to identify stable genomic segments.

    ### 4. Database Query Optimization
    * **Application:** Calculating "Running Totals" for dashboards.
    * **The Logic:** Databases maintain a prefix sum so range queries like $Sum(Day 10 \text{ to } Day 40)$ are calculated instantly as $P[40] - P[9]$ instead of summing 30 individual rows.

    ---

    ## 🧱 The "Modulo K" Power-Up
    The **Divisible by $k$** logic is vital for Cryptography and Data Integrity:
    * **Check-sums:** Algorithms for credit cards or ISBNs rely on sums divisible by 10 or 11.
    * **Corruption Detection:** Finding a "Subarray Divisible by $k$" helps identify which specific segment of a corrupted data stream is valid.

    ---

    ## 🛠️ Technical Mechanics

    ### 1. The Core Principle: The "Gap" Logic
    A subarray sum from index $i$ to $j$ is calculated by:
    $$SubarraySum(i, j) = PrefixSum[j] - PrefixSum[i-1]$$



    #### The HashMap Strategy ($O(n)$):
    Instead of nested loops, use a Map to store history:
    * **Count problems:** Store `{PrefixSum : Frequency}`.
    * **Longest problems:** Store `{PrefixSum : First_Index_Seen}`.
    * **Shortest problems:** Store `{PrefixSum : Last_Index_Seen}`.

    ### 2. Problem 525: Contiguous Array (Equal 0s and 1s)
    **The Trick:** Flip `0` to `-1`. The problem becomes: *"Find the longest subarray that sums to 0."*

    | Step | Logic |
    | :--- | :--- |
    | **Mapping** | Treat `0` as `-1`. |
    | **Target** | $CurrentSum - Target = 0 \implies$ Look for $CurrentSum$ in map. |
    | **Storage** | Store the **first index seen** to maximize distance. |

    ### 3. Problem 974: Subarray Sums Divisible by K
    **The Math:** $(P[j] - P[i]) \pmod k = 0 \iff P[j] \pmod k = P[i] \pmod k$

    #### Optimization (The Remainder Map):
    1. Calculate `current_sum % k`.
    2. If the remainder is in the map, add its frequency to your count.
    3. **Note:** In Python, `-1 % 5 = 4` (automatic). In Java/C++, use `(sum % k + k) % k`.

    ---

    ## ⚖️ Sliding Window vs. Prefix Sum

    | Array Content | Goal | Tool | Why? |
    | :--- | :--- | :--- | :--- |
    | **Positive Only** | $Sum = K$ | **Sliding Window** | Sum is monotonic ($O(1)$ space). |
    | **Positives + Zeros**| $Sum = K$ | **Prefix Sum Map** | Zeros create multiple subarrays for the same sum. |
    | **Negative Numbers**| Any Sum | **Prefix Sum Map** | **Mandatory.** Adding elements can decrease sum. |



    ---

    ## 🐢 Floyd’s Cycle Detection (Space Optimization)
    Used for finding duplicates in $O(1)$ space.

    * **Phase 1:** Tortoise (1x) and Hare (2x) meet at point $P$ inside the loop.
        * **The Geometry:** If $m$ is the tail and $c$ is the loop, $m + k = n \cdot c$.
    * **Phase 2:** Reset Tortoise to start. Move both 1 step at a time. They meet at the duplicate because the distance to the entrance is mathematically balanced.



    ---

    ## 🧠 The "Staff AI" Summary
    We use these algorithms to extract specific patterns from a continuous stream of noise without slowing down the system. The **Prefix Map** is memory that lets the computer say: *"I've seen this state before, so I know exactly what just happened between then and now."*

    > [!IMPORTANT]
    > **⚠️ Pro-Tip:** Never forget to initialize your map with `{0: -1}` (for indices) or `{0: 1}` (for counts). This accounts for subarrays that start at index 0!

### 4. Cyclic Sort (The "Missing Number" Pattern)
* **The Concept:** If an array contains numbers in a range (e.g., $1$ to $n$), use the index as a hash to place each number in its "rightful" spot.
* **When to use:** Finding missing, duplicate, or "first positive" integers in a limited range.
* **Staff Signal:** This is an $O(n)$ time and $O(1)$ space solution that avoids the overhead of a Hash Map.
* **Key Problems:**
    * Find the Missing Number.
    * First Missing Positive (Hard).

### 5. Overlapping Intervals
* **The Concept:** Sorting based on start/end times and merging or identifying conflicts.
* **When to use:** Scheduling, calendar events, or resource allocation.
* **Staff Signal:** This maps directly to **Distributed Locking** or **Resource Scheduling** (e.g., how Kubernetes schedules pods).
* **Key Problems:**
    * Merge Intervals.
    * Insert Interval.
    * Meeting Rooms II.

### 6. Dutch National Flag (3-Way Partitioning)
* **The Concept:** Using three pointers to sort an array into three distinct sections in a single pass.
* **When to use:** When you have a limited set of categories (e.g., 0s, 1s, and 2s).
* **Staff Signal:** Discussion on **Sorting Stability** and partitioning logic used in QuickSort pivots.
* **Key Problems:**
    * Sort Colors.

---

### 📊 Summary Table for Staff Engineers

| Pattern | Complexity Goal | Distributed System Analog |
| :--- | :--- | :--- |
| **Sliding Window** | $O(N)$ Time / $O(1)$ Space | Rate Limiting / Flow Control |
| **Two Pointers** | $O(N)$ Time / $O(1)$ Space | Data Deduplication / Merging Streams |
| **Prefix Sum** | $O(1)$ Query Time | OLAP Cubes / Data Warehousing |
| **Intervals** | $O(N \log N)$ Time | Resource Scheduling / Concurrency |

---