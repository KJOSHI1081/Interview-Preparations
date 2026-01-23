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