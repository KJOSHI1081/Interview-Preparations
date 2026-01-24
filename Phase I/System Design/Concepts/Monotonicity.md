## ⏱️ Monotonicity in Systems

**Monotonicity** is the guarantee that a value (usually time or an ID) only moves in one direction.

### 1. Monotonic Clocks
* **Usage:** Measuring timeouts, latency, and intervals.
* **Key Property:** Immune to NTP adjustments. It is a "steady ticker" from boot-up.
* **Staff Rule:** Never use `time.Now()` (Wall Clock) for duration logic; always use the system's monotonic source.

### 2. Monotonic IDs
* **Usage:** Primary keys in distributed databases.
* **Benefit:** Prevents "Index Fragmentation." When IDs are monotonic, new rows are always appended to the end of the database leaf nodes, maximizing write throughput.

### 3. Monotonic Reads (Consistency)
* **Definition:** A consistency guarantee where, if a process reads a value, any successive reads by that same process will return that same value or a more recent one. It never "sees the past" after seeing the present.

## 📊 Data Structures: Monotonic Queue

A **Monotonic Queue** is a specialized deque that keeps its elements in a strictly increasing or decreasing order.

### 🔑 Key Properties
* **Order:** Elements are sorted at all times.
* **Operations:** * `push(x)`: Removes elements from the back that are smaller (or larger) than `x` before inserting `x`.
    * `pop(x)`: Removes the element from the front if it matches `x` (used when the sliding window moves past it).
    * `max()`: Returns the front of the queue in $O(1)$.

### 🏎️ Performance Comparison
| Approach | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Brute Force | $O(n \times k)$ | $O(1)$ |
| Priority Queue (Heap) | $O(n \log k)$ | $O(k)$ |
| **Monotonic Queue** | **$O(n)$** | $O(k)$ |

### 💡 Staff Engineering Context: Stream Processing
In high-throughput stream processing (like monitoring gRPC request latencies over the last 60 seconds), we use Monotonic Queues to calculate **Rolling Maximums** or **P99s** in real-time without re-scanning the entire buffer. It turns a compute-heavy task into a simple $O(1)$ lookup.