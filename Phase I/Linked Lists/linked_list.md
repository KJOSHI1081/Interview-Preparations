=============================================================================
STAFF-LEVEL LINKED LIST REVISION GUIDE: THEORETICAL & ARCHITECTURAL
=============================================================================

--- PART 1: THE "STAFF" ANSWERS TO CORE ARCHITECTURAL QUESTIONS ---

1. THE MEMORY BOTTLENECK (CACHE LOCALITY)
   Q: Why is LL Merge Sort often slower than Array QuickSort in practice?
   A: SPATIAL LOCALITY. CPUs use "Prefetching" to load data into L1 cache in 
      64-byte chunks. Arrays are contiguous, so the next element is almost 
      always already in the cache. Linked Lists are scattered; every .next 
      is a "Pointer Chase" causing a "Cache Miss," forcing the CPU to wait 
      hundreds of cycles for data from RAM.

2. CONCURRENCY (LOCKING & DEADLOCKS)
   Q: How do you prevent deadlocks when moving nodes in a thread-safe DLL?
   A: LOCK ORDERING. Moving a node in a Doubly Linked List requires locking 
      the node, its current neighbors, and its new neighbors. 
      SOLUTION: Establish a global lock hierarchy (e.g., always lock nodes 
      in ascending order of memory address) or use Fine-Grained Read-Write 
      Locks with a "Try-Lock/Back-off" strategy to avoid circular waits.

3. THE "FAST/SLOW" PROOF (FLOYD'S ALGORITHM)
   Q: Why is a collision guaranteed in a cycle?
   A: RELATIVE SPEED. The distance between the fast (2 steps) and slow 
      (1 step) pointer increases/decreases by exactly 1 each iteration. 
      In a cycle of length C, the fast pointer "closes the gap." Because 
       the gap changes by 1, it must eventually hit 0. (If the delta were 
      2, it could skip over the slow pointer by landing on -1).

4. GARBAGE COLLECTION & PERSISTENCE
   Q: Can "Islands of Isolation" cause leaks?
   A: In Python/Java, Mark-and-Sweep GC handles cycles, but in Reference 
      Counting systems, they leak. 
      STAFF RULE: Always set .next = None on removed nodes. This isn't just 
      for GC; it prevents "stale" nodes from being accidentally re-attached 
      to the active list, a common cause of production data corruption.

5. SCALING (DISTRIBUTED SYSTEMS)
   Q: How do you find the N-th node from the end across 10 servers?
   A: COORDINATOR METADATA. You don't use two pointers (too many RPC calls). 
      Maintain a "Meta-Map" storing the [ServerID : NodeCount]. 
      LOGIC: Calculate absolute index (TotalLength - N). Consult the map 
      to find which server owns that index, then make ONE targeted RPC call.

--- PART 2: ROTATION LOGIC CHEAT SHEET ---

DIRECTION | NEW TAIL POSITION (from head) | NEW HEAD POSITION (from head)
-----------------------------------------------------------------------------
RIGHT (k) | (length - (k % length) - 1)   | (length - (k % length))
LEFT  (k) | (k - 1)                       | (k)

--- PART 3: 48-HOUR REVISION CHECKLIST ---

[ ] CODING: Re-write 'Reverse K-Group' and 'LFU Cache' from scratch.
[ ] CODING: Implement 'Iterative Sort List' without looking at notes.
[ ] VERBAL: Explain why an LRU Cache uses both a Hashmap AND a DLL.
[ ] ARCHITECTURE: Identify the race conditions in a DLL 'put' operation.
[ ] PERFORMANCE: Explain the memory overhead of a 64-bit pointer.

--- PART 4: DAY 5-8 PREVIEW ---
Switching to: SLIDING WINDOW, TWO-POINTER ARRAYS, and HEAPS.
Focus: Rate limiting, streaming data, and Top-K distributed processing.
=============================================================================